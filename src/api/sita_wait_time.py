import json
import requests

from util import filter_dict


def get_wait_time(iata_airport: str) -> dict:
    api_key = '8e2cff00ff9c6b3f448294736de5908a'
    headers = {'X-apiKey': api_key,
               'Accept': 'application/json'}
    relevant_keys = set(['projectedWaitTime', 'projectedMinWaitMinutes', 'projectedMaxWaitMinutes'])

    uri = 'https://waittime-qa.api.aero/waittime/v1/current/{iata}'
    resp = requests.get(uri.format(iata=iata_airport), headers=headers)
    if resp.status_code == 200:
        result = {}
        resp_bdy = json.loads(resp.text)
        try:
            current_queue = resp_bdy['current']
            for checkpoint in current_queue:
                try:
                    result[checkpoint['queueName']] = filter_dict(checkpoint, relevant_keys)
                except KeyError:
                    pass
        except KeyError:
            return
        return result if not len(result) == 0 else None
