from sqlalchemy import Column, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Message(Base):
    __tablename__ = 'messages'
    id = Column(String, primary_key=True, nullable=False)
    author_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    text = Column(String, nullable=False)
    processed = Column(Boolean, nullable=False)
    sentiment_score = Column(Float)
    sentiment_magnitude = Column(Float)
    sentiment_text = Column(String)
    sentiment_classification = Column(String)
    magnitude_classification = Column(String)
    collector_job_id = Column(String, ForeignKey("jobs.id"))
    analyzer_job_id = Column(String, ForeignKey("jobs.id"))

    collector_job = relationship("Job", foreign_keys=[collector_job_id], back_populates="collector_messages")
    analyzer_job = relationship("Job", foreign_keys=[analyzer_job_id], back_populates="analyzer_messages")
