import praw
import time

from stories_app.scripts.util import get_password
from stories_app.app import create_app
from stories_app.models import DataReddit
from stories_app.db import db

from sqlalchemy.exc import IntegrityError  # Import the IntegrityError exception

reddit_read_only = praw.Reddit(
    client_id=get_password("justeat/reddit-api", r"client_id:\s*(\S+)"),
    client_secret=get_password("justeat/reddit-api", r"client_secret:\s*(\S+)"),
    user_agent="short-stories-will",
)


app = create_app()
app.app_context().push()
session = db.session
subreddit = reddit_read_only.subreddit("shortstories")

number_of_records_in_db = session.query(DataReddit).count()
subreddit_top = subreddit.top(limit=None, after=number_of_records_in_db)

data = []

for submission in subreddit_top:
    if submission.comments:
        top_comment = submission.comments[0].body
    else:
        top_comment = ""

    r = DataReddit(
        id=submission.id,
        url=submission.url,
        title=submission.title,
        text=submission.selftext,
        score=submission.score,
        top_comment=top_comment,
    )

    try:
        session.add(r)
        session.commit()
    except IntegrityError as e:
        session.rollback()  # Rollback the transaction to undo the attempted addition
        print(f"IntegrityError: {e}")

    time.sleep(8)

    print(submission.id + " -- " + submission.title)


print(reddit_read_only.auth.limits)
