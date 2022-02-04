from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


from datetime import datetime

from codeblog import db, login_manager

from flask_login import UserMixin

from flask import current_app

@login_manager.user_loader # reloading the user from the user_id stored in the session.
def load_user(user_id):
    return User.query.get(int(user_id))


# the login extension will except your user model
# to have certain attributes and methods It's going to except
# four to be excact,  
# 1. is_authenicated - return true if provided valid credentials
# 2. is_active - 
# 3. is_anonymous - 
# 4. get_id
# This is so common that the extension provides us with a 
# simple class that to inherit from that will add all these
# required attributes and method
# extend from UserMixin

class User(db.Model, UserMixin): # for session handling in the background
    
    # User model automatically has this table name set to lower case user

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    # one to many relation with Post as 1 user can have many posts
    posts = db.relationship('Post', backref='author', lazy=True)
    # it isn't actualy a column itself. It runs an additional query on the posts table
    # that grabs any post from that user.
    # backref -> not an actual column in Post model but it allows us to use
    # that to access the user who created that post
    # post.author will give an entire user object
    

    def get_reset_token(self, expires_sec=1800):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        
        return serializer.dumps({"user_id": self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(current_app.config['SECRET_KEY'])

        try:
            user_id = serializer.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)
    
    
    # how to print the object
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"