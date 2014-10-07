#! /usr/bin/env python3

import urllib.request
from xml.etree import ElementTree as etree
from subprocess import call
import json
from os.path import expanduser

json_data=open(expanduser('~')+'/.conky/scripts/.passwords.json')
data = json.load(json_data)
username=data['gmail']['username']
password=data['gmail']['password']


auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='New mail feed',
                          uri='https://mail.google.com/',
                          user= username,
                          passwd= password)

opener = urllib.request.build_opener(auth_handler)
# ...and install it globally so it can be used with urlopen.
urllib.request.install_opener(opener)

gmail = 'https://mail.google.com/mail/feed/atom'
NS = '{http://purl.org/atom/ns#}'
with urllib.request.urlopen(gmail) as source:
    tree = etree.parse(source)
fullcount = tree.find(NS + 'fullcount').text

print(fullcount + ' new')

#call(['notify-send','Gmail Updated'])