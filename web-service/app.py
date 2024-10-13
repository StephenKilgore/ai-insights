from flask import Flask, render_template
from flask_smorest import Api
from resources.job import blp as JobBlueprint
from resources.message import blp as MessageBlueprint
from resources.metric import blp as MetricBlueprint

from db import db
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    load_dotenv()
    DATABASE_URI = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "AI Insights REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api = Api(app)

    @app.route('/')
    def index():
        return render_template('index.html')


    with app.app_context():
        db.create_all()

    api.register_blueprint(JobBlueprint)
    api.register_blueprint(MessageBlueprint)
    api.register_blueprint(MetricBlueprint)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
