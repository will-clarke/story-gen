from app import app
# from flask import render_template, request, redirect, url_for


# from . import db
from .models.models import Story # StoryCategory, StoryRating


print("hey")


@app.route('/')
def index():
    print("yoooooooooooooooooo")
    s = Story.query.all()
    print("s: ", s)
    return "heyy" + str(len(s)) + "stories in the database"

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128))
#     username = db.Column(db.String(128))

# @app.route("/users")
# def user_list():
#     users = db.session.execute(db.select(User).order_by(User.username)).scalars()
#     return render_template("user/list.html", users=users)

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
