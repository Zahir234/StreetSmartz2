from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

from flask import Flask, request
from flask_cors import CORS
import requests
import re
import json

app = Flask(__name__)
app.debug = True
CORS(app)
url = "https://maps.googleapis.com/maps/api/directions/json"

API_KEY = "AIzaSyCgcPiuIBhyF6ycpKoipIXp8HSX07aFWM0"  
from_place = "500 northside cir atlanta,ga"
to = "151 piedmont ave atlanta,a"
origin = "origin"
destination = "destination"
key="key"

crime_file = open("apd_data.txt", "r")
crimes = crime_file.readlines()


list_of_crime_points = []

for crime_string in crimes:
    crime_attributes = crime_string.split("\t")

    lat = crime_attributes[22]
    lng = crime_attributes[21]

    day_of_crime = crime_attributes[16]

    crime = {}
    crime['lat'] = lat
    crime['lng'] = lng
    crime['day'] = day_of_crime
    crime['time'] = crime_attributes[15]
    list_of_crime_points.append( crime  )










@app.route("/", methods=['GET'])
def get_directions():
    from_place = request.args.get('from_place')
    to = request.args.get('to')
    params = {"origin" : from_place , "destination" : to , "key" : API_KEY}
    params['mode'] = 'walking'
    response = requests.get(url, params=params)

    response_json = response.json()
    routes = response_json['routes']



    for route in routes:
        route['crimes'] = []
        route['crime_count'] = 0
        route['crimes_per_day'] =  {}
        route['crimes_per_day']['Mon'] = 0
        route['crimes_per_day']['Tue'] = 0
        route['crimes_per_day']['Wed'] = 0
        route['crimes_per_day']['Thu'] = 0
        route['crimes_per_day']['Fri'] = 0
        route['crimes_per_day']['Sat'] = 0
        route['crimes_per_day']['Sun'] = 0

        route['crimes_by_time'] = {}
        route['crimes_by_time']['Morn'] = 0
        route['crimes_by_time']['Eve'] = 0
        route['crimes_by_time']['Day'] = 0

        for crime in list_of_crime_points:
            current_crimes_lat = float(crime['lat'])
            current_crimes_lng = float(crime['lng'])



            day_of_crime = crime['day']
            time_of_crimes = crime['time']

            

            '''"bounds": {
            "northeast": {
              "lat": 33.8020922,
              "lng": -84.3799126
            },
            "southwest": {
              "lat": 33.757096,
              "lng": -84.4078555
            }'''

            southwest_lng = float(route['bounds']['southwest']['lng'])
            southwest_lat = float(route['bounds']['southwest']['lat'])

            northeast_lng = float(route['bounds']['northeast']['lng'])
            northeast_lat = float(route['bounds']['northeast']['lat'])

            if (current_crimes_lat >= southwest_lat) and ( current_crimes_lat <= northeast_lat) and (current_crimes_lng >= southwest_lng) and ( current_crimes_lng <= northeast_lng):
            	print "YOOO WE A GOT A CRIME"
                route['crimes'].append({'lat' : current_crimes_lat,  'lng' : current_crimes_lng })
                route['crime_count'] = route['crime_count'] + 1

                if day_of_crime in route['crimes_per_day']:
                	route['crimes_per_day'][ day_of_crime ] = route['crimes_per_day'][ day_of_crime ] + 1

                if time_of_crimes in route['crimes_by_time']:
                    route['crimes_by_time'][time_of_crimes] = route['crimes_by_time'][time_of_crimes] + 1

        ordered_days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        ordered_time = ["Morn","Day", "Eve"]

        route['day_data'] = []
        route['time_data'] = []

        for day in ordered_days:
            route['day_data'].append( route['crimes_per_day'][day])

        for time in ordered_time:
            route['time_data'].append( route['crimes_by_time'][time])


            	





    return json.dumps( routes )






