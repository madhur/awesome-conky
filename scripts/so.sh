#! /usr/bin/env python

import urllib2
import json
import zlib
from subprocess import call

so = 'https://api.stackexchange.com/2.2/users/507256?order=desc&sort=reputation&site=stackoverflow'

j = urllib2.urlopen(so)
json_data = j.read()
if j.info()['Content-Encoding'] == 'gzip':
    json_data = zlib.decompress(json_data, zlib.MAX_WBITS + 16)
    j_obj = json.loads(json_data)
    print j_obj['items'][0]['reputation']


call(['notify-send','Conky Updated'])
