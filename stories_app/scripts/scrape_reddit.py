import praw
from stories_app.scripts.util import get_password
from stories_app.app import create_app

from stories_app.models import DataReddit
from stories_app.db import db

reddit_read_only = praw.Reddit(
    client_id=get_password("justeat/reddit-api", r"client_id:\s*(\S+)"),
    client_secret=get_password("justeat/reddit-api", r"client_secret:\s*(\S+)"),
    user_agent="short-stories-will",
)


app = create_app()
app.app_context().push()
session = db.session
subreddit = reddit_read_only.subreddit("shortstories")

subreddit_top = subreddit.top()

for submission in subreddit_top:

    if submission.comments:
        top_comment = submission.comments[0].body
    else:
        top_comment = ""

    r = DataReddit(
        url=submission.url,
        title=submission.title,
        text=submission.selftext,
        score=submission.score,
        top_comment=top_comment,
    )

    session.add(r)
    session.commit()
    print(submission.title)


print(reddit_read_only.auth.limits)
