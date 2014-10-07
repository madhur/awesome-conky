#! /usr/bin/env python

import urllib2
import json
import zlib
import base64
from subprocess import call
from os.path import expanduser

json_data=open(expanduser('~')+'/.conky/scripts/.passwords.json')
data = json.load(json_data)
username=data['github']['username']
password=data['github']['password']

#Put your github username
user = "madhur"

#Put repos to publish
repos = ["madhur.github.com", "portablejekyll", "GAnalytics", "wunder-java", "msysgit-2.0.0"]

request = urllib2.Request("https://api.github.com/users/" + user)
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)   

j = urllib2.urlopen(request)
json_data = j.read()
j_obj = json.loads(json_data)


print "${color1}Followers: ${alignr}${color white}%d" %(j_obj['followers'])

for repo in repos:
	repourl = "https://api.github.com/repos/madhur/"+ repo
	
	request = urllib2.Request(repourl)
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)   

	j = urllib2.urlopen(request)
	json_data = j.read()
	j_obj = json.loads(json_data)

	print "${color white}%s  ${alignr}${color1}Starred: ${color white}%d    ${color1}Forks: ${color white}%d" %(j_obj['name'],  j_obj['stargazers_count'], j_obj['forks_count'])

