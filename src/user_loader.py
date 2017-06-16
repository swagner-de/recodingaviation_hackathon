from app import lm
from model import User

@lm.user_loader
def load_user(id):
    return User.objects.get(_id=id)._id
