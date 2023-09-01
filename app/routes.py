# from . import app

from flask import render_template

from flask import Blueprint

bp = Blueprint("main", __name__)


# from . import db
from .models import Story  # StoryCategory, StoryRating


@bp.route("/")
def index():
    # print("yoooooooooooooooooo")
    # s = Story.query.all()
    # print("s: ", s)
    return render_template("index.html")


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/story/<int:id>")
def story(id):
    story = Story.query.filter_by(id=id).first()
    return render_template("story.html", story=story)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128))
#     username = db.Column(db.String(128))


@bp.route("/random-story")
def random_story():
    s = Story.get_random()
    return render_template("story.html", story=s)


@bp.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)


# @app.route("/users/create", methods=["GET", "POST"])
# def user_create():
#     if request.method == "POST":
#         user = User(
#             username=request.form["username"],
#             email=request.form["email"],
#         )
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for("user_detail", id=user.id))

#     return render_template("user/create.html")

# @app.route("/user/<int:id>")
# def user_detail(id):
#     user = db.get_or_404(User, id)
#     return render_template("user/detail.html", user=user)

# @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
# def user_delete(id):
#     user = db.get_or_404(User, id)

#     if request.method == "POST":
#         db.session.delete(user)
#         db.session.commit()
#         return redirect(url_for("user_list"))

#     return render_template("user/delete.html", user=user)
