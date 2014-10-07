#! /usr/bin/env python

import urllib2
import json
import zlib
import base64
from subprocess import call

username="madhur"
password="whoknowswho25"
#user = 'https://api.github.com/users/madhur'

request = urllib2.Request("https://api.github.com/users/madhur")
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)   

j = urllib2.urlopen(request)
json_data = j.read()
j_obj = json.loads(json_data)

#print "${goto 250}${color1}Repos: ${alignr}${color white}%d" %(j_obj['public_repos'])
print "${goto 250}${color1}Followers: ${alignr}${color white}%d" %(j_obj['followers'])

repos = ["madhur.github.com", "portablejekyll", "GAnalytics", "wunder-java", "msysgit-2.0.0"]

for repo in repos:
	repourl = "https://api.github.com/repos/madhur/"+ repo
	
	request = urllib2.Request(repourl)
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)   

	j = urllib2.urlopen(request)
	json_data = j.read()
	j_obj = json.loads(json_data)

	print "${goto 250}${color white}%s  ${alignr}${color1}Starred: ${color white}%d    ${color1}Forks: ${color white}%d" %(j_obj['name'],  j_obj['stargazers_count'], j_obj['forks_count'])

