#! /usr/bin/env python

# Converts two times (as seconds) into a text string of the form
# "x hours, y minutes and z seconds", dropping any zeroes.

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

def TimeDiffString(t1=0, t2=0):
    diff = abs(t1 - t2)

    hours = diff / 3600
    minutes = (diff % 3600) / 60
    seconds = diff % 60
    
    return (("%d hour%s%s" % (hours, "s" if hours > 1 else "", ", " if minutes else " and " if seconds else "")) if hours else "") + \
           (("%d minute%s%s" % (minutes, "s" if minutes > 1 else "", " and " if seconds else "")) if minutes else "") + \
           (("%d second%s" % (seconds, "s" if seconds > 1 else "")) if seconds else "")
