#! /usr/bin/env python3

import urllib.request
import urllib             # For BasicHTTPAuthentication
import feedparser         # For parsing the feed
from textwrap import wrap # For pretty printing assistance
import json
from os.path import expanduser
import sys

_URL = "https://mail.google.com/gmail/feed/atom/unread"

def auth():

    

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
    
    '''The method to do HTTPBasicAuthentication'''
    #opener = urllib.FancyURLopener()
    f = opener.open(_URL)
    feed = f.read()
    return feed

def fill(text, width):
    '''A custom method to assist in pretty printing'''
    if len(text) < width:
        return text + ' '*(width-len(text))
    else:
        return text

def readmail(feed):
    '''Parse the Atom feed and print a summary'''
    atom = feedparser.parse(feed)

    print ("${color white}You have %s new mails${color}" % len(atom.entries))
  
    for i in range(len(atom.entries)):
        print ("%s" % (fill(wrap(atom.entries[i].title, 50)[0]+" ...", 55)))

def countmail(feed):
    '''Parse the Atom feed and print a summary'''
    atom = feedparser.parse(feed)  
    print ("Emails: %s new" %len(atom.entries))
                
if __name__ == "__main__":
    f = auth()  # Do auth and then get the feed
    if(len(sys.argv) > 1):
        countmail(f)
    else:
        readmail(f) # Let the feed be chewed by feedparse