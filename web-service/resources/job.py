from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..db import db
from ..models import job
from ..schemas import JobSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("jobs", __name__, description="Operations on jobs")