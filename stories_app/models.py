from stories_app.db import db


import datetime
import uuid
import re

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import desc, func


class Story(db.Model):
    __tablename__ = "stories"

    id: uuid.UUID = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: str = db.Column(db.String)
    text: str = db.Column(db.String)
    prompt: str = db.Column(db.String)
    length: int = db.Column(db.Integer)
    model_name: str = db.Column(db.String)
    updated_at: datetime.datetime = db.Column(
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

    def average_rating(self):
        return (
            db.session.query(func.avg(StoryRating.rating))
            .filter_by(story_id=self.id)
            .scalar()
        )

    @staticmethod
    def get_random():
        return Story.query.order_by(func.random()).first()

    @staticmethod
    def first():
        return Story.query.order_by("updated_at").first()

    @staticmethod
    def last():
        return Story.query.order_by(desc("updated_at")).first()

    @staticmethod
    def top_rated(limit: int = 100):
        return (
            db.session.query(Story)
            .join(StoryRating, StoryRating.story_id == Story.id)
            .group_by(Story.id)
            .order_by(db.func.avg(StoryRating.rating).desc())
            .limit(limit)
            .all()
        )


class StoryCategory(db.Model):
    __tablename__ = "story_categories"
    story_id: uuid.UUID = db.Column(
        UUID(as_uuid=True), db.ForeignKey("stories.id"), primary_key=True
    )

    # eg. tones
    category_type: str = db.Column(db.String, primary_key=True)
    # eg. funny
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
    updated_at: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.utcnow
    )

    def __repr__(self):
        return f"({self.rating_type}: {self.rating})\n"

    @staticmethod
    def get_random():
        return StoryRating.query.order_by(func.random()).first()

    @staticmethod
    def first():
        return StoryRating.query.order_by("updated_at").first()

    @staticmethod
    def last():
        return StoryRating.query.order_by(desc("updated_at")).first()


class DataReddit(db.Model):
    __tablename__ = "data_reddit"

    id: str = db.Column(db.String, primary_key=True)
    subreddit: str = db.Column(db.String)
    url: str = db.Column(db.String)
    title: str = db.Column(db.String)
    text: str = db.Column(db.String)
    score: int = db.Column(db.Integer)
    top_comment: str = db.Column(db.String, default="")
    updated_at: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.utcnow
    )
    created_at: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.utcnow
    )

    def __repr__(self):
        return f"DataReddit({self.title})\n"
