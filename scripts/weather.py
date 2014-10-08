#! /usr/bin/env python3

import urllib
import json
from subprocess import call
import sys
import time
from xml.dom import minidom
from os.path import expanduser
import urllib.request

json_data=open(expanduser('~')+'/.conky/scripts/.passwords.json')
data = json.load(json_data)
location_code=data['weather']['location_code']

url = 'http://weather.yahooapis.com/forecastrss?w='+location_code+'&u=c'

j = urllib.request.urlopen(url)
weather_data = j.read()
xmldoc = minidom.parseString(weather_data)
locs = xmldoc.getElementsByTagName("yweather:location")
city= locs[0].attributes['city'].value
country= locs[0].attributes['country'].value

locs = xmldoc.getElementsByTagName("yweather:condition")
current_condition= locs[0].attributes['text'].value
current_code = locs[0].attributes['code'].value
current_temp = locs[0].attributes['temp'].value
weather_date=locs[0].attributes['date'].value

locs = xmldoc.getElementsByTagName("yweather:units")
speed_unit = locs[0].attributes['speed'].value

locs = xmldoc.getElementsByTagName("yweather:wind")
speed =  locs[0].attributes['speed'].value

locs = xmldoc.getElementsByTagName("yweather:atmosphere")
humidity =  locs[0].attributes['humidity'].value

forecast = []
locs = xmldoc.getElementsByTagName("yweather:forecast")
for loc in locs:
	forecast.append((loc.attributes['day'].value, loc.attributes['low'].value, loc.attributes['high'].value , loc.attributes['code'].value))


print ("${voffset -20}${font Open Sans:size=15:style=Light}%s, %s${font}" % (city, country))
print ("${color7}${hr}${color}")
print ("${font Open Sans:size=60:style=Light}${alignr}%s°${font}${voffset -20}" %(current_temp))
print ("${image ~/.conky/.conky-google-now/%s.png -p 0,45 -s 60x60}" %(current_code))
print ("%s" %(current_condition))
print ("${image ~/.conky/.conky-google-now/wind.png -p 0,135 -s 15x15}${goto 35}%s %s" %(speed, speed_unit))
print ("${image ~/.conky/.conky-google-now/humidity.png -p 0,155 -s 15x15}${goto 35}%s %s" %(humidity,"%"))
print ("${image ~/.conky/.conky-google-now/%s.png -p 0,185 -s 30x30}${image ~/.conky/.conky-google-now/%s.png -p 130,185 -s 30x30}${voffset -10}" %(forecast[0][3], forecast[1][3]))
print ("${goto 60}%s ${goto 190} %s" %(forecast[0][0].upper(), forecast[1][0].upper()))
print ("${goto 60}%s°${color6}%s°${color}${goto 190}%s°${color6}%s°${color}${voffset 15}" %(forecast[0][2], forecast[0][1], forecast[1][2], forecast[1][1]))
print ("${font :size=6}${color7}Updated: ${alignr}${color white}%s" %(time.strftime("%I:%M")))
print ("${color7}Published: ${alignr}${color white}%s" %(weather_date))