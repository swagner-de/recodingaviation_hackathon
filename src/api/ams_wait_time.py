""" Retrieves Waittime Information from Schiphol Airport`"""
from pprint import pprint
from api.util import filter_dict
import json
import requests

APP_ID = 'f92b2b96'
APP_KEY = '770d0a55a98fe27c2954e3eb118a06b4'
URL = 'https://api-acc.schiphol.nl/waittimes/displays/API_all_predictive_private'
HEADERS = {'app_key': APP_KEY,
               'app_id': APP_ID,
               'Accept': 'application/json',
               'ResourceVersion': 'v1'}

def get_unique_filters() -> set:
    """ Returns the list of all unique filters"""
    resp = requests.get(URL, headers=HEADERS)
    resp_json = json.loads(resp.text)['measurements']
    unique_filters = set()
    for meas in resp_json:
        unique_filters.add(meas['resultId'].strip('_economy_prediction'))
    return unique_filters

def get_waittime_for_filter(filter_airport:str) -> dict:
    """Get the current waittime for a specific filter """
    resp = requests.get(URL, headers=HEADERS)
    resp_json = json.loads(resp.text)['measurements']
    result = {}
    wanted = set(['updated', 'timeIntervalInMinutes'])
    for meas in resp_json:
        if meas['resultId'].strip('_economy_prediction') == filter_airport:
            result[filter_airport] = filter_dict(meas,wanted)
    return result

def get_waittime_for_filters(filter_airport:list) -> dict:
    """Get the current waittime for a set of filters """
    filter_airport = set(filter_airport)
    resp = requests.get(URL, headers=HEADERS)
    resp_json = json.loads(resp.text)['measurements']
    result = {}
    max = 0
    min = 0
    # wanted = set(['updated', 'timeIntervalInMinutes'])
    for meas in resp_json:
        result_id = meas['resultId'].strip('_economy_prediction')
        if result_id in filter_airport:
            max_val = meas['timeIntervalInMinutes'].get('max',0)
            min_val = meas['timeIntervalInMinutes'].get('min',0)
            result[result_id] ={'max':max_val, 'min': min_val}
            max += max_val
            min += min_val
    result['max_waiting'] = max
    result['min_waiting'] = min
    return result

if __name__ == '__main__':
    # pprint(get_unique_filters())
    pprint(get_waittime_for_filter('T6'))

    # pprint(status)
