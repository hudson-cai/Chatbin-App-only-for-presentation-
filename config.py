# reference: chapter 4 of Miguel Grinberg's mega tutorial
import os

# basedir is the path of the directory where the config.py file resides
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # os.environ.get('SECRET_KEY') is used to get the value of the SECRET_KEY environment variable, if it is set, otherwise the string '2023cits5505project2' is used as a default value.
    SECRET_KEY = os.environ.get('SECRET_KEY') or '2023cits5505project2'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Turn off update message for every change in the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tests/test.db')