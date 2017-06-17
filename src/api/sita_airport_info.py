""" Module that handles api calls to get information related to airports"""
import json
import requests

API_KEY = "3035d833bb6e531654a3cce03e6b1fde"

def get_airport_iata(iata):
    """
    Get all information about a airport by iata code
    Keyword arguments:
    iata -- airport iata code
    """
    url = "https://airport-qa.api.aero/airport/v2/airport/{}"
    url = url.format(iata)
    headers = {"X-apiKey": API_KEY, "Accept":"application/json"}
    resp = requests.get(url, headers=headers)
    resp = json.loads(resp.text)
    return resp.get('airports', None)

def get_airport_match(query):
    """
    Match airport by iata code or name

    Keyword arguments:
    query -- airport name or code to be found
    """
    url = "https://airport-qa.api.aero/airport/v2/match/{}"
    url = url.format(query)
    headers = {"X-apiKey": API_KEY, "Accept":"application/json"}
    resp = requests.get(url, headers=headers)
    resp = json.loads(resp.text)
    return resp.get('airports', None)

def get_airport_distance(iata_from, iata_to, units="km"):
    """
    Calculate the distance between two airports

    Keyword arguments:
    iata_from -- airport iata code
    iata_to -- airport iata code
    units -- unit of measure for distance (km or miles)
    """
    url = "https://airport-qa.api.aero/airport/v2/distance/{}/{}"
    url = url.format(iata_from, iata_to)
    headers = {"X-apiKey": API_KEY, "Accept":"application/json"}
    params = {"units":units}
    resp = requests.get(url, headers=headers, params=params)
    resp = json.loads(resp.text)
    return resp.get('distance', None)

def get_airport_nearest(latitude, longitude, max=5):
    """
    Get the nearest airports for a geo location

    Keyword arguments:
    latitude -- coordinates (e.g. 52.297097)
    longitude -- coordinates (e.g. 4.879903)
    max -- maximum number of airports to be returned (optional)
    """
    url = "https://airport-qa.api.aero/airport/v2/nearest/{}/{}"
    url = url.format(latitude, longitude)
    headers = {"X-apiKey": API_KEY, "Accept":"application/json"}
    params = {"maxAirports":max}
    resp = requests.get(url, headers=headers, params=params)
    resp = json.loads(resp.text)
    return resp.get('airports', None)

if __name__ == "__main__":
    # get_airport_iata("FRA")
    get_airport_match("frank")
    # get_airport_distance("FRA", "HAM", "mile")
    # get_airport_nearest("52.297097", "4.879903", 1)
