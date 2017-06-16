import requests
import json
import re

def get_oper_flight_status(flight_no: str) -> dict:
    app_id = 'a20fe5d6'
    app_key = '82c6a07405642ea8a61e808a1afba7e1'
    headers = {'app_key': app_key,
               'app_id': app_id,
               'Accept': 'application/json',
               'ResourceVersion': 'v1'}

    uri = 'https://api-acc.schiphol.nl/operational-flight/flights?flightNumber={code}'
    resp = requests.get(uri.format(
        code=re.search('\\d+', flight_no).group(0)
    ), headers=headers)
    if resp.status_code == 200:
        resp_bdy = json.loads(resp.text)
        flights = resp_bdy.get('flights', [])
        for flight in flights:
            flight.get('flightName', '') == flight_no
            return flight


if __name__ == '__main__':
    status = get_oper_flight_status('KL606')
    from pprint import pprint
    pprint(status)
