#! /usr/bin/env python

# Start point. Takes user input and generates output HTML.

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

import cgi

import json

from DivideByZero import *

form = cgi.FieldStorage()
if "user_ids" in form.keys():
    # Max of 10, so split a max of 9 times
    user_ids = [x.strip() for x in form["user_ids"].value.split(",", 9)]
    if len(user_ids) == 10:
        user_ids[9], temp, temp = user_ids[9].partition(",")
        user_ids[9] = user_ids[9].strip()
# Original key name, kept for compatibility with saved links
elif "user_id" in form.keys():
    user_ids = [x.strip() for x in form["user_id"].value.split(",", 9)]
    if len(user_ids) == 10:
        user_ids[9], temp, temp = user_ids[9].partition(",")
        user_ids[9] = user_ids[9].strip()
else:
    user_ids = None

show = {
    "total" : False,
    "open" : False,
    "closed" : False,
    "proportions" : False
}

if "show" in form.keys():
    for key in form.getlist("show"):
        show[key] = True
else:
    show = {
        "total" : False,
        "open" : True,
        "closed" : False,
        "proportions" : True
    }


data = json.load(open("data.json", "r"))

fetchtime = data["time"]
questions = data["questions"]
answers = data["answers"]
oquestions = [] # open answers
oanswers = [] # open questions
cquestions = [] # closed questions
canswers = [] # closed answers


# Only user ids in user_ids are guaranteed be in these dictionaries
uquestions = {} # questions by user id
uanswers = {} # answers by user id
uoquestions = {}
uoanswers = {}
ucquestions = {}
ucanswers = {}
display_names = {} # display names by user id

if user_ids:
    for user_id in user_ids:
        uquestions[user_id] = []
        uanswers[user_id] = []
        uoquestions[user_id] = []
        uoanswers[user_id] = []
        ucquestions[user_id] = []
        ucanswers[user_id] = []
        display_names[user_id] = ""

# Build open/closed lists
for question in questions:        
    if "closed_date" in question:
        cquestions.append(question)
        if "answers" in question:
            for answer in question["answers"]:
                canswers.append(answer)
    else:
        oquestions.append(question)
        if "answers" in question:
            for answer in question["answers"]:
                    oanswers.append(answer)

# Build user lists

# ufanswers should be either ucanswers or uoanswers
def BuildUserLists_ProcessAnswerList(answers, uanswers, ufanswers, display_names):
    for answer in answers:
        if "owner" in answer:
            if "user_id" not in answer["owner"]:
                if "nonexistent" in user_ids:
                    uanswers["nonexistent"].append(answer)
                    ufanswers["nonexistent"].append(answer)
                        
            elif str(answer["owner"]["user_id"]) in user_ids:
                uanswers[str(answer["owner"]["user_id"])].append(answer)
                ufanswers[str(answer["owner"]["user_id"])].append(answer)
                display_names[str(answer["owner"]["user_id"])] = answer["owner"]["display_name"]

if user_ids:
    for question in questions:
        if "owner" in question:
            if "user_id" not in question["owner"]:
                if "nonexistent" in user_ids:
                    uquestions["nonexistent"].append(question)
                    if "closed_date" in question:
                        ucquestions["nonexistent"].append(question)
                    else:
                        uoquestions["nonexistent"].append(question)
                        
            elif str(question["owner"]["user_id"]) in user_ids:
                uquestions[str(question["owner"]["user_id"])].append(question)
                if "closed_date" in question:
                    ucquestions[str(question["owner"]["user_id"])].append(question)
                else:
                    uoquestions[str(question["owner"]["user_id"])].append(question)
                display_names[str(question["owner"]["user_id"])] = question["owner"]["display_name"]

        # Must process when iterating through the question, else it's difficult
        # to tell if the question the answer belongs to is closed
        if "answers" in question:
            if "closed_date" in question:
                BuildUserLists_ProcessAnswerList(question["answers"], uanswers, ucanswers, display_names)
            else:
                BuildUserLists_ProcessAnswerList(question["answers"], uanswers, uoanswers, display_names)
            
                    
# Generate formatted output
import HTML
# Add timestamp
import time
import datetime
import TimeDiff
curtime = int(time.mktime(datetime.datetime.now().timetuple()))

table = []

table.append([HTML.TableCell(None, header=True)]) #header
table.append([HTML.TableCell("Post count", header=True)])
table.append([HTML.TableCell("Question count", header=True)])
table.append([HTML.TableCell("Answer count", header=True)])
table.append([HTML.TableCell("Answer to question ratio", header=True)])
table.append([HTML.TableCell("Average score per post", header=True)])
table.append([HTML.TableCell("Average score per question", header=True)])
table.append([HTML.TableCell("Average score per answer", header=True)])
table.append([HTML.TableCell("Highest score overall", header=True)])
table.append([HTML.TableCell("Highest score on a question", header=True)])
table.append([HTML.TableCell("Highest score on an answer", header=True)])

