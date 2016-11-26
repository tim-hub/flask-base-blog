from google.appengine.ext import db
from werkzeug.security import generate_password_hash, \
     check_password_hash
'''
This is google datastore model to store post
'''
class BlogPost(db.Model):
    subject= db.StringProperty(required=True)
    content=db.TextProperty(required=True)
    modified=db.DateTimeProperty(auto_now=True)
    created=db.DateTimeProperty(auto_now_add=True)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name= db.StringProperty(required=True)
    # user_id=db.StringProperty() #random id is not a good idea
    password=db.StringProperty(required=True)
    email=db.EmailProperty(required=False)
    created=db.DateTimeProperty(auto_now=True)

    @classmethod # it can be called like User.by_id
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = generate_password_hash(pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and check_password_hash( u.pw_hash,pw):
            return u

def get_this_user(name):
    query = db.GqlQuery(' select *  from User where name = :name ', name=name)
    return query

def get_posts():
    return db.GqlQuery("Select * from BlogPost Order By created DESC") #maybe add limit 10 to gql

def encrypt_val(s):
    return generate_password_hash(s)

def check_val(h,s):
    return check_password_hash(h,s)