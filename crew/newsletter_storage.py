from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal, engine, Base
from models import NewsletterTopic, Newsletter

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def store_newsletter_data(week: str, topics_json: str, final_html: str) -> str:
    """
    Store the weekly newsletter data in SQLite database.
    
    Args:
        week (str): The current week identifier (e.g., '2025-W23')
        topics_json (str): JSON string from the topic planner agent
        final_html (str): HTML string of the formatted newsletter
        
    Returns:
        str: Success or error message
    """
    db = SessionLocal()
    try:
        # Start a transaction
        with db.begin():
            # Handle NewsletterTopic
            existing_topic = db.query(NewsletterTopic).filter_by(week=week).first()
            if existing_topic:
                db.delete(existing_topic)
            
            new_topic = NewsletterTopic(
                week=week,
                topics_json=topics_json,
                created_at=datetime.utcnow()
            )
            db.add(new_topic)
            
            # Handle Newsletter
            existing_newsletter = db.query(Newsletter).filter_by(week=week).first()
            if existing_newsletter:
                db.delete(existing_newsletter)
            
            new_newsletter = Newsletter(
                week=week,
                html=final_html,
                created_at=datetime.utcnow()
            )
            db.add(new_newsletter)
            
        return f"✅ Stored weekly topics and newsletter HTML for week {week}"
        
    except SQLAlchemyError as e:
        db.rollback()
        return f"❌ Error storing newsletter data: {str(e)}"
    finally:
        db.close() 