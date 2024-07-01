from db import db


class MessageModel(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.String, primary_key=True, nullable=False)
    author_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.String, nullable=False)
    processed = db.Column(db.Boolean, nullable=False)
    sentiment_score = db.Column(db.Float)
    sentiment_magnitude = db.Column(db.Float)
    sentiment_text = db.Column(db.String)
    sentiment_classification = db.Column(db.String)
    magnitude_classification = db.Column(db.String)
    collector_job_id = db.Column(db.String, db.ForeignKey("jobs.id"))
    analyzer_job_id = db.Column(db.String, db.ForeignKey("jobs.id"))

    collector_job = db.relationship("Job", foreign_keys=[collector_job_id], back_populates="collector_messages")
    analyzer_job = db.relationship("Job", foreign_keys=[analyzer_job_id], back_populates="analyzer_messages")