# Usage: First, you need to modify a line in the __init__.py
# app.config.from_object('config.TestingConfig')
# Then, run the following code in the termianl:
# python3 -m unittest tests.unit_test

import unittest, os
from app import app, db
from app.models import User, Message

class UserModelCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['TESTING'] = True
        self.app = app.test_client() #create a virtual test environment
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
    
    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))
    
    def test_message(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        message1 = Message(content='Hello',user_id = u1.id)
        message2 = Message(content='Hi',user_id = u2.id)
        db.session.add(message1)
        db.session.add(message2)
        db.session.commit()
        self.assertEqual(message1.user_id, u1.id)
        self.assertEqual(message2.user_id, u2.id)
        self.assertEqual(message1.content, 'Hello')
        self.assertEqual(message2.content, 'Hi')


if __name__ == '__main__':
    unittest.main(verbosity=2)