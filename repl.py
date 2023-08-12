from sqlalchemy.orm import Session
from models import Story, StoryCategory, StoryRating
import db


import code

engine = db.setup()
session = Session(engine)


all_stories = session.query(Story).all()
stories = session.query(Story).limit(10).all()
print(stories)
story = stories[0]
s = story

code.interact(local=globals()) 
