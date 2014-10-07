#!/usr/bin/env python

from feedly import FeedlyClient
import json
from subprocess import call

ignored=["global.all", "global.must", "global.uncategorized", "Security", "Ignore", "GMAT"]
code = "AhDOo-J7ImkiOiIyM2JiYjJjNC02MmI5LTRiYjktYTc1Ni01NTZjZWYxNTEyZjkiLCJ1IjoiMTAxMjk2MjUyNDE1MzQ5MDM1NzgwIiwiYSI6IldlYlJlYWRlciIsInAiOjYsInQiOjE0MTI2MTQwMzEzMzd9"
#{u'access_token': u'Ajkjuy97ImEiOiJXZWJSZWFkZXIiLCJlIjoxNDEzMjE4OTU2Mjg4LCJpIjoiMjNiYmIyYzQtNjJiOS00YmI5LWE3NTYtNTU2Y2VmMTUxMmY5IiwicCI6NiwidCI6MSwidiI6InByb2R1Y3Rpb24iLCJ3IjoiMjAxMy4xMiIsIngiOiJzdGFuZGFyZCJ9:webreader', 
#u'expires_in': 604799, u'token_type': u'Bearer', u'plan': u'standard', u'provider': u'GooglePlus', u'id': u'23bbb2c4-62b9-4bb9-a756-556cef1512f9', 
#u'refresh_token': u'AtOPH917ImkiOiIyM2JiYjJjNC02MmI5LTRiYjktYTc1Ni01NTZjZWYxNTEyZjkiLCJ1IjoiMTAxMjk2MjUyNDE1MzQ5MDM1NzgwIiwiYSI6IldlYlJlYWRlciIsInAiOjYsImMiOjE0MTI2MTQxNTYyODgsInYiOiJwcm9kdWN0aW9uIiwibiI6ImVWYjlnOTJmRDVhSEh1cDYifQ:webreader'}
access_token = "Ajkjuy97ImEiOiJXZWJSZWFkZXIiLCJlIjoxNDEzMjE4OTU2Mjg4LCJpIjoiMjNiYmIyYzQtNjJiOS00YmI5LWE3NTYtNTU2Y2VmMTUxMmY5IiwicCI6NiwidCI6MSwidiI6InByb2R1Y3Rpb24iLCJ3IjoiMjAxMy4xMiIsIngiOiJzdGFuZGFyZCJ9:webreader"

FEEDLY_REDIRECT_URI = "http://localhost"
FEEDLY_CLIENT_ID="webreader"
FEEDLY_CLIENT_SECRET="FE01FQSUP6QB0XP4XQ07VVMDWBKU"
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


client =  get_feedly_client(access_token)
categories = client.get_user_categories(access_token)
#with open('categories.json', 'w') as outfile:
#  json.dump(categories, outfile)
#print categories
counts = client.get_unread_count(access_token)
#with open('counts.json', 'w') as outfile:
#  json.dump(counts, outfile)
#print counts

for item in counts['unreadcounts']:
    itemcount = item['count']
    itemname = item['id'][51:]
    if(itemcount > 0 and itemname not in ignored and "user/23bbb2c4-62b9-4bb9-a756-556cef1512f9/category/" in item['id']):
        print "${goto 250}${color1}%s${alignr}${color white} %d" %(itemname, itemcount)


call(['notify-send','Feedly Updated'])        