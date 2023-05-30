# reference: chapter 4: Database of Miguel Grinberg's mega tutorial
# reference: chapter 5: User Logins of Miguel Grinberg's mega tutorial
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config





# reference: chapter 5 of Miguel Grinberg's mega tutorial
# login is an instance of the class LoginManager
# The 'login' value below is the function (or endpoint) name for the login view

app = Flask(__name__, static_folder='static')
# app.config.from_object(Config)
app.config.from_object('config.TestingConfig')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models




@login.user_loader
def load_user(id):
    from app.models import User  # Import the User model here to avoid circular imports
    return User.query.get(int(id))