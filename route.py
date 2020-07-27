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
    return seconds

def get_routetime(stops, margin = 300):
    totalTime = 0
    for i in range(0, len(stops)-1):
        print(i)
        traveltime = get_traveltime(stops[i], stops[i+1])
        print(traveltime)
        totalTime += traveltime
    return totalTime + (len(stops)-2)*300   # margin for intermediary stops

def sec_to_hms(sec):
    return str(datetime.timedelta(seconds=sec))

print(sec_to_hms(get_routetime(['koningin astridlaan 10 helchteren', 'emiel verhaerenstraat 133 leopoldsburg', 'koningin astridlaan 10 helchteren' ])))