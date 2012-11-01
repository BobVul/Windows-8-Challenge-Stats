#! /usr/bin/env python

# Overrides the builtin float and int classes to provide divide by zero support for floats.
# Divisions by zero return float("NaN").

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

import __builtin__

class float(__builtin__.float):
    def __div__(self, other):
        if other == 0:
            return float("NaN")
        else:
            return __builtin__.float.__div__(self, other)

class int(__builtin__.int):
    def __div__(self, other):
        if isinstance(other, __builtin__.float) and other == 0:
            return float("NaN")
        else:
            return __builtin__.int.__div__(self, other)

# Does not work; the builtin is used instead of str(). Find a way to replace builtin?
# Not necessary any more, since using float("NaN") now instead of str("NaN")?
"""
class str(__builtin__.str):
    def __div__(self, other):
        print self, other
        if self == "NaN" and (isinstance(other, __builtin__.float) or other == "NaN"):
            return "NaN"
        else:
            raise TypeError("unsupported operand type(s) for /: 'str' and 'float'")
"""
