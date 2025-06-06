from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine, Base, get_db
from sqlalchemy.exc import IntegrityError

from admin import admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(admin_router)

# Home page with subscription form
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request, db: Session = Depends(get_db)):
    count = db.query(models.Subscriber).count()
    return templates.TemplateResponse("index.html", {"request": request, "subscriber_count": count})


# HTML Form POST submission
@app.post("/subscribe", response_class=HTMLResponse)
async def subscribe_email(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    subscriber = models.Subscriber(email=email)
    message = None
    error = None

    try:
        db.add(subscriber)
        db.commit()
        db.refresh(subscriber)
        message = f"Thanks for subscribing, {email}!"
    except IntegrityError:
        db.rollback()
        error = f"{email} is already subscribed."

    count = db.query(models.Subscriber).count()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "subscriber_count": count,
        "message": message,
        "error": error,
    })


# JSON API POST submission
@app.post("/subscribe", response_class=JSONResponse)
async def subscribe_from_json(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    email = data.get("email")
    if not email:
        raise HTTPException(status_code=422, detail="Email is required.")

    subscriber = models.Subscriber(email=email)
    db.add(subscriber)
    try:
        db.commit()
        db.refresh(subscriber)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already subscribed."
        )
    return {"message": "Successfully subscribed!"}

@app.get("/health")
def health():
    return {"status": "ok"}

# GET: Show Unsubscribe Form
@app.get("/unsubscribe", response_class=HTMLResponse)
async def get_unsubscribe_form(request: Request):
    return templates.TemplateResponse("unsubscribe.html", {"request": request})

# POST: Process Unsubscribe Request
@app.post("/unsubscribe", response_class=HTMLResponse)
async def unsubscribe_email(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    subscriber = db.query(models.Subscriber).filter(models.Subscriber.email == email).first()
    if subscriber:
        db.delete(subscriber)
        db.commit()
        message = f"{email} has been unsubscribed successfully."
    else:
        message = f"{email} was not found in the subscription list."

    return templates.TemplateResponse("unsubscribe.html", {
        "request": request,
        "message": message
    })