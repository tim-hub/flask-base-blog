from flask import redirect, make_response
from secure_manager import *

def get_respect_with_cookie(next_url, **kwargs):
    redirect_to_next_url = redirect(next_url)
    resp = make_response(redirect_to_next_url) # strin, template redirect
    for name, val in kwargs.items():
        encrypted_val=get_secure_val(val)
        resp.set_cookie(name,encrypted_val)
    return resp



def get_cookie(req, name):
    # print name
    # print req.cookies.get(name)
    return  get_decoded_val(req.cookies.get(name))

def get_secure_val(s):
    return "sha512|%s|%s" %(s, encrypt_val(s))

def get_decoded_val(h):
    strs=h.split('|')
    val=strs[1]
    h=strs[2]
    # print val
    if (check_val(h,val)):
        return val
    
