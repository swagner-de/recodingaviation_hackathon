"""Module that handles api calls to get information about flights"""
from pprint import pprint
import requests as requests

API_KEY = "2cfd0827f82ceaccae7882938b4b1627"

def get_flights(airport, adi, airline="", future_window=0):
    """ Requests all flights from an airport.

    Keyword arguments:
    airport -- iata code of airport
    airline -- iata code of airline
    adi -- a | d (a = arrival, d = depature)
    future_window -- relevant scope of hours (optional)"""
    if airline != "":
        airline += "/"
    url = "https://flifo-qa.api.aero/flifo/v3/flights/{}/{}{}"
    url = url.format(airport, airline, adi)
    payload = {"futureWindow": future_window}
    headers = {"X-apiKey": API_KEY, "Accept":"application/json"}
    resp = requests.get(url, headers=headers, params=payload)
    return resp

def get_flight(airport, airline, flightno, adi, operation_date=""):
    """ Requests information for a specific flight.

    Keyword arguments:
    airport -- iata code of airport
    airline -- iata code of airline
    flightno -- flightnumber
    adi -- a | d (a = arrival, d = depature)
    operation_date -- date of the flight (default: current day) """

    url = "https://flifo-qa.api.aero/flifo/v3/flight/{}/{}/{}/{}"
    url = url.format(airport, airline, flightno, adi)
    headers = {"X-apiKey": API_KEY, "Accept":"application/json"}
    if operation_date != "":
        payload = {"operationDate": operation_date}
        resp = requests.get(url, headers=headers, params=payload)
    else:
        resp = requests.get(url, headers=headers, params=payload)
    return resp

if __name__ == "__main__":
    # get_flights("MIA", "d")
    get_flight("FRA","LH", "012", "d"
