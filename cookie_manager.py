from flask import redirect, make_response

def respect_with_cookie(next_url, **kwargs):
    redirect_to_next_url = redirect(next_url)
    resp = make_response(redirect_to_next_url)
    for name, value in kwargs.items():
        resp.set_cookie(name,value)
    return resp

def get_cookie():
    pass