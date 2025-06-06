import logging
from database import get_db
from models import Subscriber
from crew.crew_engine import run_newsletter_pipeline
from utils.email import send_email

logging.basicConfig(level=logging.INFO)

def weekly_newsletter_job():
    logging.info("⏰ Starting newsletter pipeline...")
    result = run_newsletter_pipeline()

    week = result["week"]
    html = result["final_html"]

    db = next(get_db())
    subscribers = db.query(Subscriber).all()
    logging.info(f"📬 Sending newsletter to {len(subscribers)} subscribers")

    for sub in subscribers:
        send_email(
            to=[sub.email],
            subject=f"📰 AI Bulletin - Week {week}",
            html=html
        )

    logging.info("✅ All emails sent successfully.")

if __name__ == "__main__":
    weekly_newsletter_job()