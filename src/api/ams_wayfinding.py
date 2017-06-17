import ams_wait_time
import requests
import json
import re

def get_geometry(gate, departue=True):
    uri = 'http://etest2.esri.nl:8080/arcgis/rest/services/Schiphol/SWF_POI/MapServer/0/query?where=NAME=%27{gate}%27%20and%20SUBCATEGORY%20=%20%27{dep_arr}%20Gate%27&outFields=*&returnGeometry=true&outSR=4326&returnZ=true&f=json'
    if not re.search('\\w\\d{2}', gate):
        raise ValueError('Not a valid gate: %s' % gate)

    dep_arr = 'Departing' if departue else 'Arriving'

    uri.format(
        dep_arr=dep_arr,
        gate=gate
    )

    resp = requests.get(uri.format(
        dep_arr=dep_arr, gate=gate))

    if not resp.status_code == 200:
        return

    resp_bdy = json.loads(resp.text)
    features = resp_bdy.get('features', [])

    for item in features:
        return item.get('geometry', None)

def get_pedestrian_time(routes):
    for route in routes:
        return route.get('attributes', {}).get('Total_PedestrianTime', None)

def get_filters_on_route(directions):
    filters_set = ams_wait_time.get_unique_filters()
    filters = []
    for item in directions:
        events = item.get('events', [])
        for event in events:
            event_strings = event.get('strings', [{}])
            for string_ in event_strings:
                evt_string = string_.get('string', None)
                if evt_string:
                    try:
                        relevant = [k for k in filters_set if k in evt_string]
                        if relevant:
                            filters.append(relevant[0])
                    except AttributeError:
                        pass
    return filters if len(filters) != 0 else None

def __get_directions_from_geo(geo_arr:str, geo_dep:str) -> dict:
    uri = 'http://etest2.esri.nl:8080/arcgis/rest/services/Schiphol/SWF_NETWORK/NAServer/Route/solve?stops=' \
          '{"type":"features","features":[{"geometry":{%s,"spatialReference":{"wkid":4326}}},{"geometry":{%s,"spatialReference":{"wkid":4326}}' \
          '}]}&outSR=4326&ignoreInvalidLocations=true&returnDirections=true&returnRoutes=true&directionsOutputType=esriDOTComplete&directionsTimeAttributeName=&returnZ=true&f=json'
    resp = requests.get(
        uri % (geo_arr, geo_dep)
    )
    print(uri % (geo_arr, geo_dep))
    resp_bdy = json.loads(resp.text)
    resp = None

    routes = resp_bdy.get('routes', {}).get('features', [])
    directions = resp_bdy.get('directions', [{}])[0].get('features', [])
    resp_bdy = None


    return {
        'total_ped_time': get_pedestrian_time(routes),
        'filters_on_route': get_filters_on_route(directions)
    }



def get_directions_from_gates(arr_gate:str, dep_gate:str) -> dict:
    arrival_g = get_geometry(arr_gate, departue=False)
    departure_g = get_geometry(dep_gate, departue=True)
    geo_arr = str(arrival_g).replace('{','').replace('}', '')
    geo_dep = str(departure_g).replace('{','').replace('}', '')
    resp = __get_directions_from_geo(geo_arr, geo_dep)

    return resp


if __name__ == '__main__':
    from pprint import pprint
    r= get_directions_from_gates(arr_gate='D03', dep_gate='F04')
    pprint(r)
    pprint(ams_wait_time.get_waittime_for_filters(r['filters_on_route']))
