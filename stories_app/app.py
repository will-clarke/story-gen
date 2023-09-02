from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def create_app():
    from stories_app.routes import bp
    from stories_app.db import db

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///stories"
    db.init_app(app)
    _ = Migrate(app, db)

    app.register_blueprint(bp)

    return app


# from . import app