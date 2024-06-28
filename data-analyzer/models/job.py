import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.orm import relationship
from db import Base

from models.message import Message
class Job(Base):
    __tablename__ = 'jobs'
    id = Column(String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    service_name = Column(String, nullable=False)
    job_start_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    job_end_date = Column(DateTime)
    rows_processed = Column(Integer, nullable=False, default=0)
    rows_failed = Column(Integer, nullable=False, default=0)
    runtime = Column(Float, nullable=False, default=0.0)

    collector_messages = relationship("Message", foreign_keys="Message.collector_job_id", back_populates="collector_job")
    analyzer_messages = relationship("Message", foreign_keys="Message.analyzer_job_id", back_populates="analyzer_job")
