import requests
import json

def get_bag_journey(pax_last_name:str, pax_first_name:str, airline:str, dep_airport: str, flight_no: str, dep_date:str) -> dict:
    api_key = '2ad03198b7287e91a44d213e696bbb4b'
    headers = {'api_key': api_key,
               'Accept': 'application/json'}

    uri = 'https://bagjourney.sita.aero/baggage/bagsforflight/v1.0/airport_code/{airport}/arr_dep_indicator/D/airline_code/{airline}/flight_no/{flight_no}/dep_flight_date/{dep_date}'
    resp = requests.get(uri.format(
        airport=dep_airport,
        airline=airline,
        flight_no=flight_no,
        dep_date=dep_date
    ), headers=headers)
    if resp.status_code == 200:
        resp_bdy = json.loads(resp.text)
        try:
            bags = resp_bdy['bags']
            result = {}
            for bag in bags:
                if bag.get('passenger_last_name') == pax_last_name.upper():
                    if bag.get('passenger_first_name') == pax_first_name.upper():
                        result[bag.get('bagtag')] = bag.get('loading_status')
        except KeyError:
            return
        return result

if __name__ == '__main__':
    k = get_bag_journey('akter', 'nazma', 'ZZ', 'LHR', '0650', '2015-10-14')
    from pprint import pprint
    pprint(k)
