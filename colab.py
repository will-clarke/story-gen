# !pip install ctransformers ctransformers[cuda] sqlalchemy langchain

import datetime
import uuid
import re
import random

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

# from ctransformers import AutoModelForCausalLM

from langchain.llms import CTransformers


from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


model_name = "TheBloke/Llama-2-7B-Chat-GGML"

llm = CTransformers(model=model_name, gpu_layers=50)

# llm = AutoModelForCausalLM.from_pretrained(model_name, gpu_layers=50)

llm("AI is going to")

db_uri = "sqlite:///content/gdrive/ai/stories.db"
engine = create_engine(db_uri, echo=True)
session_factory = sessionmaker(bind=engine)
session = session_factory()

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


potential_genres = [
    "hisorical",
    "fantasy",
    "romantic",
    "suspense",
    "sci-fi",
    "noir",
    "adventure",
    "comedy",
    "mystery",
    "fantasy",
    "romance",
]
potential_tones = [
    "eerie",
    "suspense",
    "joyful",
    "celebration",
    "melancholic",
    "reflective",
    "funny",
    "comedy",
    "tense",
]


prompt = PromptTemplate.from_template(
    """
I want you to write an interesting and absorbing short story with the following genres: {genres}.

It should have the following tone: {tones}.

Make in interesting and fun and roughly maximum {length} words long.

Start with the title on the first line then the story on the next line.
"""
)


# llm = CTransformers(model=model_name, model_type="llama", client=None)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
)


def extract_title(text):
    lines = text.strip().split("\n")
    if len(lines) < 2:
        return "", text
    title = lines[0]
    story_text = "\n".join(lines[1:])
    title = title.strip()
    story_text = story_text.strip()
    title = title.replace("Title: ", "")
    title = title.replace("Example: ", "")
    return title, story_text


def process(genres, tones, length):
    f = prompt.format(genres=", ".join(genres), tones=", ".join(tones), length=length)
    out = chain.run(genres=genres, tones=tones, length=length)
    print(out)

    title, story_text = extract_title(out)
    if title == "":
        return

    categories = [StoryCategory(category_type="tones", category=t) for t in tones] + [
        StoryCategory(category_type="genres", category=g) for g in genres
    ]
    s = Story(
        title=title,
        text=story_text,
        prompt=f,
        categories=categories,
        model_name=model_name,
        length=length,
    )

    session.add(s)
    session.commit()


if __name__ == "__main__":
    for i in range(0, 100000):
        genres = [
            random.choice(potential_genres) for _ in range(0, random.randint(1, 3))
        ]
        genres = list(set(genres))
        tones = [random.choice(potential_tones) for _ in range(0, random.randint(1, 3))]
        tones = list(set(tones))
        length = random.choice(["10", "50", "100", "200", "500", "1000", "2000"])
        process(genres, tones, length)
