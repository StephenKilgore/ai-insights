from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import MetricSchema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from model import message, job

blp = Blueprint("metrics", __name__, description="Operations on metrics")

@blp.route("/api/metrics")
class Metric(MethodView):
    @blp.response(200, MetricSchema())
    def get(self):
        return get_metrics()

    def get_metrics(self):
        total_messages = db.session.query(func.count(message.id)).scalar()
        total_jobs = db.session.query(func.count(job.id)).scalar()
        jobs_with_failed_rows = db.session.query(func.count(job.id)).filter(job.rows_failed > 0).scalar()
        avg_messages_per_job = total_messages / total_jobs
        avg_job_runtime = db.session.query(func.avg(job.runtime)).scalar()
        last_job_run_date = db.session.query(func.max(job.job_end_date)).scalar()
