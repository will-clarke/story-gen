from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# from .models import Story, StoryCategory, StoryRating


def register_routes(application):
    from .routes import bp

    application.register_blueprint(bp)


application = Flask(__name__)

application.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///stories"

db = SQLAlchemy(application)
migrate = Migrate(application, db)
