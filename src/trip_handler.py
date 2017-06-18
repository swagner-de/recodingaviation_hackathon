import api
import model

def get_current_legs(user):
    return user.get_current_legs()

def get_connection(legs):
    earliest = None
    con = None
    for i in range(len(legs)):
        leg = legs[i]
        legs_remaining = legs[i+1:]
        for r in legs_remaining:
            if leg.arrival_airport == r.departure_airport:
                if not earliest or earliest > r.departure_date:
                    con = r
                    earliest = r.departure_date
            if con:
                return {'inbound': leg, 'outbound': con}

def get_flight_oper_info(connection):
    connection['inbound'].get_operational_info()
    connection['outbound'].get_operational_info()
    return connection

def get_transfer_info_ams(connection):
    connection['transfer'] = {}
    if connection['inbound'].gate != None and connection['outbound'].gate != None:
        from api.ams_wayfinding import get_directions_from_gates
        connection['transfer'] = get_directions_from_gates(arr_gate=connection['inbound'].gate, dep_gate=connection['outbound'].gate)
        from api.ams_wait_time import get_waittime_for_filters
        transfer = connection['transfer']
        wait_time = get_waittime_for_filters(transfer['filters_on_route'])
        transfer['min_waiting_time'] = wait_time['min_waiting']
        transfer['max_waiting_time'] = wait_time['max_waiting']

def get_transfer_info_cph(connection):
    connection['transfer'] = {}
    from api.cph_wait_time import get_waittime_for_filters, get_filters
    transfer = connection['transfer']
    transfer['filters_on_route'] = get_filters(connection['inbound'].departure_airport, connection['outbound'].arrival_airport)
    wait_time = get_waittime_for_filters(transfer['filters_on_route'])
    transfer['min_waiting_time'] = wait_time['min_waiting']
    transfer['max_waiting_time'] = wait_time['max_waiting']

def calc_times(connection):
    additional_time = connection['outbound'].delay - connection['inbound'].delay
    planned_time = int((connection['outbound'].departure_date - connection['inbound'].arrival_date).total_seconds() / 60)
    tta = planned_time + additional_time
    connection['transfer']['tta'] = tta
    etg_min = connection['transfer']['min_waiting_time'] + connection['transfer'].get('total_ped_time', 0)
    etg_max = connection['transfer']['max_waiting_time'] + connection['transfer'].get('total_ped_time', 0)
    connection['transfer']['etg_min'] = etg_min
    connection['transfer']['etg_max'] = etg_max
    connection['transfer']['spare_time_min'] = tta-etg_max
    connection['transfer']['spare_time_max'] = tta-etg_min

def get_que_recommendation(connection):
    transfer = connection['transfer']
    from analysis.waittime_EHAM import get_best_timeslot
    spare_time_min = transfer.get('spare_time_min', False)
    if spare_time_min:
        later, improvement = get_best_timeslot(connection['inbound'].arrival_date, spare_time_min)
        transfer['recommendation'] = {
            'later' : later,
            'improvement': str(improvement*100) * '\%' if not 1 else 'no queueing expected'
        }

def get_current_connect_info(user):
    current_legs = user.get_current_legs()
    connection = get_connection(current_legs)
    get_flight_oper_info(connection)
    if connection['inbound'].arrival_airport == 'AMS':
        get_transfer_info_ams(connection)
        calc_times(connection)
        try:
            get_que_recommendation(connection)
        except KeyError:
            pass
    elif connection['inbound'].arrival_airport == 'CPH':
        get_transfer_info_cph(connection)
        calc_times(connection)
    return connection

def get_bags_info(user):
    from api.sita_bag_journey import get_bag_journey
    return get_bag_journey('akter', 'nazma', 'ZZ', 'LHR', '0650', '2015-10-14')

