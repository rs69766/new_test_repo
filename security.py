from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(email , password):
    user = UserModel.find_by_email(email) # get function can be applied to dict , it behaves same as getting the value from key
    if user and safe_str_cmp(user.password , password):
        return user

#identity is an default function provided by flask which will hold payload from which you can extract identity
def identity(payload):
    user_id = payload['identity']
    user = UserModel.find_by_id(user_id)
    return user
