from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from db_manager import get_this_user

def validate_username(form, field):
    name = field.data
    # print (field.data)
    query = get_this_user(name)
    # print ('checking and got %s %s' % (query.count(), query.fetch(1)))
    if query.count(limit=2) >0:
        raise ValidationError("Someone already registered this username")

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
    username= StringField('Username', [validators.DataRequired()])
    password= PasswordField('Password', [validators.DataRequired()])