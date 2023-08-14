import flask_sqlalchemy as sqlalchemy
from models import Base

def setup() -> sqlalchemy.engine.Engine:
    # engine = sqlalchemy.create_engine("sqlite:///stories.db", echo=True)
    engine = sqlalchemy.create_engine("postgresql:///stories", echo=True)
    # Base.metadata.create_all(engine, checkfirst=True)

    return engine
