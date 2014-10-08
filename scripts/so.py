#! /usr/bin/env python

import urllib2
import json
import zlib
from subprocess import call
import sys
import time

so = 'https://api.stackexchange.com/2.2/users/507256?order=desc&sort=reputation&site=stackoverflow'

j = urllib2.urlopen(so)
json_data = j.read()
if j.info()['Content-Encoding'] == 'gzip':
    json_data = zlib.decompress(json_data, zlib.MAX_WBITS + 16)
    j_obj = json.loads(json_data)
    if(len(sys.argv) > 1):
    	print "%s: %s" %("Reputation", j_obj['items'][0]['reputation'])
    else:
    	print "${color}%s: ${alignr}${color white} %s" %("Stackoverflow Reputation", j_obj['items'][0]['reputation'])
    	print "  ${color}%s: ${alignr}${color white} %s" %("Month", j_obj['items'][0]['reputation_change_month'])
    	print "  ${color}%s: ${alignr}${color white} %s" %("Week", j_obj['items'][0]['reputation_change_week'])
    	print "  ${color}%s: ${alignr}${color white} %s" %("Day", j_obj['items'][0]['reputation_change_day'])


call(['notify-send','Conky Updated'])
