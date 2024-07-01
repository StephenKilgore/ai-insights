from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import message
from schemas import MessageSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("messages", __name__, description="Operations on messages")