import sqlalchemy
import models.story as story

def setup() -> sqlalchemy.engine.Engine:
    # engine = sqlalchemy.create_engine("sqlite:///stories.db", echo=True)
    engine = sqlalchemy.create_engine("postgresql:///stories", echo=True)
    story.Base.metadata.create_all(engine, checkfirst=True)

    return engine
