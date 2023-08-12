import datetime
import uuid

from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
    pass

class Story(Base):
    __tablename__ = 'stories'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text: Mapped[str] = mapped_column(String)
    prompt: Mapped[str] = mapped_column(String)
    length: Mapped[int] = mapped_column(Integer)
    model_name: Mapped[str] = mapped_column(String)
    update_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    categories: Mapped[List["StoryCategory"]] = relationship("StoryCategory", back_populates="story")

class StoryCategory(Base):
    __tablename__ = 'story_categories'
    story_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('stories.id'), primary_key=True)

    category_type: Mapped[str] = mapped_column(String, primary_key=True)
    category: Mapped[str] = mapped_column(String, primary_key=True)
    story: Mapped["Story"] = relationship("Story", back_populates="categories")
