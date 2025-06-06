from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import engine, Base, get_db
from sqlalchemy.exc import IntegrityError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from jobs.newsletter_job import weekly_newsletter_job

from admin import admin_router
from utils.email import send_email

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    trigger = CronTrigger(day_of_week="sun", hour=10, minute=0)
    scheduler.add_job(weekly_newsletter_job, trigger, id="weekly_newsletter_job")
    scheduler.start()

    print("✅ APScheduler started")
    yield

    scheduler.shutdown()
    print("🛑 APScheduler shut down")

app = FastAPI(lifespan=lifespan)
app.include_router(admin_router)

def get_latest_newsletter_content(db: Session):
    newsletter = db.query(models.Newsletter).order_by(models.Newsletter.created_at.desc()).first()
    if not newsletter:
        return None, None
    return newsletter.week, newsletter.html

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

        # Fetch newsletter content and send email
        week, html_content = get_latest_newsletter_content(db)
        if html_content:
            send_email(
                to=[email],
                subject=f"📰 AI Bulletin - Week {week}",
                html=html_content
            )

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

        # Fetch newsletter content and send email
        subject, html_content = get_latest_newsletter_content(db)
        if subject and html_content:
            send_email(
                to_email=email,
                subject=subject,
                text=None,
                html=html_content
            )

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