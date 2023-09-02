from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# from .models import Story, StoryCategory, StoryRating


import datetime
import uuid
import re

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///stories"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Story(db.Model):
    __tablename__ = "stories"

    id: uuid.UUID = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: str = db.Column(db.String)
    text: str = db.Column(db.String)
    prompt: str = db.Column(db.String)
    length: int = db.Column(db.Integer)
    model_name: str = db.Column(db.String)
    update_at: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.utcnow
    )
    created_at: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.utcnow
    )
    categories = db.relationship(
        "StoryCategory", back_populates="story", cascade="all, delete-orphan"
    )
    ratings = db.relationship(
        "StoryRating", back_populates="story", cascade="all, delete-orphan"
    )
    # : List["StoryRating"]

    def __repr__(self):
        title_long_enough = self.title and len(self.title) >= 40
        text_preview = self.title[:40] if title_long_enough else self.title
        text_preview.replace("\n", " ")
        text_preview = re.sub(r"\s+", " ", text_preview)
        return f"Story({text_preview})\n"

    @staticmethod
    def get_random():
        return Story.query.order_by(func.random()).first()


class StoryCategory(db.Model):
    __tablename__ = "story_categories"
    story_id: uuid.UUID = db.Column(
        UUID(as_uuid=True), db.ForeignKey("stories.id"), primary_key=True
    )

    category_type: str = db.Column(db.String, primary_key=True)
    category: str = db.Column(db.String, primary_key=True)
    story = db.relationship("Story", back_populates="categories")

    def __repr__(self):
        return f"({self.category_type}: {self.category})\n"


class StoryRating(db.Model):
    __tablename__ = "story_ratings"
    story_id: uuid.UUID = db.Column(
        UUID(as_uuid=True), db.ForeignKey("stories.id"), primary_key=True
    )

    rating_type: str = db.Column(db.String, primary_key=True)
    rating: int = db.Column(db.Integer, primary_key=True)
    prompt: str = db.Column(db.String)
    model_name: str = db.Column(db.String)
    model_output: str = db.Column(db.String, default="")
    story = db.relationship("Story", back_populates="ratings")

    def __repr__(self):
        return f"({self.rating_type}: {self.rating})\n"


# from . import app

from flask import render_template


@app.route("/")
def index():
    # print("yoooooooooooooooooo")
    # s = Story.query.all()
    # print("s: ", s)
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/story/<int:id>")
def story(id):
    story = Story.query.filter_by(id=id).first()
    return render_template("story.html", story=story)


@app.route("/random-story")
def random_story():
    s = Story.get_random()
    return render_template("story.html", story=s)
