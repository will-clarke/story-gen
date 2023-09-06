import time
from flask import render_template
from flask import Blueprint

from stories_app.models import Story


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


@bp.route("/random-story")
def random_story():
    requests_total.inc()
    s = Story.get_random()
    return render_template("story.html", story=s)


@bp.route("/metrics")
def metrics():
    return generate_latest(REGISTRY)
