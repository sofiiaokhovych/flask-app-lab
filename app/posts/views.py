from flask import request, render_template, redirect, url_for, flash, session
from app import db
from . import post_bp
from .models import Post
from .forms import PostForm


@post_bp.route("")
@post_bp.route("/")
def all_posts():
    stmt = (
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts, title="Posts")

@post_bp.route("/create", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post()
        form.populate_obj(new_post)
        new_post.posted = form.publish_date.data
        new_post.author = session.get("username", "Anonymous")
        db.session.add(new_post)
        db.session.commit()
        flash("Post added successfully", "success")
        return redirect(url_for("posts.all_posts"))
    elif request.method == "POST":
        flash("Enter the correct data in the form!", "danger")
    return render_template("add_post.html", form=form, title="Create a New Post")

@post_bp.route("/<int:id>")
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", post=post, title=post.title)

@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    if request.method == "GET":
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
        post.posted = form.publish_date.data
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template("add_post.html", form=form, title="Edit Post")

@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "danger")
        return redirect(url_for("posts.all_posts"))

    return render_template("delete_confirm.html", post=post, title="Delete Post")