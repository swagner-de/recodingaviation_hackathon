from model import Leg, Trip
from datetime import datetime

leg_1 = Leg(departure_airport='SFO', arrival_airport='AMS',
            carrier='KL', flight_no='606', departure_date=datetime.strptime('2017-06-16', '%Y-%m-%d'))
leg_2 = Leg(departure_airport='AMS', arrival_airport='FRA',
            carrier='KL', flight_no='1765', departure_date=datetime.strptime('2017-06-17', '%Y-%m-%d'))

leg_3 = Leg(departure_airport='LAX', arrival_airport='AMS',
                carrier='KL', flight_no='602', departure_date=datetime.strptime('2017-06-22', '%Y-%m-%d'))
leg_4 = Leg(departure_airport='AMS', arrival_airport='TXL',
                carrier='KL', flight_no='1823', departure_date=datetime.strptime('2017-06-23', '%Y-%m-%d'))

leg_5 = Leg(departure_airport='YYZ', arrival_airport='AMS',
                carrier='KL', flight_no='0692', departure_date=datetime.strptime('2017-06-27', '%Y-%m-%d'))
leg_6 = Leg(departure_airport='AMS', arrival_airport='CPH',
                carrier='KL', flight_no='1125', departure_date=datetime.strptime('2017-06-28', '%Y-%m-%d'))

leg_7 = Leg(departure_airport='SIN', arrival_airport='AMS',
                carrier='KL', flight_no='0836', departure_date=datetime.strptime('2017-06-21', '%Y-%m-%d'))
leg_8 = Leg(departure_airport='AMS', arrival_airport='MAD',
                carrier='KL', flight_no='1701', departure_date=datetime.strptime('2017-06-16', '%Y-%m-%d'))

leg_9 = Leg(departure_airport='EDI', arrival_airport='AMS',
                carrier='KL', flight_no='1276', departure_date=datetime.strptime('2017-06-26', '%Y-%m-%d'))
leg_10 = Leg(departure_airport='AMS', arrival_airport='HAJ',
                carrier='KL', flight_no='1903', departure_date=datetime.strptime('2017-06-26', '%Y-%m-%d'))

leg_11 = Leg(departure_airport='SFO', arrival_airport='AMS',
                carrier='KL', flight_no='606', departure_date=datetime.strptime('2017-06-16', '%Y-%m-%d'))
leg_12 = Leg(departure_airport='AMS', arrival_airport='FRA',
                carrier='KL', flight_no='1765', departure_date=datetime.strptime('2017-06-16', '%Y-%m-%d'))

codes = {
    'AAAAA1': [leg_1, leg_2],
    'AAAAA2': [leg_3, leg_4],
    'AAAAA3': [leg_5, leg_6],
    'AAAAA4': [leg_7, leg_8],
    'AAAAA5': [leg_9, leg_10],
    'AAAAA6': [leg_11, leg_12]
}


def get_trip(pnr, user):
    return Trip(legs=codes.get(pnr, None), user=user)
