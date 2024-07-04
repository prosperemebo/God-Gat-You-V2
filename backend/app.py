import os

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_cors import CORS
from dotenv import load_dotenv

from db import db, database_url
from controllers import WallpaperBlueprint


def create_app(db_url=None):
    load_dotenv()

    app = Flask(__name__)

    CORS(
        app,
        origins=[
            "http://localhost:3000",
        ],
    )

    app.config["API_TITLE"] = "God Gat You API"
    app.config["API_VERSION"] = "v1"

    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY") or "ggy_secret"

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    api = Api(app)

    api.register_blueprint(WallpaperBlueprint)

    return app
