""" This module retrieves weather information for a airport"""
import json
import requests
from util import filter_dict
from pprint import pprint

API_KEY = "89e15931434731aefdaa04920ec60e44"

def get_airport_weather_current(iata, scale="C"):
    """
    Get current weather information for an airport
    Keyword arguments:
    iata -- airport iata code
    scale -- temparature scale (C or F)
    """
    url = "https://weather-qa.api.aero/weather/v1/current/{}"
    url = url.format(iata)
    headers = {"X-apiKey": API_KEY, "Accept":"application/json"}
    params = {"temperatureScale":scale}
    resp = requests.get(url, headers=headers, params=params)
    resp = json.loads(resp.text)
    return resp.get('currentWeather', None)

def get_airport_weather_forecast(iata, duration="7", scale="C"):
    """
    Get weather forecast information for an airport

    Keyword arguments:
    iata -- airport iata code
    duration -- period of days to be returned
    scale -- temparature scale (C or F)
    """
    url = "https://weather-qa.api.aero/weather/v1/forecast/{}"
    url = url.format(iata)
    headers = {"X-apiKey": API_KEY, "Accept":"application/json"}
    params = {"temperatureScale":scale, "duration":duration}
    resp = requests.get(url, headers=headers, params=params)
    resp = json.loads(resp.text)
    return resp('weatherForecast', None)

def get_airport_weather_combined(iata, duration="7", scale="C"):
    """
    Get combination of current weather information and forecast for an airport

    Keyword arguments:
    iata -- airport iata code
    duration -- period of days to be returned
    scale -- temparature scale (C or F)
    """
    url = "https://weather-qa.api.aero/weather/v1/combined/{}"
    url = url.format(iata)
    headers = {"X-apiKey": API_KEY, "Accept":"application/json"}
    params = {"temperatureScale":scale, "duration":duration}
    resp = requests.get(url, headers=headers, params=params)
    resp = json.loads(resp.text)
    filter_set = {"currentWeather", "weatherForecast"}
    resp = filter_dict(resp, filter_set)
    return resp('weatherForecast', None)


if __name__ == "__main__":
    # get_airport_weather_current("HAM")
    # get_airport_weather_forecast("HAM", 7)
    get_airport_weather_combined("HAM", 7)
