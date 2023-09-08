from flask import Flask

from flask_migrate import Migrate


def create_app():
    from stories_app.routes import bp
    from stories_app.db import db

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///stories"

    # set PGPASSWORD !!!
    # app.config[
    #     "SQLALCHEMY_DATABASE_URI"
    # ] = "postgresql://will@161.35.40.10:5432/stories"
    db.init_app(app)
    _ = Migrate(app, db)

    app.register_blueprint(bp)

    return app
