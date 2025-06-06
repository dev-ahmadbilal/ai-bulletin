from sqlalchemy import Column, Integer, String, DateTime, Text, func
from database import Base
 
class Subscriber(Base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class NewsletterTopic(Base):
    __tablename__ = "newsletter_topics"
    id = Column(Integer, primary_key=True, index=True)
    week = Column(String, unique=True, index=True)
    topics_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Newsletter(Base):
    __tablename__ = "newsletters"
    id = Column(Integer, primary_key=True, index=True)
    week = Column(String, unique=True, index=True)
    html = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 