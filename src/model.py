from flask_mongoengine import MongoEngine, DoesNotExist
from werkzeug.security import check_password_hash, generate_password_hash


db = MongoEngine()

class User(db.Document):
    email = db.StringField(max_length=120)
    password = db.StringField(max_length=120)

    def clean(self):
        self.password = generate_password_hash(self.password)


    @staticmethod
    def check_pw(email, password):
        try:
            u = User.objects.get(email=email)
            return check_password_hash(u.password, password)
        except DoesNotExist:
            return False

class Leg(db.EmbeddedDocument):
    departure_airport = db.StringField(max_length=3)
    arrival_airport = db.StringField(max_length=3)
    carrier = db.StringField(max_length=2)
    flight_no = db.StringField(max_length=4)
    departure_date = db.DateTimeField()


class Trip(db.Document):
    user = db.ReferenceField(User)
    legs = db.ListField(db.EmbeddedDocumentField(Leg))
