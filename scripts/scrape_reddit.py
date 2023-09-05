import praw
from util import get_password


reddit_read_only = praw.Reddit(
    client_id=get_password("justeat/reddit-api", r"client_id:\s*(\S+)"),
    client_secret=get_password("justeat/reddit-api", r"client_secret:\s*(\S+)"),
    user_agent="short-stories-will",
)


subreddit = reddit_read_only.subreddit("shortstories")

subreddit_top = subreddit.top()

for submission in subreddit_top:


print(reddit_read_only.auth.limits)
