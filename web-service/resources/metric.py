from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import MetricSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("metrics", __name__, description="Operations on metrics")

@blp.route("/api/metrics")
class Metric(MethodView):
    @blp.response(200, MetricSchema())
    def get(self):
        return {
            "successful_jobs": 1,
            "failed_jobs": 0,
            "total_processed_tweets": 20,
            "last_job_status": "complete"
        }