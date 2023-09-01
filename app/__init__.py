from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///stories"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes
