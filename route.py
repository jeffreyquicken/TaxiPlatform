import configparser
import herepy
import json
import datetime

# API key (in config.ini)
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['HERE']['key']

#API's
geocoderApi = herepy.GeocoderApi(api_key)
routingApi = herepy.RoutingApi(api_key)


def address_to_geo(address):
    response = geocoderApi.free_form(address)
    data = json.loads(response.as_json_string())
    lat = data['items'][0]['access'][0]['lat']
    long = data['items'][0]['access'][0]['lng']
    return [lat, long]


def get_traveltime(start_address, end_address):
    start = address_to_geo(start_address)
    end = address_to_geo(end_address)
    response = routingApi.pedastrian_route(start,
                                           end,
                                           [herepy.RouteMode.car, herepy.RouteMode.fastest])
    seconds = response.response['route'][0]['summary']['travelTime']
    hms = str(datetime.timedelta(seconds=seconds))
    return hms
