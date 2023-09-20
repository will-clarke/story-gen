# !pip install ctransformers ctransformers[cuda] sqlalchemy

import datetime
import uuid
import re

from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
    declarative_base,
    sessionmaker,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    desc,
    func,
    create_engine,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from ctransformers import AutoModelForCausalLM

llm = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-7B-GGML", gpu_layers=50)

llm("AI is going to")

engine = create_engine("sqlite:///stories.db", echo=True)
Session = sessionmaker(bind=engine)

# Create a session instance
session = Session()

Base = declarative_base()


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    prompt: Mapped[str] = mapped_column(String)
    length: Mapped[int] = mapped_column(Integer)
    model_name: Mapped[str] = mapped_column(String)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    categories = relationship(
        "StoryCategory", back_populates="story", cascade="all, delete-orphan"
    )
    ratings = relationship(
        "StoryRating", back_populates="story", cascade="all, delete-orphan"
    )

    def __repr__(self):
        title_long_enough: bool = len(self.title) >= 40
        text_preview = self.title[:40] if title_long_enough else self.title
        text_preview.replace("\n", " ")
        text_preview = re.sub(r"\s+", " ", text_preview)
        return f"Story({text_preview})\n"

    def average_rating(self):
        return (
            session.query(func.avg(StoryRating.rating))
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
    def top_rated(limit=100):
        return (
            session.query(Story)
            .join(StoryRating, StoryRating.story_id == Story.id)
            .group_by(Story.id)
            .order_by(func.avg(StoryRating.rating).desc())
            .limit(limit)
            .all()
        )


class StoryCategory(Base):
    __tablename__ = "story_categories"
    story_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stories.id"), primary_key=True
    )

    # eg. tones
    category_type: Mapped[str] = mapped_column(String, primary_key=True)
    # eg. funny
    category: Mapped[str] = mapped_column(String, primary_key=True)
    story = relationship("Story", back_populates="categories")

    def __repr__(self):
        return f"({self.category_type}{self.category})\n"


class StoryRating(Base):
    __tablename__ = "story_ratings"
    story_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stories.id"), primary_key=True
    )

    rating_type: Mapped[str] = mapped_column(String, primary_key=True)
    rating: Mapped[int] = mapped_column(Integer, primary_key=True)
    prompt: Mapped[str] = mapped_column(String)
    model_name: Mapped[str] = mapped_column(String)
    model_output: Mapped[str] = mapped_column(String, default="")
    story = relationship("Story", back_populates="ratings")
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    def __repr__(self):
        return f"({self.rating_type}{self.rating})\n"

    @staticmethod
    def get_random():
        return StoryRating.query.order_by(func.random()).first()

    @staticmethod
    def first():
        return StoryRating.query.order_by("updated_at").first()

    @staticmethod
    def last():
        return StoryRating.query.order_by(desc("updated_at")).first()
