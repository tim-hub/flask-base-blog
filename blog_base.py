from flask import Flask, render_template, request, redirect
import logging
from google.appengine.ext import db

class BlogPost(db.Model):
	subject= db.StringProperty(required=True)
	content=db.TextProperty(required=True)
	created=db.DateTimeProperty(auto_now_add=True)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    if request.method=='POST':
        subject=request.form('subject')
        content=request.form('content')

        if subject and content:
            post=BlogPost(subject=subject,content=content)
            post.put()
            return redirect('/')
        else:
            pass
        return render_template("new_post.html")
    else:
        return render_template("new_post.html")



if __name__ == '__main__':
    app.run()

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500