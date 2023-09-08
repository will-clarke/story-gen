import time
from flask import render_template, request
from flask import Blueprint
from sqlalchemy import func
from datetime import datetime

from stories_app.models import Story, StoryCategory, StoryRating

from prometheus_client import Counter, Histogram, generate_latest, REGISTRY

routes = []

requests_total = Counter("stories_requests_total", "Total HTTP Requests")
request_duration = Histogram(
    "stories_request_duration_seconds", "Request latency in seconds"
)


bp = Blueprint("stories", __name__)


@bp.route("/")
def index():
    start_time = time.time()
    requests_total.inc()
    top_rated = Story.top_rated()[:20]  # TODO: limit!
    end_time = time.time()
    request_duration.observe(end_time - start_time)
    return render_template("index.html", top_rated=top_rated)


@bp.route("/about")
def about():
    requests_total.inc()
    return render_template("about.html")


@bp.route("/story/<uuid:id>")
def story(id):
    requests_total.inc()
    story = Story.query.filter_by(id=id).first()
    return render_template("story.html", story=story)


@bp.route("/stories")
def stories():
    page = request.args.get("page")
    per_page = request.args.get("per_page")
    model_name = request.args.get("model_name")
    created_at = request.args.get("created_at")
    updated_at = request.args.get("updated_at")
    categories = request.args.get("categories")
    ratings = request.args.get("ratings")
    title = request.args.get("title")
    length = request.args.get("length")

    if page:
        page = int(page)
    else:
        page = 1

    if per_page:
        per_page = int(per_page)
    else:
        per_page = 10

    # story = Story.query.paginate(page, per_page)
    story_query = Story.query
    if model_name:
        story_query = story_query.filter(Story.model_name == model_name)

    if created_at:
        created_at_date = datetime.strptime(created_at, "%Y-%m-%d")
        story_query = story_query.filter(func.date(Story.created_at) == created_at_date)

    if updated_at:
        updated_at_date = datetime.strptime(updated_at, "%Y-%m-%d")
        story_query = story_query.filter(func.date(Story.updated_at) == updated_at_date)

    if categories:
        # Assuming categories are passed as a list of strings separated by commas
        category_list = categories.split(",")
        story_query = story_query.join(Story.categories).filter(
            StoryCategory.name.in_(category_list)
        )

    if ratings:
        # Assuming ratings are passed as a list of integers separated by commas
        rating_list = [int(rating) for rating in ratings.split(",")]
        story_query = story_query.join(Story.ratings).filter(
            StoryRating.value.in_(rating_list)
        )

    if title:
        story_query = story_query.filter(Story.title.ilike(f"%{title}%"))

    if length:
        story_query = story_query.filter(Story.length == length)

    if page and per_page:
        story_query = story_query.limit(per_page).offset((page - 1) * per_page)

    stories = story_query.all()

    return render_template("stories.html", stories=stories)


@bp.route("/random-story")
def random_story():
    requests_total.inc()
    s = Story.get_random()
    return render_template("story.html", story=s)


@bp.route("/metrics")
def metrics():
    return generate_latest(REGISTRY)
