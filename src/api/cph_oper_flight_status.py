import requests
import json

def get_oper_flight_status(flight_no: str) -> dict:

    uri = 'https://cph.novasa.com/json/flights?apikey=MC8XuCJ0ofeYo3iLKsX39HoJsQ18GrGF'

    resp = requests.get(uri)
    resp_bdy = json.loads(resp.text)
    resp = None

    for flight in resp_bdy.get('items', []):
        if flight.get('flight_number', '') == flight_no:
            return flight

if __name__ == '__main__':
    d = get_oper_flight_status('AF1750')
    from pprint import pprint
    pprint(d)
