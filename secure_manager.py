from werkzeug.security import generate_password_hash, \
     check_password_hash

def encrypt_val(s):
    return generate_password_hash(s)

def check_val(h,s):
    return check_password_hash(h,s)