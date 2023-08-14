from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# create the extension
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///stories"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

