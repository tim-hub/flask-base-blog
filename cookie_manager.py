import random
import string
import hmac

from flask import redirect, make_response

# SALT=app.config['COOKIE_SALT']
SALT='slat' # for test

def get_respect_with_cookie(next_url, **kwargs):
    redirect_to_next_url = redirect(next_url)
    resp = make_response(redirect_to_next_url) # string/ template/ redirect
    for name, val in kwargs.items():

        resp.set_cookie(name, val)
    return resp

def get_cookie(req, name):
    # print name
    # print req.cookies.get(name)
    return  (req.cookies.get(name))
#
def get_secure_val(s):
    str=get_random_string(4)

    return "%s|%s|%s" %(str, s, hash_str(s))
#
def get_decoded_val(h):
    print h
    strs=h.split('|')
    print strs[0]
    val=strs[1]
    h=strs[2]
    # print val
    if (hash_str(val)==h):
        return val

def get_random_string(size=2):
    chars= string.ascii_uppercase + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))

def hash_str(s):
    ###Your code here
    return hmac.new(SALT, s).hexdigest()

