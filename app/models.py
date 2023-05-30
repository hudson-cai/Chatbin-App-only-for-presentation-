# reference: chapter 5 of Miguel Grinberg's mega tutorial
# reference: chapter 6 of Miguel Grinberg's mega tutorial
# This is to create an MD5 hash of the email address, which we will use as the avatar image URL.
from hashlib import md5
# This is to get the current date and time in UTC.
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):  # tells Python how to print objects of this class
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # avatar() method returns the URL of the user's avatar image, scaled to the requested size in pixels
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
     # Add a relationship with the Message model
     #consulted ChatGPT for this since I always failed to keep the message on the chatboard
    messages = db.relationship('Message', backref='author', lazy='dynamic')

# login.user_loader is a decorator that registers the function as a user loader function. It is used to reload the user object from the user ID stored in the session.


@login.user_loader
def load_user(id):
    return User.query.get(int(id))  # get the user id from the database

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'user_id': self.user_id,
            'username': self.author.username
        }
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):  # tells Python how to print objects of this class
        return '<Post {}>'.format(self.body)


