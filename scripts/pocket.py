#! /usr/bin/env python

import urllib2
import urllib
import json
from subprocess import call
from os.path import expanduser

json_data=open(expanduser('~')+'/.conky/scripts/.passwords.json')
data = json.load(json_data)
key=data['pocket']['key']
access_token=data['pocket']['access_token']


data = {'consumer_key': key, 'access_token': access_token}
data = urllib.urlencode(data)

request = urllib2.Request("https://getpocket.com/v3/stats")

j = urllib2.urlopen(request, data)
json_data = j.read()
j_obj = json.loads(json_data)


print "${color1}Unread Items: ${alignr}${color white}%d" %(j_obj['count_unread'])
