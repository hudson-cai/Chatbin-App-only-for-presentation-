from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

# Define the login and registration forms as subclasses of FlaskForm


class LoginForm(FlaskForm):
    # DataRequired validator simply checks that the field is not submitted empty
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember_me field is a BooleanField, which represents a checkbox that the user can select when logging in
    remember_me = BooleanField('Remember Me')
    # submit field is a SubmitField, which represents a submit button
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # EqualTo validator checks that the values entered in both fields match
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # A validation error is triggered by raising an exception of type ValidationError
    # The message included as the argument in the exception will be the message that will be displayed next to the field for the user to see.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# EditProfileForm class is similar to the RegistrationForm class, except that it does not have a password field


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # TextAreaField is a multi-line text field
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

# for message in routes.py
class MessageForm(FlaskForm):
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
