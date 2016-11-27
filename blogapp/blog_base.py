from blogapp import app

from flask import Flask, flash, render_template, request


import logging




# app = Flask(__name__, instance_relative_config=True)
# app.config.from_object('config') # load config.py from root folder
# app.config.from_pyfile('config.py')  # load from instance folder
# COOKIE_SALT= app.config['COOKIE_SALT']

from cookie_manager import *
from db_manager import *
from forms_manager import *


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


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

        # User.login(user.name,user.password) # check user valid in db

        flash('Thanks for registering, %s' % name)

        user_id_hash=get_secure_val(name)

        return get_respect_with_cookie('/welcome',user_id=user_id_hash, PATH='/')

    else:
        page = render_template('signup.html', form=form)
        return page

@app.route('/login', methods=['GET', 'POST'])
def login():
    form =LoginForm(request.form)
    if (request.method == 'GET'):
        user_id_hash=get_cookie(request, 'user_id')
        if user_id_hash:
            user_id=get_decoded_val(user_id_hash)

            #if there is a valid cookie
            if user_id:
                flash('You already login %s' %user_id )
                return redirect('/')

        return render_template('login.html', form=form)

    elif(request.method=='POST' and form.validate()):
        name=form.username.data
        pwd=form.password.data

        user=get_this_user(name)
        if user:
            u=user[0]
            # print user
            # print u.name
            # print u.password
            if check_password_hash(u.password,pwd):
                name=u.name
                flash('Login Successfully, %s' % name)
                name_hash=get_secure_val(name)
                return get_respect_with_cookie('/welcome', user_id=name_hash, PATH='/')
    else:
        print ('wrong when login, no cookie')
        return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    user_hash=get_cookie(request, 'user_id')
    user_name=get_decoded_val(user_hash)
    if user_name:
        flash('you are logging out %s' % user_name)
        return get_respect_with_cookie('/signup', user_id='', PATH='')
    else:
        return 'you did not login'


@app.route('/welcome', methods=['GET'])
def welcome():
    name_hash=get_cookie(request, 'user_id')
    if name_hash:
        name=get_decoded_val(name_hash)

        print name
        return render_template('welcome.html', name=name)
    else:
        return redirect('/signup')
    # if name:
    #     return render_template('welcome.html', name=name)
    # else:
    #     return redirect('/signup')

@app.route('/test', methods=['GET', 'POST'])
def test():
    return str(get_cookie(request,'test'))


if __name__ == '__main__':
    app.run()