#! /usr/bin/env python

# Gets details for all users who are competing

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

# `time.sleep` to deal with backoff requests
import time

# Process iterable in chunks
import itertools

# stdout flush for progress
import sys

site = "superuser"
apiurl = "http://api.stackexchange.com/2.1"
key = "X9lcjCphRxyStgisCgaFBw(("

data = json.load(open("data.json", "r"))

fetchtime = data["time"]
questions = data["questions"]
answers = data["answers"]
shallow_users = {}

for question in questions:
    if question["up_vote_count"] > 0 and "user_id" in question["owner"]:
        shallow_users[str(question["owner"]["user_id"])] = question["owner"]

for answer in answers:
    if answer["up_vote_count"] > 0 and "user_id" in answer["owner"]:
        shallow_users[str(answer["owner"]["user_id"])] = answer["owner"]

users = dict((str(user_id), shallow_users[str(user_id)]) for user_id in shallow_users)

# Process in chunks of 100
for user_id_chunk in itertools.izip_longest(*[shallow_users.iterkeys()]*100):
    request = urllib2.Request(apiurl + "/users/" +
                              ";".join(str(user_id) for user_id in user_id_chunk if user_id is not None) +
                              "?key=" + key +
                              "&site=" + site +
                              "&pagesize=100")
    request.add_header("Accept-encoding", "gzip")
    
    print "Fetching " + request.get_full_url()
    sys.stdout.flush()

    # Assume always gzipped, as per SE API documentation
    gzippedresponse = urllib2.urlopen(request)
    response = gzip.GzipFile(fileobj=StringIO.StringIO(gzippedresponse.read())).read()
    
    # Convert the JSON response to a Python object
    wrapper = json.loads(response)

    if "error_id" in wrapper:
        raise Exception("error_id: %d;error_name: %s; error_message: %s" \
                        % (wrapper["error_id"], wrapper["error_name"], wrapper["error_message"]))
    
    for user in wrapper["items"]:
        users[str(user["user_id"])] = user
        
    if "backoff" in wrapper:
        print "Backing off for %d seconds" % wrapper["backoff"]
        sys.stdout.flush()
        time.sleep(int(wrapper["backoff"]))
        
open("users.json", "w").write(json.dumps(users))