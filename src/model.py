from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash

db = MongoEngine()

class User(db.Document):
    email = db.StringField(max_length=120)
    password = db.StringField(max_length=120)

    def clean(self):
        # clean will be called when you call .save()
        # You can do whatever you'd like to clean data before save
        self.password = generate_password_hash(self.password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_pw(username, password):
        u = User.objects.get(username=username)
        return check_password_hash(u.password_hash, password)
