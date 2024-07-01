from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import JobModel
from schemas import JobSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("jobs", __name__, description="Operations on jobs")

@blp.route("/job")
class JobList(MethodView):
    @blp.response(200, JobSchema(many=True))
    def get(self):
        return JobModel.query.all()

@blp.route("/job/<string:job_id>")
class Job(MethodView):
    @blp.response(200, JobSchema())
    def get(self, job_id):
        return JobModel.query.get_or_404(job_id)