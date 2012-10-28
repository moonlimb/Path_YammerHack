import re


        
text = """
<div class="ymodule-instance-7378779-vcalendar">
   <div class="ymodule-instance-7378779-vevent" style="margin-bottom:5px">
      <span class="ymodule-instance-7378779-uid"> <span class="ymodule-instance-7378779-value-title" id="ymodule-instance-7378779-uid" title="event-undefined@yammer.com"></span> </span> <span class="ymodule-instance-7378779-dtstamp"> <span class="ymodule-instance-7378779-value-title" id="ymodule-instance-7378779-dtstamp" title="2012-10-28T04:29::00.000Z"></span> </span> <span class="ymodule-instance-7378779-dtend"> <span class="ymodule-instance-7378779-value-title" id="ymodule-instance-7378779-dtend" title="2012-10-28T02:30::00.000Z"></span> </span> <span class="ymodule-instance-7378779-url url"> <span class="ymodule-instance-7378779-value-title" id="ymodule-instance-7378779-url" title="https://www.yammer.com/hacktoberfest.onmicrosoft.com/messages/227495730"></span> </span> 
      <div class="ymodule-instance-7378779-event-icon event-icon" style="float:left;padding-right:15px">
         <div class="ymodule-instance-7378779-calcontrol" style="width:50px">
            <div class="ymodule-instance-7378779-calcontrol-header" style="background-color:#9c2a2c;text-align:center;height:16px;color:#fff;border-width:1px;border-style:solid;border-color:#8f2629;border-bottom:none;-moz-border-radius-topleft:4px;-moz-border-radius-topright:4px;-webkit-border-top-left-radius:4px;-webkit-border-top-right-radius:4px"> Oct </div>
            <div class="ymodule-instance-7378779-calcontrol-body" style="background-color:#fafafa;text-align:center;height:34px;color:#000;line-height:34px;font-weight:bold;font-size:24px;border-width:1px;border-style:solid;border-color:#e6e6e6;border-top:none;-moz-border-radius-bottomleft:4px;-moz-border-radius-bottomright:4px;-webkit-border-bottom-left-radius:4px;-webkit-border-bottom-right-radius:4px"> 27 </div>
         </div>
      </div>
      <div>
         <h4 class="ymodule-instance-7378779-title" style="margin:0"> <a href="https://www.yammer.com/hacktoberfest.onmicrosoft.com#/Threads/show?threadId=227495730" class="ymodule-instance-7378779-summary" data-action-onclick="overlay(&quot;https://ymodules.yammer.com/3/7378779/1490226512/overlay/29e3fbddbcaccd41ea66085d40cc209d74776580&quot;, 580, 325, &quot;Dinner at Yammer&quot;, &quot;/images/notifications/event.png&quot;)"> Dinner at Yammer </a> </h4>
         <div class="ymodule-instance-7378779-time" style="color:#333"> <span class="ymodule-instance-7378779-dtstart"> <span class="ymodule-instance-7378779-value-title" title="2012-10-28T01:30::00.000Z">Saturday, October 27, 2012 6:30 PM</span> </span>  <span>PDT</span> </div>
         <div class="ymodule-instance-7378779-location" style="color:#333"> YammerHQ </div>
         <div class="ymodule-instance-7378779-status" style="margin-left:65px;color:#333"> You are <a href="https://www.yammer.com/hacktoberfest.onmicrosoft.com#/Threads/show?threadId=227495730" style="font-weight:bold" data-action-onclick="overlay(&quot;https://ymodules.yammer.com/3/7378779/1490226512/overlay/29e3fbddbcaccd41ea66085d40cc209d74776580&quot;, 580, 325, &quot;Dinner at Yammer&quot;, &quot;/images/notifications/event.png&quot;)"> attending</a>. </div>
      </div>
   </div>
</div>

"""

re_loc= r"\<div.*ymodule.*location.*\> (.*) \</div\>"
m = re.search(re_loc, text)
print m.group(1)

re_title =r"\<h4.*\> (.*) \<\/a\>\s<\/h4\>"
n = re.search(re_title, text)
print n.group(1)



day_and_date =  "\<span.+2012.+\>([\w]+)\,\s([a-zA-Z]+\s[\d]+)\,\s"
year_and_hour = "(\d{4})\s(\d{1,2}\:\d{2}\s[P|A]M)\<\/span\>"
re_datetime = r"%s%s" %(day_and_date, year_and_hour)		
# one-line version:
# re_datetime = r"\<span.+2012.+\>([\w]+)\,\s([a-zA-Z]+\s[\d]+)\,\s(\d{4})\s(\d{1,2}\:\d{2}\s[P|A]M)\<\/span\>"
# print re_datetime2 == re_datetime <-- checks that one-line version is equivalent to concatenated version

o = re.search(re_datetime, text)
day_of_the_week = o.group(1)	#group 1 is day_of_the_week
date = o.group(2)	#group 2 is month day
year = o.group(3)	#group 3 is year
hour = o.group(4)	#group 4 is --:-- PM
event_time =  hour + " on " + day_of_the_week + ", " + date + ", " + year 
print event_time
	


# import requests
# import sys

# ACCESS_TOKEN = "UPHfq3mR70BndCMQzHtoww"
# JSON_URL = "https://www.yammer.com/api/v1/messages/in_group/1025128.json?include_counts=true&threaded=extended&exclude_own_messages_from_unseen=true&_=1351379906601"

# def oauth_authorization(token):
# 	return {"Authorization": "Bearer %s" %token}

# r = requests.get(JSON_URL, headers=oauth_authorization(ACCESS_TOKEN), config={'verbose': sys.stderr})
# print r.json