import CalcCols

if show["total"]:
    CalcCols.FillCols.FillCounts(table, CalcCols.MainData(questions, answers), "All posts")

if show["open"]:
    if show["proportions"]:
        CalcCols.FillCols.FillCountsAndPercentages(table, CalcCols.ColData(questions, answers, oquestions, oanswers), "Open posts (% of total)")
    else:
        CalcCols.FillCols.FillCounts(table, CalcCols.MainData(oquestions, oanswers), "Open posts")

if show["closed"]:
    if show["proportions"]:
        CalcCols.FillCols.FillCountsAndPercentages(table, CalcCols.ColData(questions, answers, cquestions, canswers), "Closed posts (% of total)")
    else:
        CalcCols.FillCols.FillCounts(table, CalcCols.MainData(cquestions, canswers), "Closed posts")

if user_ids:
    for user_id in user_ids:
        if show["total"]:
            CalcCols.FillCols.FillCounts(table, CalcCols.MainData(uquestions[user_id], uanswers[user_id]), "All posts by %s, %s" % (user_id, display_names[user_id] if display_names[user_id] else "No Display Name"))

        if show["open"]:
            if show["proportions"]:
                CalcCols.FillCols.FillCountsAndPercentages(table, CalcCols.ColData(uquestions[user_id], uanswers[user_id], uoquestions[user_id], uoanswers[user_id]), "Open posts (%% of total) by %s, %s" % (user_id, display_names[user_id] if display_names[user_id] else "No Display Name"))
            else:
                CalcCols.FillCols.FillCounts(table, CalcCols.MainData(uoquestions[user_id], uoanswers[user_id]), "Open posts by %s, %s" % (user_id, display_names[user_id] if display_names[user_id] else "No Display Name"))

        if show["closed"]:
            if show["proportions"]:
                CalcCols.FillCols.FillCountsAndPercentages(table, CalcCols.ColData(uquestions[user_id], uanswers[user_id], ucquestions[user_id], ucanswers[user_id]), "Closed posts (%% of total) by %s, %s" % (user_id, display_names[user_id] if display_names[user_id] else "No Display Name"))
            else:
                CalcCols.FillCols.FillCounts(table, CalcCols.MainData(ucquestions[user_id], ucanswers[user_id]), "Closed posts by %s, %s" % (user_id, display_names[user_id] if display_names[user_id] else "No Display Name"))


print ("""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <title>Windows 8 Challenge Stats</title>
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
            <b>The challenge has ended! These stats will no longer be updated.</b>
        </p>
        <hr>
        <p>
            This page is an attempt to compile and display some real-time stats on [windows-8] questions asked during the <a href="http://win8challenge.com">Windows 8 Challenge</a> hosted by Super User/Stack Exchange. This site is not affiliated with Super User or Stack Exchange in any way. All data is obtained through the Stack Exchange API. Any questions, suggestions, problems, etc., should go to the <a href="http://meta.superuser.com/questions/5801/so-heres-a-stats-site-for-the-challenge">post</a> on Meta Super User.
        </p>
        <p>
            <b>Only posts created since the challenge started (2012-10-19) are counted. Posts after challenge end (2012-11-09) are not counted.</b>
        </p>
""" + HTML.table(table) + """
        <form name="selectuser" action="/cgi-bin/stats.py" method="get">
            <p>
                Filter specific user: <br>
                user_id (separate with commas, max 10): <input type="text" name="user_ids" value=\"""" + (",".join(user_ids) if user_ids else "") + """\"> 
            </p>
            <table>
                <tr><td>show:</td><td><input type="checkbox" name="show" value="total" """ + ("checked" if show["total"] else "") + """>total</td></tr>
                <tr><td></td><td><input type="checkbox" name="show" value="open" """ + ("checked" if show["open"] else "") + """>open</td></tr>
                <tr><td></td><td><input type="checkbox" name="show" value="closed" """ + ("checked" if show["closed"] else "") + """>closed</td></tr>
                <tr><td></td><td><input type="checkbox" name="show" value="proportions" """ + ("checked" if show["proportions"] else "") + """>proportion to total</td></tr>
            </table>
            <p>
                <input type="submit" value="Submit">
            </p>
        </form>
        <p>
            Or <a href="/cgi-bin/stats.py?user_id=nonexistent">filter posts with no linked user</a> by using the id 'nonexistent'.
        </p>
        <p>
""" + "        Data last fetched %s (%s ago)"
                                 % (time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(fetchtime)),
                                    TimeDiff.TimeDiffString(curtime, fetchtime)) + """
        </p>
        <p>
            <small><a href="/cgi-bin/stats.py?user_ids=36744%2C10165%2C163760%2Cnonexistent%2Cru3tuxf&amp;show=total&amp;show=open&amp;show=closed&amp;show=proportions">test page</a></small>
        </p>
    </body>
</html>
""")
    
