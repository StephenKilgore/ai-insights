from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import MessageModel
from schemas import MessageSchema
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("messages", __name__, description="Operations on messages")


@blp.route("/api/message")
class MessageList(MethodView):
    @blp.response(200, MessageSchema(many=True))
    def get(self):
        return MessageModel.query.all()

@blp.route("/api/message/<string:message_id>")
class MessageList(MethodView):
    @blp.response(200, MessageSchema())
    def get(self, message_id):
        return MessageModel.query.get_or_404(message_id)
