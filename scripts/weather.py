#! /usr/bin/env python

import urllib2
import json
import zlib
from subprocess import call
import sys
import time
from xml.dom import minidom
from os.path import expanduser

json_data=open(expanduser('~')+'/.conky/scripts/.passwords.json')
data = json.load(json_data)
location_code=data['weather']['location_code']

url = 'http://weather.yahooapis.com/forecastrss?w='+location_code+'&u=c'

j = urllib2.urlopen(url)
weather_data = j.read()
xmldoc = minidom.parseString(weather_data)
locs = xmldoc.getElementsByTagName("yweather:location")
city= locs[0].attributes['city'].value
country= locs[0].attributes['country'].value

locs = xmldoc.getElementsByTagName("yweather:condition")
current_condition= locs[0].attributes['text'].value
current_code = locs[0].attributes['code'].value
current_temp = locs[0].attributes['temp'].value

locs = xmldoc.getElementsByTagName("yweather:wind")
speed =  locs[0].attributes['speed'].value

locs = xmldoc.getElementsByTagName("yweather:atmosphere")
humidity =  locs[0].attributes['humidity'].value

forecast = []
locs = xmldoc.getElementsByTagName("yweather:forecast")
for loc in locs:
	forecast.append((loc.attributes['day'].value, loc.attributes['low'].value, loc.attributes['high'].value , loc.attributes['code'].value))

print forecast