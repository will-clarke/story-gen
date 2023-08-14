from sqlalchemy.orm import Session
from models import Story, StoryCategory, StoryRating
import db


import code

engine = db.setup()
session = Session(engine)


all_stories = session.query(Story).all()
stories = session.query(Story).limit(10).all()
# empty_title_stories = session.query(Story).filter(Story.title == '').all()
# for i in empty_title_stories:
#     session.delete(i)
# session.commit()
print(stories)
story = stories[0]
s = story


a = session.query(StoryRating).order_by(StoryRating.rating.desc()).all()

code.interact(local=globals()) 

