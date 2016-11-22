from flask import Flask, flash, render_template, request, redirect, make_response
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
# from wtforms.validators import DataRequired
from flask_wtf.csrf import CsrfProtect

import logging
from google.appengine.ext import db

# init app
# csrf = CsrfProtect()
app = Flask(__name__)
# csrf.init_app(app)

# this is for flash message
app.secret_key = 'some_secret'

'''
This is google datastore model to store post
'''
class BlogPost(db.Model):
    subject= db.StringProperty(required=True)
    content=db.TextProperty(required=True)
    modified=db.DateTimeProperty(auto_now=True)
    created=db.DateTimeProperty(auto_now_add=True)
class User(db.Model):
    name= db.StringProperty(required=True)
    password=db.StringProperty(required=True)
    email=db.EmailProperty(required=False)
    created=db.DateTimeProperty(auto_now=True)

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=20)])

    password = PasswordField('New Password', [
        validators.Length(min=3, max=20),
        validators.DataRequired()])
    verify = PasswordField('Repeat Password',
        [validators.EqualTo('password', message='Passwords must match')
    ])
    email = StringField('Email Address',[validators.Email(), validators.Optional()])
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

def encrypt_val(s):
    return generate_password_hash(s)

def check_val(h,s):
    return check_password_hash(h,s)

@app.route('/')
def home():
    posts=db.GqlQuery("Select * from BlogPost Order By created DESC") #maybe add limit 10 to gql
    return render_template('home.html', posts=posts)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    if request.method=='POST':
        subject=request.form['subject']
        content=request.form['content']

        if subject and content:
            blog_post=BlogPost(subject=subject,content=content)
            blog_post.put()
            id = (blog_post.key().id())
            if id :
                return redirect('/post/%s' %id)
            else:
                print ("something wrong, there is no post id")
        else:
            return render_template("new_post.html", error="Both subject and content are needed")

    else:
        return render_template("new_post.html")

@app.route('/post/<post_id>/')
def show_post(post_id):
    print ("show post, id is %s" %post_id)
    blog_post=BlogPost.get_by_id(long(post_id))
    return render_template('post.html', subject=blog_post.subject, content=blog_post.content)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if (request.method == 'POST' and form.validate()):
        flash('Thanks for registering, %s' % form.username.data)

        name_cookie=str(form.username.data)
        redirect_to_welcome= redirect('/welcome')
        resp=make_response(redirect_to_welcome)
        resp.set_cookie('username',name_cookie)
        return resp
    else:
        page = render_template('signup.html', form=form)

        return page

@app.route('/welcome', methods=['GET'])
def welcome():
    name=request.cookies.get('username')
    return "welcome %s" % name


if __name__ == '__main__':
    app.run()



'''
this is only for test
'''
@app.route('/test-cookie', methods=['GET', 'POST'])
def test_cookie():
    if request.method=='POST':
        pass
    else:
        visit_times = request.cookies.get('visits','0')
        if visit_times.isdigit():
            visit_times = int(visit_times) + 1
        else:
            visit_times=0

        if visit_times>500:
            resp = make_response(render_template('space.html', str='it is good'))
            resp.set_cookie('visits', str(visit_times))
        else:
            resp = make_response(render_template('space.html', str='you visit %s times' %visit_times))
            resp.set_cookie('visits', str(visit_times))

        return resp

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500