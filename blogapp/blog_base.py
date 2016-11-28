from blogapp import app

from flask import Flask, flash, render_template, request



from cookie_manager import *
from db_manager import *
from forms_manager import *


import logging


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


@app.route('/')
def home():
    posts= get_posts()
    if who_logined(request):
        return render_template('home.html', posts=posts, logined=True)
    else:
        return render_template('home.html', posts=posts, logined=False)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    form=NewPostForm(request.form)
    if request.method=='POST' and form.validate():
        subject=form.subject.data
        content=form.content.data
        user=who_logined(request)
        key_name=create_post_id(subject)

        if subject and content:
            blog_post=BlogPost( key_name=key_name, subject=subject,content=content,belong_to=user)
            blog_post.put()
            id = (blog_post.key().name())
            if id :
                return redirect('/post/%s' %id)
            else:
                print ("something wrong, there is no post id")
        else:
            return render_template("new_post.html", error="Both subject and content are needed")

    else:

        return render_template("new_post.html")
#
# @app.route('/post/<post_id>/')
# def show_post(post_id):
#
#     print ("show post, id is %s" % post_id)
#     blog_post = query_post_by_id((post_id))
#     return render_template('post.html', subject=blog_post.subject, content=blog_post.content)
#
#     # post_query=query_post_by_id(post_id)
#     # if post_query.count()>0:
#     #     blog_post=post_query[0]
#     #
#     #     return render_template('post.html', subject=blog_post.subject, content=blog_post.content)


@app.route('/post/<key_name>/')
def show_post(key_name):
    print ("show post, id is %s" % key_name)
    # blog_post = query_post_by_key((key_name))
    k=db.Key.from_path('BlogPost', key_name )
    # more on https://cloud.google.com/appengine/docs/python/datastore/entities

    blog_post=db.get(k)
    return render_template('post.html',subject=blog_post.subject, content=blog_post.content)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)
    if (request.method == 'POST' and form.validate()):
        name=form.username.data
        password=form.verify.data
        pwd_encrypted=generate_password_hash(password)
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
        user_id=who_logined(request)
        if user_id:
            flash('You already login %s ' %user_id )
            return redirect('/')
        return render_template('login.html', form=form)

    elif(request.method=='POST' and form.validate()):
        name=form.username.data
        # pwd=form.password.data
        #
        # user=get_this_user(name)
        # if user:
        #     u=user[0]
        #     # print user
        #     # print u.name
        #     # print u.password
        #     if check_password_hash(u.password,pwd):
        # name=u.name
        flash('Login Successfully, %s' % name)
        name_hash=get_secure_val(name)
        return get_respect_with_cookie('/welcome', user_id=name_hash, PATH='/')

    print ('wrong when login, no cookie')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    user_name=who_logined(request)
    if user_name:
        flash('you are logging out %s  ' % user_name)
        return get_respect_with_cookie('/signup', user_id='', PATH='')
    else:
        return 'you did not login'


@app.route('/welcome', methods=['GET'])
def welcome():
    name=who_logined(request)
    if name:
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