import api
import model

def get_current_legs(user):
    return user.get_current_legs()

def get_connection(leg, legs_remaining):
    earliest = None
    con = None
    for r in legs_remaining:
        if leg.arrival_airport == r.departure_airport:
            if not earliest or earliest > r.departure_date:
                con = r
                earliest = r.departure_date
    return {'inbound': leg, 'outbound': con} if con else None


def get_current_connect_info(user):
    current_legs = user.get_current_legs()
    try:
        connection = get_connection(current_legs[0], current_legs[1:])
    except IndexError:
        return None
    return connection
