from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError, TextField, TextAreaField
from werkzeug.security import generate_password_hash, \
     check_password_hash
from db_manager import get_this_user

def validate_username(form, field):
    name = field.data
    # print (field.data)
    query = get_this_user(name)
    # print ('checking and got %s %s' % (query.count(), query.fetch(1)))
    if query.count(limit=2) >0:
        raise ValidationError("Someone already registered this username")


def registered_username(form, field):
    name = field.data
    # print (field.data)
    query = get_this_user(name)
    # print ('checking and got %s %s' % (query.count(), query.fetch(1)))
    if query.count(limit=2) !=1:
        # current_user=None
        raise ValidationError("Username is not registered")


def right_password(form, field):
    if form.username.errors ==None:

        current_user = get_this_user(form.username.data)

        pwd_hash=current_user[0].password

        if not check_password_hash(pwd_hash, field.data):
            raise ValidationError("wrong pwd")


class SignUpForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=20), validate_username])

    password = PasswordField('New Password', [
        validators.Length(min=3, max=20),
        validators.DataRequired()])
    verify = PasswordField('Repeat Password',
        [validators.EqualTo('password', message='Passwords must match')
    ])
    email = StringField('Email Address',[validators.Email(), validators.Optional()])


    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
class LoginForm(Form):
    username= StringField('Username', [validators.DataRequired(), registered_username])
    password= PasswordField('Password', [validators.DataRequired(),right_password])

class NewPostForm(Form):
    subject=StringField('Subject', [validators.DataRequired()])
    content=TextAreaField('Content', [validators.DataRequired()])