#! /usr/bin/env python

# List of users who are probably suspended (1 rep)

### COPYRIGHT ###
"""
Copyright 2012 Bob Rao.
You are free to use this code under the terms of the GNU GPLv3.
"""
### LICENSING ###
"""
    This file is part of Win8ChallengeStats.

    Win8ChallengeStats is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Win8ChallengeStats is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Win8ChallengeStats.  If not, see <http://www.gnu.org/licenses/>.
"""
### PROGRAM ###

print "Content-type: text/html\n\n"

# Error logging
import cgitb
cgitb.enable(display = 0, logdir = "./errors")

import json


data = json.load(open("users.json", "r"))

active = {}

for user_id, user in data.iteritems():
    if "account_id" in user and "timed_penalty_date" not in user:
        active[str(user_id)] = user
                    
# Generate formatted output
import HTML

table = []

table.append([HTML.TableCell("Active", header=True, valign="middle", attribs={"colspan":4})])
for user in active.itervalues():
    table.append(["<img src=\"%s\" alt=\"Gravatar\"></img>" % (user["profile_image"]),
                  "<a href=\"%s\">%s</a>" % (user["link"], user["display_name"]),
                  "user_id: %s" % (user["user_id"]),
                  "user_type: %s" % (user["user_type"])])

print ("""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <title>Windows 8 Challenge Stats - active users</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <script type="text/javascript">
            var _gaq = _gaq || [];
            _gaq.push(['_setAccount', 'UA-35935769-1']);
            _gaq.push(['_trackPageview']);
            
            (function() {
                var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
                ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
                var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
            })();
        </script>
    </head>
    <body>
        <p>
            """ + print open("navigation.html").read() + """
        </p>
        <p>
            This page lists users who answered [windows-8] questions during the <a href="http://win8challenge.com">Windows 8 Challenge</a> hosted by Super User/Stack Exchange. This site is not affiliated with Super User or Stack Exchange in any way. All data is obtained through the Stack Exchange API. Any questions, suggestions, problems, etc., should go to the <a href="http://meta.superuser.com/questions/5801/so-heres-a-stats-site-for-the-challenge">post</a> on Meta Super User.
        </p>
        <p>
            Users who were still active following the cheater purge are listed here. The order is random. Not all users would have qualified for the challenge; only those who posted during the time period are counted. Some winners (especially of level 1/2) may not be shown, since they may have won on upvotes from older posts (NB: I'm not sure whether such upvotes actually count).
        </p>
        <p>
            <b>Only posts created since the challenge started (2012-10-19) are counted. Posts after challenge end (2012-11-09) are not counted. Any user who got at least one upvote on a [windows-8] post in that time period are counted.</b>
        </p>
""" + HTML.table(table) + """
        <p>
            <a href="/">Home page</a>
        <p>
    </body>
</html>
""").encode("utf-8") # Some names may be in unicode
    
