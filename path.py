from yammer import Yammer
import httplib2
import time
import urllib2
import urllib
import json
import collections
import pprint
import logging
import re
import oauth2 as oauth
import time
import json
import requests
import sys
from flask import Flask, render_template, redirect, request, session, g, flash
from BeautifulSoup import BeautifulSoup 
#URL handler in application for logging in

app = Flask(__name__)
SECRET_KEY = 'yam_path_hackathon_OCT27'
app.config.from_object(__name__)

CONSUMER_KEY = "bIG8LNgSYklfUgE99wvyPQ"
CONSUMER_SECRET = "uXp5aTrHlUlSlLjo7ouuN7XqYkLBwUGZemhObU7mqs"
CODE = "xMStn1LQQ5rUueexWOLsLQ"
ACCESS_TOKEN = "UPHfq3mR70BndCMQzHtoww"
client = Yammer(CONSUMER_KEY, CONSUMER_SECRET, oauth2=True, redirect_url='localhost:5000/authenticate')
JSON_URL = ""

# Authorize URL
#https://www.yammer.com/dialog/authenticate?client_id=bIG8LNgSYklfUgE99wvyPQ

#redirect_url='localhost:5000/authenticate'
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
	return redirect(client.get_authorize_url())

@app.route("/authenticate")
def authenticate():
	access_token = client.authenticate(CODE)
	return access_token

@app.route("/feed")
def feed():
	return render_template("group_feed.html")

def oauth_authorization(token):
	return {"Authorization": "Bearer %s" %token}

@app.route("/map")
def map():
	global JSON_URL
	JSON_URL = "https://www.yammer.com/api/v1/messages/in_group/1025128.json?include_counts=true&threaded=extended&exclude_own_messages_from_unseen=true&_=1351379906601"
	r = requests.get(JSON_URL, headers=oauth_authorization(ACCESS_TOKEN), config={'verbose': sys.stderr})
	json_dict= r.json
	# event_html = json_dict["messages"][0]["attachments"][0]
	messages_dict = json_dict["messages"][0]
	refs = json_dict["references"]

	#event_html is unicode 
	event_html2=json_dict["meta"]["ymodules"][0]["inline_html"]

	f = open('json_raw.txt')
	event_html = f.read()
	f.close()

	# re_ stands for regular expression
	re_loc= r"\<div.*ymodule.*location.*\> (.*) \</div\>"
	m = re.search(re_loc, event_html)
	event_location =  m.group(1)

	re_title =r"\<h4.*\> (.*) \<\/a\>\s<\/h4\>"
	n = re.search(re_title, event_html)
	event_title = n.group(1)

	day_and_date =  "\<span.+2012.+\>([\w]+)\,\s([a-zA-Z]+\s[\d]+)\,\s"
	year_and_hour = "(\d{4})\s(\d{1,2}\:\d{2}\s[P|A]M)\<\/span\>"
	re_datetime = r"%s%s" %(day_and_date, year_and_hour)		

	o = re.search(re_datetime, event_html)
	day_of_the_week = o.group(1)	#group 1 is day_of_the_week
	date = o.group(2)	#group 2 is month day
	year = o.group(3)	#group 3 is year
	hour = o.group(4)	#group 4 is --:-- PM
	event_time =  hour + " on " + day_of_the_week + ", " + date + ", " + year 
	
	# # re_event_title = 
	# #get list of people invited
	# guests_list = messages_dict["body"]["rich"]
	# guests_named = re.findall('(\w+\s\w+)', 'guests_list')
	# guests_named = []

	return render_template("map2.html", loc= event_location, title = event_title, time = event_time)
		# title = event_title, time = event_time)
		# event_time=event_time, event_location=event_location, event_title=event_title)

	# return json_object
	# client.request(url)
	# data = urllib.urlopen(JSON_URL)
	# JSON_text = data.read()
	# print JSON_text
	# return render_template("map.html")



if __name__ == "__main__":
    app.run(debug=True)


# def authorize(self, url, ):
# 	return redirect(client.get_authorize_url())

# Interacting with the Yammer messages API
# client = Yammer(CONSUMER_KEY, CONSUMER_SECRET, oauth2=True,access_token=access_token)
# msg_id = client.message.post('My message', group_id=GROUP_ID)
# rv = client.messages.get(msg_id)
# client.messages.delete(msg_id)

# @app.before_request
# def set_up_db():
#     g.db = model.connect_db()
