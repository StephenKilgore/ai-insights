from ..db import db
import uuid
from datetime import datetime

class JobModel(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    service_name = db.Column(db.String, nullable=False)
    job_start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    job_end_date = db.Column(db.DateTime)
    rows_processed = db.Column(db.Integer, nullable=False, default=0)
    rows_failed = db.Column(db.Integer, nullable=False, default=0)
    runtime = db.Column(db.Float, nullable=False, default=0.0)

    collector_messages = db.relationship("Message", foreign_keys="Message.collector_job_id",
                                      back_populates="collector_job")
    analyzer_messages = db.relationship("Message", foreign_keys="Message.analyzer_job_id", back_populates="analyzer_job")