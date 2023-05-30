from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify # for get_message
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, MessageForm
from app.models import User, Message
from pytz import timezone






# @before_request decorator from Flask register the decorated function to be executed right before the view function
# This enbales inserting code that we want to execute before any view function in the application

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    # current_user variable comes from Flask-Login
    if current_user.is_authenticated:  # if the user is already logged in, redirect to the index page
        return redirect(url_for('chat'))
    form = LoginForm()  # create an instance of the LoginForm class
    # validate_on_submit() method returns True when the user submits the form (POST request) and all the data is valid
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        # login_user() function comes from Flask-Login
        # This function will register the user as logged in
        # This means that any future pages the user navigates to will have the current_user variable set to that user.
        login_user(user, remember=form.remember_me.data)
        # request.args attribute exposes the contents of the query string in a friendly dictionary format
        next_page = request.args.get('next')
        # url_parse() is to make sure that the URL is relative, which ensures that the redirect stays within the same site as the application
        # netloc is the network location part of the URL
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('chat')
        return redirect(next_page)  # redirect to the index page
    return render_template('index.html', title='Sign In', form=form)


@app.route('/chat', methods=['GET', 'POST'])
# if not logged in, @login_required decorator will intercept the request and respond with a redirect to /login
# but it will add a query string argument to this URL, making the complete redirect URL /login?next=/index.
@login_required
def chat():
    if request.method == 'POST':
        content = request.form.get('message')
        if content:
            message = Message(content=content, author=current_user)
            db.session.add(message)
            db.session.commit()
            return redirect(url_for('chat'))

    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return render_template('chat.html', messages=messages)








# Aim:
# The application only redirects when the URL is relative, which ensures that the redirect stays within the same site as the application.

# Three conditions:
# If the login URL does not have a next argument, then the user is redirected to the index page.
# If the login URL includes a next argument that is set to a relative path (or in other words, a URL without the domain portion), then the user is redirected to that URL.
# If the login URL includes a next argument that is set to a full URL that includes a domain name, then the user is redirected to the index page. (This is to make the application more secure)


@app.route('/logout')
def logout():
    logout_user()  # logout_user() function comes from Flask-Login
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # if the user is already logged in, redirect to the index page
        return redirect(url_for('chat'))
    form = RegistrationForm()  # create an instance of the RegistrationForm class
    if form.validate_on_submit():  # validate the form
        user = User(username=form.username.data,
                    email=form.email.data)  # create a new user
        user.set_password(form.password.data)  # set the password
        db.session.add(user)  # add the user to the database
        db.session.commit()  # commit the changes to the database
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))  # redirect to the login page
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    # If validate_on_submit() returns True, copy the data from the form into the user object and then write the object to the database in a separate db.session.commit() call.
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/get-messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    serialized_messages = [message.serialize() for message in messages]
    return jsonify(messages=serialized_messages)



@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    content = data.get('content')
    perth_tz = timezone('Australia/Perth')
    perth_time = datetime.now(perth_tz).replace(microsecond=0)
    username = data.get('username')

    # Use "ChatBot" as the username for auto replies
    if username == "ChatBot":
        chatbot_user = User.query.filter_by(username="ChatBot").first()
        message = Message(content=content, timestamp=perth_time, author=chatbot_user)
    else:
        message = Message(content=content, timestamp=perth_time, author=current_user)

    db.session.add(message)
    db.session.commit()

    return jsonify(message=message.serialize())




# Route for cleaning all history
@app.route('/clean-history', methods=['POST'])
def clean_history():
    Message.query.delete()
    db.session.commit()
    return jsonify(message='Chat history has been cleaned')






