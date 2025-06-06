from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import Session
import os
from database import get_db
from models import Subscriber, NewsletterTopic, Newsletter
from fastapi.templating import Jinja2Templates

import models

templates = Jinja2Templates(directory="templates")
admin_router = APIRouter()

# Change this password
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "secret")

# --- Login Page ---
@admin_router.get("/admin/login")
def login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

# --- Login Form Submission ---
@admin_router.post("/admin/login")
def login(request: Request, password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin/dashboard", status_code=HTTP_303_SEE_OTHER)
        response.set_cookie(key="admin", value="true", httponly=True)
        return response
    return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Incorrect password."})

# --- Authentication Helper ---
def require_admin(request: Request):
    if request.cookies.get("admin") != "true":
        raise HTTPException(status_code=403, detail="Access Denied")

# --- Admin Dashboard ---
@admin_router.get("/admin/dashboard")
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    subscribers = db.query(Subscriber).order_by(Subscriber.created_at.desc()).all()
    topics = db.query(NewsletterTopic).order_by(NewsletterTopic.created_at.desc()).all()
    newsletters = db.query(Newsletter).order_by(Newsletter.created_at.desc()).all()
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "subscribers": subscribers,
        "topics": topics,
        "newsletters": newsletters
    })

# --- Delete Subscriber ---
@admin_router.post("/admin/delete/subscriber/{id}")
def delete_subscriber(id: int, request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    db.query(Subscriber).filter(Subscriber.id == id).delete()
    db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=HTTP_303_SEE_OTHER)

# --- Delete Newsletter Topic ---
@admin_router.post("/admin/delete/topic/{id}")
def delete_topic(id: int, request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    db.query(NewsletterTopic).filter(NewsletterTopic.id == id).delete()
    db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=HTTP_303_SEE_OTHER)

# --- Delete Newsletter ---
@admin_router.post("/admin/delete/newsletter/{id}")
def delete_newsletter(id: int, request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    db.query(Newsletter).filter(Newsletter.id == id).delete()
    db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=HTTP_303_SEE_OTHER)

@admin_router.post("/admin/subscribers/{subscriber_id}/edit")
def edit_subscriber(subscriber_id: int, email: str = Form(...), db: Session = Depends(get_db)):
    subscriber = db.query(models.Subscriber).get(subscriber_id)
    if subscriber:
        subscriber.email = email
        db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=303)

@admin_router.post("/admin/topics/{topic_id}/edit")
def edit_topic(topic_id: int, week: str = Form(...), topics_json: str = Form(...), db: Session = Depends(get_db)):
    topic = db.query(models.NewsletterTopic).get(topic_id)
    if topic:
        topic.week = week
        topic.topics_json = topics_json
        db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=303)

@admin_router.post("/admin/newsletters/{newsletter_id}/edit")
def edit_newsletter(newsletter_id: int, week: str = Form(...), html: str = Form(...), db: Session = Depends(get_db)):
    newsletter = db.query(models.Newsletter).get(newsletter_id)
    if newsletter:
        newsletter.week = week
        newsletter.html = html
        db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=303)