from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import MetricSchema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from models import MessageModel, JobModel

blp = Blueprint("metrics", __name__, description="Operations on metrics")

@blp.route("/api/metrics")
class Metric(MethodView):
    @blp.response(200, MetricSchema())
    def get(self):
        total_messages = db.session.query(func.count(MessageModel.id)).scalar()
        total_jobs = db.session.query(func.count(JobModel.id)).scalar()
        jobs_with_failed_rows = db.session.query(func.count(JobModel.id)).filter(JobModel.rows_failed > 0).scalar()
        avg_messages_per_job = total_messages / total_jobs
        avg_job_runtime_in_ms = db.session.query(func.avg(JobModel.runtime)).scalar()
        last_job_run_date = db.session.query(func.max(JobModel.job_end_date)).scalar()

        return {
            "total_messages": total_messages,
            "total_jobs": total_jobs,
            "jobs_with_failed_rows": jobs_with_failed_rows,
            "avg_messages_per_job": avg_messages_per_job,
            "avg_job_runtime_in_ms": avg_job_runtime_in_ms,
            "last_job_run_date": last_job_run_date
        }