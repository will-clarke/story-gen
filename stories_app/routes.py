import time
from typing import List, Tuple
from flask import render_template, request, url_for
from flask import Blueprint
from sqlalchemy import func, and_
from datetime import datetime
from sqlalchemy.orm import aliased

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
    per_page = min(per_page, 200)

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

        for category_name in category_list:
            category_alias = aliased(StoryCategory)
            story_query = story_query.join(category_alias, Story.categories).filter(
                category_alias.category == category_name
            )

    if ratings:

        # if ratings includes a -, assume it's a range
        if "-" in ratings:
            low, high = ratings.split("-")
            if low > high:
                low, high = high, low  # Swap values to ensure low is the smallest
            rating_list = [*range(int(low), int(high) + 1)]
        else:
            # Assuming ratings are passed as a list of integers separated by commas
            rating_list = [int(rating) for rating in ratings.split(",")]
        print("rating_list", rating_list)
        story_query = story_query.join(Story.ratings).filter(
            StoryRating.rating.in_(rating_list)
        )

    if title:
        story_query = story_query.filter(Story.title.ilike(f"%{title}%"))

    if length:
        story_query = story_query.filter(Story.length == length)

    if page and per_page:
        story_query = story_query.limit(per_page).offset((page - 1) * per_page)

    stories = story_query.all()

    # FIXME: This is in memory and could probs be done in the db
    param_name = "categories"
    unique_categories = set()
    for story in stories:
        for category in story.categories:
            unique_categories.add(category.category)
    categories: List[
        Tuple[str, str, bool]
    ] = (
        []
    )  # a list of "categories" - which involves a name, the url, and whether this category has already been applied
    for category in list(unique_categories):
        category_is_applied_already = False
        existing_query_params = request.args.copy()
        if param_name in existing_query_params:

            # remove the category if it exists and it gets clicked on
            if category in existing_query_params[param_name]:
                category_is_applied_already = True
                existing_query_params[param_name] = (
                    existing_query_params[param_name]
                    .replace(category, "")
                    .replace(",,", ",")
                    .strip(",")
                )
            else:
                # otherwise just add it
                existing_query_params[param_name] = (
                    existing_query_params[param_name] + "," + category
                )
        else:
            # If it doesn't exist, add it with the new value
            existing_query_params[param_name] = category
        url = url_for("stories.stories", **existing_query_params)
        categories.append((category, url, category_is_applied_already))

        # Generate the updated URL with the modified query parameters
        # updated_url = url_for(request.endpoint, **existing_query_params)

        # if "categories" in existing_query_params:
        #     url = url.replace(existing_query_params["categories"], category)

    categories = sorted(categories, key=lambda x: x[0])  # sort by name first
    categories = sorted(
        categories, key=lambda x: x[2], reverse=True
    )  # sort by whether the category is applied already
    return render_template("stories.html", stories=stories, categories=categories)


@bp.route("/random-story")
def random_story():
    requests_total.inc()
    s = Story.get_random()
    return render_template("story.html", story=s)


@bp.route("/metrics")
def metrics():
    return generate_latest(REGISTRY)
