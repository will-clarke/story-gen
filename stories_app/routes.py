from flask import render_template
from flask import Blueprint

from stories_app.models import Story

routes = []


bp = Blueprint("stories", __name__)


@bp.route("/")
def index():
    top_rated = Story.top_rated()[:20]
    return render_template("index.html", top_rated=top_rated)


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/story/<uuid:id>")
def story(id):
    story = Story.query.filter_by(id=id).first()
    return render_template("story.html", story=story)


@bp.route("/random-story")
def random_story():
    s = Story.get_random()
    return render_template("story.html", story=s)
