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

def get_flight_oper_info(connection):
    connection['inbound'].get_operational_info()
    connection['outbound'].get_operational_info()
    return connection

def get_transfer_info(connection):
    from ams_wayfinding import get_directions_from_gates
    connection['transfer'] = get_directions_from_gates(arr_gate=connection['inbound'].gate, dep_gate=connection['outbound'].gate)

def get_current_connect_info(user):
    current_legs = user.get_current_legs()
    try:
        connection = get_connection(current_legs[0], current_legs[1:])
    except IndexError:
        return None
    from pprint import pprint
    pprint(connection)
    get_flight_oper_info(connection)
    get_transfer_info(connection)
    return connection

