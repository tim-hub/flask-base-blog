from flask import Flask, flash, render_template, request
# from wtforms.validators import DataRequired
from flask_wtf.csrf import CsrfProtect

import logging

from cookie_manager import *
from secure_manager import *
from db_manager import *
from forms_manager import *

# init app
# csrf = CsrfProtect()
app = Flask(__name__)
# csrf.init_app(app)

# this is for flash message
app.secret_key = 'some_secret'


@app.route('/')
def home():
    posts= get_posts()
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
    form = SignUpForm(request.form)
    if (request.method == 'POST' and form.validate()):
        name=form.username.data
        password=form.verify.data
        pwd_encrypted=encrypt_val(password)
        email=form.email.data
        user=User(name=name,password=pwd_encrypted)
        if email:
            user.email=email
        user.put()

        flash('Thanks for registering, %s' % form.username.data)

        # set cookie
        name_cookie=str(form.username.data)
        return respect_with_cookie('/welcome',username=name_cookie)

    else:
        page = render_template('signup.html', form=form)
        return page

@app.route('/login', methods=['GET', 'POST'])
def login():
    form =LoginForm(request.form)
    if(request.method=='POST' and form.validate()):
        name=form.username.data
        pwd=form.password.data

        user=get_this_user(name)
        if user:
            u=user[0]
            # print user
            # print u.name
            # print u.password
            if check_password_hash(u.password,pwd):
                flash('Login Successfully, %s' % form.username.data)
                return respect_with_cookie('/welcome', username=u.name)
            else:
                flash('Wrong Logining' )
                return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)
@app.route('/logout', methods=['GET'])
def logout():
    if get_cookie(request, 'username'):
        return respect_with_cookie('/', username='')
    else:
        return 'you did not login'


@app.route('/welcome', methods=['GET'])
def welcome():
    name=get_cookie(request, 'username')

    print name
    if name:
        return render_template('welcome.html', name=name)
    else:
        return redirect('/signup')


if __name__ == '__main__':
    app.run()

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500