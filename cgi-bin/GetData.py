#! /usr/bin/env python

# Downloads data from the StackExchange API, applies the appropriate filtering
# and saves to a file (`data.json`).

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

print "Content-type: text/plain\n\n"

# Error logging
import cgitb
cgitb.enable(display = 0, logdir = "./errors")

# API request
import urllib2

# API response to Python object
import json

# Decode API response
import gzip
import StringIO

# `fromdate` in API request, `time.sleep` to deal with backoff requests
import datetime
import time

# stdout flush for progress
import sys

### ###

# Querystring values
site = "superuser"
fromdate = int(time.mktime(datetime.date(2012, 10, 19).timetuple()))
tagged = "windows-8"
apiurl = "http://api.stackexchange.com/2.1"
key = "X9lcjCphRxyStgisCgaFBw(("
qafilter = "!5UDW(BsW)nWjKEHJ5ohnay5IoZss4sVN7T6o7wJCC" # Filter for questions and answers

def GetData():
    questions = []
    answers = []
    
    has_more = True # are there more pages? bool value returned by API
    page = 1 # start page
    
    print "Requesting 100 questions per page"
    sys.stdout.flush()
    
    while has_more:
        print "Requesting page %d" % page
        sys.stdout.flush()
        
        # Build the query
        request = urllib2.Request(apiurl + "/questions?key=" + key + \
                                  "&filter=" + qafilter + \
                                  "&site=" + site + \
                                  "&tagged=" + tagged + \
                                  "&pagesize=100" \
                                  "&page=" + str(page))
        request.add_header("Accept-encoding", "gzip")

        # Assume always gzipped, as per SE API documentation
        gzippedresponse = urllib2.urlopen(request)
        response = gzip.GzipFile(fileobj=StringIO.StringIO(gzippedresponse.read())).read()

        # Convert the JSON response to a Python object
        wrapper = json.loads(response)

        if "error_id" in wrapper:
            raise Exception("error_id: %d;error_name: %s; error_message: %s" \
                            % (wrapper["error_id"], wrapper["error_name"], wrapper["error_message"]))

        has_more = wrapper["has_more"]

        for question in wrapper["items"]:
            if question["creation_date"] >= fromdate:
                questions.append(question)

            if "answers" in question:
                for answer in question["answers"]:
                    if answer["creation_date"] >= fromdate:
                        answers.append(answer)

        if has_more and "backoff" in wrapper:
            print "Backing off for %d seconds" % wrapper[backoff]
            sys.stdout.flush()
            time.sleep(backoff)

        page += 1

    return (questions, answers)

(questions, answers) = GetData()

# Add timestamp
import time

open("data.json", "w").write(json.dumps({
    "time" : int(time.mktime(datetime.datetime.now().timetuple())),
    "questions" : questions,
    "answers" : answers}))
