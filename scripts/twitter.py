#! /usr/bin/env python

import urllib2
import json
import zlib
import base64
from subprocess import call
from os.path import expanduser

json_data=open(expanduser('~')+'/.conky/scripts/.passwords.json')
data = json.load(json_data)
access_token=data['twitter']['access_token']
user = data['twitter']['user']

request = urllib2.Request("https://api.twitter.com/1.1/users/show.json?screen_name=" + user)
bearer_value = 'Bearer %s' % access_token
request.add_header("Authorization", bearer_value)   

j = urllib2.urlopen(request)
json_data = j.read()
j_obj = json.loads(json_data)


print "${color1}Twitter Followers: ${alignr}${color white}%d" %(j_obj['followers_count'])
