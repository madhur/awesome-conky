#!/usr/bin/env python

from feedly import FeedlyClient
import json
from subprocess import call
from os.path import expanduser
import time

#Categories to ignore, you can add yours
ignored=["global.all", "global.must", "global.uncategorized", "Security", "Ignore", "GMAT", "sharepoint", "madhur"]

FEEDLY_REDIRECT_URI = "http://localhost"

def get_feedly_client(token=None):
    if token:
        return FeedlyClient(token=token, sandbox=False)
    else:
        return FeedlyClient(
                            client_id=FEEDLY_CLIENT_ID, 
                            client_secret=FEEDLY_CLIENT_SECRET,
                            sandbox=False
        )
def auth(request):   
    feedly = get_feedly_client()
    # Redirect the user to the feedly authorization URL to get user code
    code_url = feedly.get_code_url(FEEDLY_REDIRECT_URI)    
    return redirect(code_url)

def callback(request):
    code=request.GET.get('code','')
    if not code:
        return HttpResponse('The authentication is failed.')

    feedly = get_feedly_client()

    #response of access token
    res_access_token = feedly.get_access_token(FEEDLY_REDIRECT_URI, code)
    # user id
    if 'errorCode' in res_access_token.keys():
        return HttpResponse('The authentication is failed.')

    id = res_access_token['id']
    access_token=res_access_token['access_token']    

def feed(access_token):
    '''get user's subscription'''
    feedly = get_feedly_client()
    user_subscriptions = feedly.get_user_subscriptions(access_token)    


json_data=open(expanduser('~')+'/.conky/scripts/.passwords.json')
data = json.load(json_data)
access_token=data['feedly']['access_token']

client =  get_feedly_client(access_token)
categories = client.get_user_categories(access_token)
counts = client.get_unread_count(access_token)

text=""
count=0
for item in counts['unreadcounts']:
    itemcount = item['count']
    itemname = item['id'][51:]
    if(itemcount > 0 and itemname not in ignored and "user/23bbb2c4-62b9-4bb9-a756-556cef1512f9/category/" in item['id']):        
        count = count + itemcount
        text=text + "${color1}%s${alignr}${color white} %d" %(itemname, itemcount) +"\n"

print "${color1}Total unread: ${color white}%s ${alignr}${color1}Updated: ${color white}%s" %(count, time.strftime("%I:%M"))
print text

#call(['notify-send','Feedly Updated'])        