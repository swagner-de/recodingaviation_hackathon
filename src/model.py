from flask_mongoengine import MongoEngine, DoesNotExist
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta


db = MongoEngine()

class User(db.Document):
    email = db.StringField(max_length=120)
    last_name = db.StringField(max_length=120)
    first_name = db.StringField(max_length=120)
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
    arrival_date = db.DateTimeField()
    delay = db.IntField()
    gate = db.StringField(max_length=20)

    @staticmethod
    def get_current_legs(user):
        high_border = datetime.now() + timedelta(hours=36)
        low_border = datetime.now() - timedelta(hours=36)
        ts = Trip.objects(user=user)
        res = []
        for t in ts:
            for l in t.legs:
                if l.departure_date <= high_border and l.departure_date >= low_border:
                    res.append(l)
        return sorted(res, key=lambda x: x.departure_date, reverse=False)


    def _get_oper_info_ams(self):
        from api import ams_oper_flight_status
        import dateutil
        oper_info = ams_oper_flight_status.get_oper_flight_status(self.carrier+self.flight_no)
        estimated_ = oper_info['estimatedInBlockTime']
        scheduled_ = oper_info['scheduledInBlockTime']
        if estimated_ == None and scheduled_ == None:
            estimated_ = oper_info['estimatedOffBlockTime']
            scheduled_ = oper_info['scheduledOffBlockTime']
        try:
            estimated = dateutil.parser.parse(estimated_)
            scheduled = dateutil.parser.parse(scheduled_)
            self.arrival_date = scheduled
            self.delay = int((estimated - scheduled).total_seconds() / 60)
        except TypeError:
            self.delay = 0
        try:
            self.gate = oper_info['gate']['current']
        except TypeError:
            self.gate = None
        try:
            self.departure_date = dateutil.parser.parse(oper_info['scheduledOffBlockTime'])
        except TypeError:
            pass

    def _get_oper_info_cph(self):
        from api.cph_oper_flight_status import get_oper_flight_status
        oper_info = get_oper_flight_status(self.carrier+self.flight_no)
        estimated_ = oper_info.get('estimated', None)
        scheduled_ = oper_info.get('scheduled', None)
        try:
            scheduled = datetime.fromtimestamp(int(scheduled_))
            estimated = datetime.fromtimestamp(int(estimated_))
            self.delay = int((estimated - scheduled).total_seconds() / 60)
            if self.departure_airport == 'CPH':
                # inbound
                self.departure_date = scheduled
            self.arrival_date = scheduled
        except TypeError:
            self.delay = 0
        self.gate = oper_info.get('gate_number', None)



    def get_operational_info(self):
        if self.departure_airport == 'AMS' \
            or self.arrival_airport == 'AMS':
            self._get_oper_info_ams()
        if self.departure_airport == 'CPH' \
            or self.arrival_airport == 'CPH':
            self._get_oper_info_cph()

class Trip(db.Document):
    user = db.ReferenceField(User)
    pnr = db.StringField(max_length=6)
    legs = db.EmbeddedDocumentListField(Leg)

    @staticmethod
    def get_current_trips(user):
        high_border = datetime.now() + timedelta(hours=36)
        low_border = datetime.now() - timedelta(hours=36)
        return [t.legs.filter(departure_date__lte=high_border, departure_date__gte=low_border) for t in Trip.objects(user=user)]
