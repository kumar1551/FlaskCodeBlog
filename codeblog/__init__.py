from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_mail import Mail
# import os

from codeblog.config import Config

# init extension outside and pass app inside function
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()




# init app
# app = Flask(__name__)
# #config using object

# app.config.from_object(Config)


#config for using forms
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# config for databases
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
# db = SQLAlchemy(app)

# for hashing password
# bcrypt = Bcrypt(app)

# for implementing login
# login_manager = LoginManager(app)
# login_manager.login_view = 'login' # telling the login about login route
# login_manager.login_message_category = 'info' # msg category for login message

# for sending mails
# app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER') # set before using
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS') # set before using
# mail = Mail(app)

# from codeblog import routes

# # import blueprints objects

# from codeblog.users.routes import users
# from codeblog.posts.routes import posts
# from codeblog.main.routes import main

# app.register_blueprint(users)
# app.register_blueprint(posts)
# app.register_blueprint(main)


# function for app creation

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class) #config using object

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from codeblog.users.routes import users
    from codeblog.posts.routes import posts
    from codeblog.main.routes import main
    from codeblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app # replace everywhere import app is used with flask current_app