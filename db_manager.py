from google.appengine.ext import db

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

def get_this_user(name):
    query = db.GqlQuery(' select *  from User where name = :name ', name=name)
    return query

def get_posts():
    return db.GqlQuery("Select * from BlogPost Order By created DESC") #maybe add limit 10 to gql