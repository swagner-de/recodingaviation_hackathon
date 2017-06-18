import requests
import json

def get_waittimes():
    uri = 'https://cph.novasa.com/json/security-times?apikey=MC8XuCJ0ofeYo3iLKsX39HoJsQ18GrGF'

    resp = requests.get(uri)
    resp_bdy = json.loads(resp.text)
    return resp_bdy.get('items', [])


def get_waittime_for_filters(to_pass):
    filters = get_waittimes()
    min = 0
    max = 0
    for f in filters:
        if f.get('name', '') in to_pass:
           min += f.get('minutes_between', {}).get('from', 0)
           max += f.get('minutes_between', {}).get('to', 0)
    return {'max_waiting': max, 'min_waiting': min}


def get_filters(origin, destination):
    from api.airports import eu_airports, us_airports
    if origin in eu_airports and destination in eu_airports:
        return []
    if origin in eu_airports and destination in us_airports:
        return ['paskontrolF', 'T2']
    if origin in eu_airports and destination not in eu_airports:
        return ['paskontrolF']
    if origin not in eu_airports and destination in eu_airports:
        return ['paskontrolF']
    if origin not in eu_airports and destination in us_airports:
        return ['T2']
    return []


if __name__ == '__main__':
    get_waittimes()
