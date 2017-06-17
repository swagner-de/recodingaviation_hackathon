from flask_mongoengine import MongoEngine, DoesNotExist
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


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

    def get_current_legs(self):
        return Leg.get_current_legs(self)



class Leg(db.EmbeddedDocument):
    departure_airport = db.StringField(max_length=3)
    arrival_airport = db.StringField(max_length=3)
    carrier = db.StringField(max_length=2)
    flight_no = db.StringField(max_length=4)
    departure_date = db.DateTimeField()

    @staticmethod
    def get_current_legs(user):
        low_border = datetime.strptime('2017-06-16', '%Y-%m-%d')
        high_border = datetime.strptime('2017-06-30', '%Y-%m-%d')
        ts = Trip.objects(user=user)
        res = []
        for t in ts:
            for l in t.legs:
                if l.departure_date <= high_border and l.departure_date >= low_border:
                    res.append(l)
        return sorted(res, key=lambda x: x.departure_date, reverse=True)



class Trip(db.Document):
    user = db.ReferenceField(User)
    pnr = db.StringField(max_length=6)
    legs = db.EmbeddedDocumentListField(Leg)

    @staticmethod
    def get_current_trips(user):
        low_border = datetime.strptime('2017-06-16', '%Y-%m-%d')
        high_border = datetime.strptime('2017-06-30', '%Y-%m-%d')
        return [t.legs.filter(departure_date__lte=high_border, departure_date__gte=low_border) for t in Trip.objects(user=user)]
