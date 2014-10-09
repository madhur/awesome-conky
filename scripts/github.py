#! /usr/bin/env python

import urllib2
import json
import zlib
import base64
from subprocess import call
from os.path import expanduser
import time

json_data=open(expanduser('~')+'/.conky/scripts/.passwords.json')
data = json.load(json_data)
username=data['github']['username']
password=data['github']['password']

#Put repos to publish
repos = data['github']['fav_repos']

request = urllib2.Request("https://api.github.com/users/" + username)
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)   

j = urllib2.urlopen(request)
json_data = j.read()
j_obj = json.loads(json_data)


print "${color1}Followers: ${color white}%d ${alignr}${color1}Updated: ${color white}%s" %(j_obj['followers'], time.strftime("%I:%M"))

for repo in repos:
	repourl = "https://api.github.com/repos/"+ username +"/" + repo
	
	request = urllib2.Request(repourl)
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)   

	j = urllib2.urlopen(request)
	json_data = j.read()
	j_obj = json.loads(json_data)

	print "${color white}%s  ${goto 200}${color1}Starred: ${color white}%d    ${color1}${alignr}Forks: ${color white}%d" %(j_obj['name'],  j_obj['stargazers_count'], j_obj['forks_count'])

