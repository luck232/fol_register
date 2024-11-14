import secrets
import string
import re
import bcrypt
import hashlib

def unique_code(long:int = 50) -> str:
    chars = string.ascii_letters + string.digits 
    code = ''.join(secrets.choice(chars) for _ in range(long))
    return code

def is_code(text: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9]{50}$', text))

def is_email(text: str) -> bool:
    return bool(re.match(r'^(?=.{1,253}$)([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$', text))

def is_password(text: str) -> bool:
    return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', text))

def hashpass(password:str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8') 

def to_sha(shatoken: str) -> str:
    hash_obj = hashlib.sha256()
    hash_obj.update(shatoken.encode('utf-8'))
    return hash_obj.hexdigest()