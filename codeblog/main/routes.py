from flask import Blueprint, request, render_template

from codeblog.models import Post

main = Blueprint('main', __name__)



@main.route("/") #just a way to add additional functionality to existing functions
@main.route("/home") # another route for the same function
def root():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)



@main.route("/about")
def about():
    return render_template('about.html', title='About')
