from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import MetricSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("metrics", __name__, description="Operations on metrics")

@blp.route("/api/metrics")
class Metric(MethodView):
    @blp.response(200, MetricSchema())
    def get(self, job_id):
        return "test"