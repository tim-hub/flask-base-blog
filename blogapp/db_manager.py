from google.appengine.ext import db
import string
import random
import time
# for user
class User(db.Model):
    name= db.StringProperty(required=True)
    # user_id=db.StringProperty() #random id is not a good idea
    password=db.StringProperty(required=True)
    email=db.EmailProperty(required=False)
    created=db.DateTimeProperty(auto_now=True)

def get_this_user(name):
    query = db.GqlQuery(' select *  from User where name = :name ', name=name)
    return query



# for posts
'''
This is google datastore model to store post
'''
class BlogPost(db.Model):
    belong_to=db.StringProperty(required=True)
    # post_id=db.StringProperty(required=True)

    subject= db.StringProperty(required=True)
    content=db.TextProperty(required=True)

    modified=db.DateTimeProperty(auto_now=True)
    created=db.DateTimeProperty(auto_now_add=True)

    # @classmethod
    # def query_post_by_title(cls, title):
    #     return BlogPost.all().filter('subject =', title).get()
    #
    # @classmethod
    # def query_post_by_id(cls, id):
    #     return db.GqlQuery("SELECT * from BlogPost WHERE post_id=:id", id=id)
    #     # return BlogPost.all().filter('post_id =', id).get()# index firstly
    #
    # @classmethod
    # def get_posts(cls):
    #     return db.GqlQuery("Select * from BlogPost Order By created DESC")  # maybe add limit 10 to gql
    #
    # @classmethod
    # def create_post_id(cls, title):
    #
    #     l=len(title)
    #     part_title=''
    #
    #     if l >= 4:
    #         part_title = title[-4:]
    #
    #     else:
    #         part_title=title[-l:]
    #
    #     part_time = time.strftime("%Y-%m-%d")
    #
    #     part_number = generate_random_number()
    #     return part_time + '-' + part_title + '-' + part_number


def query_post_by_id( id):
    return db.GqlQuery("SELECT * from BlogPost WHERE post_id=:id", id=id)

def query_post_by_key( k):
    return db.GqlQuery("SELECT * from BlogPost WHERE key_name=:k", id=k)

def generate_random_number(size=4):
    # create random string
    # chars=string.ascii_uppercase + string.ascii_lowercase
    # create random number
    chars=string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def create_post_id( title):
    l = len(title)
    part_title = title[-l:]
    if l >= 4:
        part_title = title[-4:]

    part_time = time.strftime("%Y-%m-%d")

    part_number = generate_random_number()
    return part_time + '-' + part_title + '-' + part_number

def get_posts():
    return db.GqlQuery("Select * from BlogPost Order By created DESC")  # maybe add limit 10 to gql