import praw
import time
from pmaw import PushshiftAPI

api = PushshiftAPI()

from stories_app.scripts.util import get_password
from stories_app.app import create_app
from stories_app.models import DataReddit
from stories_app.db import db
from sqlalchemy import desc

from sqlalchemy.exc import IntegrityError  # Import the IntegrityError exception

reddit = praw.Reddit(
    client_id=get_password("justeat/reddit-api", r"client_id:\s*(\S+)"),
    client_secret=get_password("justeat/reddit-api", r"client_secret:\s*(\S+)"),
    user_agent="short-stories-will",
)


api_praw = PushshiftAPI(praw=reddit)

comments = api_praw.search_comments(
    q="quantum", subreddit="science", limit=100, until=1629990795
)


app = create_app()
app.app_context().push()
session = db.session
subreddit = reddit.subreddit("shortstories")


# last datareddit id
last = session.query(DataReddit).order_by(desc(DataReddit.updated_at)).first()
last_id = None
if last:
    last_id = "t3_" + last.id

subreddit_top = subreddit.top(time_filter="all", limit=None, params={"after": last_id})

data = []

for submission in subreddit_top:
    if submission.comments:
        top_comment = submission.comments[0].body
    else:
        top_comment = ""

    r = DataReddit(
        id=submission.id,
        subreddit=submission.subreddit.display_name,
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


print(reddit.auth.limits)
