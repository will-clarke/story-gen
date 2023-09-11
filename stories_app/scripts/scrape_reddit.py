from praw import Reddit
import praw.models
import time
from datetime import datetime

from stories_app.scripts.util import get_password
from stories_app.app import create_app
from stories_app.models import DataReddit
from stories_app.db import db
from sqlalchemy import desc

from sqlalchemy.exc import IntegrityError  # Import the IntegrityError exception

reddit = Reddit(
    client_id=get_password(
        "REDDIT_CLIENT_ID", "justeat/reddit-api", r"client_id:\s*(\S+)"
    ),
    client_secret=get_password(
        "REDDIT_CLIENT_SECRET", "justeat/reddit-api", r"client_secret:\s*(\S+)"
    ),
    user_agent="short-stories-will",
)

app = create_app()
app.app_context().push()
session = db.session
subreddit = reddit.subreddit("shortstories")
start_time = time.time()


def format_time(timestamp):
    # Convert the timestamp to a datetime object
    rfc3339_datetime = datetime.fromtimestamp(timestamp).astimezone()

    # Format the datetime object as RFC3339
    rfc3339_string = rfc3339_datetime.isoformat()

    return rfc3339_string


# last datareddit id
# last = session.query(DataReddit).order_by(desc(DataReddit.updated_at)).first()
# last_id = None
# if last:
#     last_id = "t3_" + last.id

# subreddit_top = subreddit.top(time_filter="all", limit=None, params={"after": last_id})


def save_submission(submission: praw.models.Submission):
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

    print(submission.id + " -- " + submission.title)


subreddits = [
    subreddit.top(limit=None, time_filter="week"),
    subreddit.top(limit=None, time_filter="year"),
    subreddit.top(limit=None, time_filter="month"),
    subreddit.hot(limit=None),
    subreddit.hot(limit=None),
    subreddit.new(limit=None),
    subreddit.rising(limit=None),
    subreddit.controversial(limit=None),
    subreddit.gilded(limit=None),
]

count = 0
for subreddit in subreddits:
    for submission in subreddit:
        count += 1
        time_now = time.time()
        total_duration = time_now - start_time
        save_submission(submission)
        print("count: ", count,"duration:", total_duration, "time_now:", format_time(time.time()), "reddit_limits:",  reddit.auth.limits)
        time.sleep(4)
