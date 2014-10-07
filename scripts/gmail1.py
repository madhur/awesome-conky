#! /usr/bin/env python3

import urllib.request
from xml.etree import ElementTree as etree
from subprocess import call

# Enter your username and password below within quotes below, in place of ****.
# Set up authentication for gmail
auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='New mail feed',
                          uri='https://mail.google.com/',
                          user= 'ahuja.madhur',
                          passwd= 'cmu@word10')
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