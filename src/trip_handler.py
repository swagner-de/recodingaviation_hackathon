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
    connection['transfer'] = {}
    if connection['inbound'].gate != None and connection['outbound'].gate != None:
        from api.ams_wayfinding import get_directions_from_gates
        connection['transfer'] = get_directions_from_gates(arr_gate=connection['inbound'].gate, dep_gate=connection['outbound'].gate)
        from api.ams_wait_time import get_waittime_for_filters
        wait_time = get_waittime_for_filters(connection['transfer']['filters_on_route'])
        transfer = connection['transfer']
        transfer['min_waiting_time'] = wait_time['min_waiting']
        transfer['max_waiting_time'] = wait_time['max_waiting']

def calc_times(connection):
    additional_time = connection['outbound'].delay - connection['inbound'].delay
    planned_time = int((connection['outbound'].departure_date - connection['inbound'].arrival_date).total_seconds() / 60)
    tta = planned_time + additional_time
    connection['transfer']['tta'] = tta
    try:
        etg_min = connection['transfer']['min_waiting_time'] + connection['transfer']['total_ped_time']
        etg_max = connection['transfer']['max_waiting_time'] + connection['transfer']['total_ped_time']
        connection['transfer']['etg_min'] = etg_min
        connection['transfer']['etg_max'] = etg_max
        connection['transfer']['spare_time_min'] = tta-etg_max
        connection['transfer']['spare_time_max'] = tta-etg_min
    except KeyError:
        pass

def get_current_connect_info(user):
    current_legs = user.get_current_legs()
    try:
        connection = get_connection(current_legs[0], current_legs[1:])
    except IndexError:
        return None
    get_flight_oper_info(connection)
    get_transfer_info(connection)
    calc_times(connection)
    return connection

