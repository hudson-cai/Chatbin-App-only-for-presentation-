# Description: This file contains the system test for the application.
# Usage: First, you need to modify a line in the __init__.py
# app.config.from_object('config.TestingConfig')
# Then, run the following code in the termianl:
# python3 -m tests.system_test
import unittest, os, time
from datetime import datetime
from app import app, db
from app.models import User, Message
from selenium import webdriver
basedir = os.path.abspath(os.path.dirname(__file__))

class SystemTest(unittest.TestCase):
    driver = None
  
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir,'geckodriver'))

        if not self.driver:
            self.skipTest('Web browser not available')
        else:
            db.init_app(app)
            db.create_all()
            u1 = User(username='test',email='test@example.com')
            u2 = User(username='case',email='case@example.com')
            message1 = Message(content='Hello',user_id=u1.id,timestamp=datetime.utcnow())
            message2 = Message(content='Hi',user_id=u2.id,timestamp=datetime.utcnow())
            db.session.add(u1)
            db.session.add(u2)
            db.session.add(message1)
            db.session.add(message2)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get('http://127.0.0.1:5000/')

    def tearDown(self):

        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.query(Message).delete()
            db.session.commit()
            db.session.remove()

    def test_register(self):
        u = User.query.get('1') # get user with id 1，which is test
        self.assertEqual(u.username,'test',msg='user exists in db')
        self.driver.get('http://127.0.0.1:5000/register')
        self.driver.implicitly_wait(5)
        username_field = self.driver.find_element_by_id('username')
        username_field.send_keys('test')
        email = self.driver.find_element_by_id('email')
        email.send_keys('test@example.com')
        new_pin = self.driver.find_element_by_id('password')
        new_pin.send_keys('0000')
        new_pin2 = self.driver.find_element_by_id('password2')
        new_pin2.send_keys('0000')
        time.sleep(1)
        self.driver.implicitly_wait(5)
        submit = self.driver.find_element_by_id('submit')
        submit.click()
        #check login success
        self.driver.implicitly_wait(5)
        time.sleep(1)
        logout = self.driver.find_element_by_partial_link_text('Logout')
        self.assertEqual(logout.get_attribute('innerHTML'), 'Logout test', msg='Logged in')

if __name__=='__main__':
  unittest.main(verbosity=2)
    
      