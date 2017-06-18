import requests
import json
import pickle
import math

ZMAP = None
KEYS_TO_KEEP = set(['AIRSIDE_LANDSIDE', 'SUBCATEGORY', 'SUBLOCATION', 'NAME'])

def get_all_pois():
    uri = "http://etest2.esri.nl:8080/arcgis/rest/services/Schiphol/SWF_POI/MapServer/0/query?where=CATEGORY LIKE '%'&outFields=*&returnGeometry=true&outSR=4326&returnZ=true&f=json"
    resp = requests.get(uri)
    resp_bdy = json.loads(resp.text)
    features = resp_bdy.get('features')
    z_map = {}
    for f in features:
        cat = f.get('attributes', {}).get('SUBCATEGORY', False)
        loc = f.get('attributes', {}).get('SUBLOCATION', False)
        if not cat or \
            'gate' in cat.lower() or \
            "ladies' room" in cat.lower() or \
            "passport control" in cat.lower() or \
            "men's room" in cat.lower():
            continue
        if not loc or 'outside' in loc.lower():
            continue

        geo = f.get('geometry')
        z = geo.get('z')
        try:
            z_map[z].append(f)
        except KeyError:
            z_map[z] = [f]
    with open('../data/ams_pois.pkl', 'wb') as f:
        pickle.dump(z_map, f)
    return z_map

def init():
    global ZMAP
    try:
        f = open('../data/ams_pois.pkl', 'rb')
        ZMAP = pickle.load(f)
    except FileNotFoundError:
        ZMAP = get_all_pois()

def euclidean_distance(x1, x2, y1, y2):
    return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))

def calculate_closest(x, y, z):
    result = {}
    klo_flag = False
    for item in ZMAP.get(z, []):
        geo = item['geometry']
        o = {k.lower(): item['attributes'][k] for k in set(item['attributes'].keys()).intersection(KEYS_TO_KEEP)}
        if 'toilet' in o.get('subcategory').lower() and klo_flag == True:
            continue
        elif 'toilet' in o.get('subcategory').lower() and klo_flag == False:
            klo_flag = True
        result[euclidean_distance(x, geo['x'], y, geo['y'])] = o
    return [result[k] for k in sorted(result, reverse=True)[:10]]

init()

if __name__ == '__main__':
    x = 4.763843565361593
    y = 52.30939576526768
    z = 0
    closest = calculate_closest(x, y, z)
    from pprint import pprint
    pprint(closest)
