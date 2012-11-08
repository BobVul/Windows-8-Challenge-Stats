#! /usr/bin/env python

# Calculates data for a column in the results table and adds said column to the table.
# Should be run as a cron job to avoid hammering the API.
# Every 5 minutes is the recommended maximum.

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

import HTML

from DivideByZero import *

class MainData():
    def __init__(self, questions, answers):
        self.q = questions
        self.a = answers

    def num(self):
        return len(self.q) + len(self.a)

    def num_q(self):
        return len(self.q)

    def num_a(self):
        return len(self.a)

    def aqratio(self):
        return float(self.num_a()) / float(self.num_q())

    def avgscore(self):
        return float(sum([x["score"] for x in (self.q + self.a)])) / float(self.num())

    def avgscore_q(self):
        return float(sum([x["score"] for x in (self.q)])) / float(self.num_q())

    def avgscore_a(self):
        return float(sum([x["score"] for x in (self.a)])) / float(self.num_a())
    
    def highestscore(self):
        if not self.q + self.a:
            return float("NaN")
        else:
            return max([x["score"] for x in (self.q + self.a)])

    def highestscore_q(self):
        if not self.q:
            return float("NaN")
        else:
            return max([x["score"] for x in (self.q)])

    def highestscore_a(self):
        if not self.a:
            return float("NaN")
        else:
            return max([x["score"] for x in (self.a)])
    
    

class ColData():
    def __init__(self, questions, answers, filteredquestions, filteredanswers):
        self.total = MainData(questions, answers)
        self.filtered = MainData(filteredquestions, filteredanswers)

    def num(self, proportion=False):
        if proportion:
            return float(self.filtered.num()) / float(self.total.num())
        else:
            return self.filtered.num()

    def num_q(self, proportion=False):
        if proportion:
            return float(self.filtered.num_q()) / float(self.total.num_q())
        else:
            return self.filtered.num_q()

    def num_a(self, proportion=False):
        if proportion:
            return float(self.filtered.num_a()) / float(self.total.num_a())
        else:
            return self.filtered.num_a()

    def aqratio(self, proportion=False):
        faqratio = self.filtered.aqratio()
        if faqratio == 0:
            return 0
        if proportion:
            taqratio = self.total.aqratio()
            return float(faqratio) / float(taqratio)
        else:
            return faqratio

    def avgscore(self, proportion=False):
        favgscore = self.filtered.avgscore()
        tavgscore = self.total.avgscore()
        if favgscore == 0:
            return 0
        if proportion:
            return float(favgscore) / float(tavgscore)
        else:
            return favgscore

    def avgscore_q(self, proportion=False):
        favgscore = self.filtered.avgscore_q()
        tavgscore = self.total.avgscore_q()
        if favgscore == 0:
            return 0
        if proportion:
            return float(favgscore) / float(tavgscore)
        else:
            return favgscore

    def avgscore_a(self, proportion=False):
        favgscore = self.filtered.avgscore_a()
        tavgscore = self.total.avgscore_a()
        if favgscore == 0:
            return 0
        if proportion:
            return float(favgscore) / float(tavgscore)
        else:
            return favgscore

    def highestscore(self, proportion=False):
        fhighestscore = self.filtered.highestscore()
        thighestscore = self.total.highestscore()
        if proportion:
            return float(fhighestscore) / float(thighestscore)
        else:
            return fhighestscore
        
    def highestscore_q(self, proportion=False):
        fhighestscore = self.filtered.highestscore_q()
        thighestscore = self.total.highestscore_q()
        if proportion:
            return float(fhighestscore) / float(thighestscore)
        else:
            return fhighestscore

    def highestscore_a(self, proportion=False):
        fhighestscore = self.filtered.highestscore_a()
        thighestscore = self.total.highestscore_a()
        if proportion:
            return float(fhighestscore) / float(thighestscore)
        else:
            return fhighestscore

import HTML

class FillCols():
    @staticmethod
    def FillCounts(table, calc, title):
        table[0].append(HTML.TableCell(title, header=True))
        table[1].append(calc.num())
        table[2].append(calc.num_q())
        table[3].append(calc.num_a())
        table[4].append(FillCols.FloatToString(calc.aqratio()))
        table[5].append(FillCols.FloatToString(calc.avgscore()))
        table[6].append(FillCols.FloatToString(calc.avgscore_q()))
        table[7].append(FillCols.FloatToString(calc.avgscore_a()))
        table[8].append(FillCols.FloatToString(calc.highestscore()))
        table[9].append(FillCols.FloatToString(calc.highestscore_q()))
        table[10].append(FillCols.FloatToString(calc.highestscore_a()))

    @staticmethod
    def FillCountsAndPercentages(table, calc, title):
        table[0].append(HTML.TableCell(title, header=True))
        table[1].append("%s (%s%%)" % (calc.num(), FillCols.FloatToString(calc.num(proportion=True) * 100)))
        table[2].append("%s (%s%%)" % (calc.num_q(), FillCols.FloatToString(calc.num_q(proportion=True) * 100)))
        table[3].append("%s (%s%%)" % (calc.num_a(), FillCols.FloatToString(calc.num_a(proportion=True) * 100)))
        table[4].append("%s (%s%%)" % (FillCols.FloatToString(calc.aqratio()), FillCols.FloatToString(calc.aqratio(proportion=True) * 100)))
        table[5].append("%s (%s%%)" % (FillCols.FloatToString(calc.avgscore()), FillCols.FloatToString(calc.avgscore(proportion=True) * 100)))
        table[6].append("%s (%s%%)" % (FillCols.FloatToString(calc.avgscore_q()), FillCols.FloatToString(calc.avgscore_q(proportion=True) * 100)))
        table[7].append("%s (%s%%)" % (FillCols.FloatToString(calc.avgscore_a()), FillCols.FloatToString(calc.avgscore_a(proportion=True) * 100)))
        table[8].append("%s (%s%%)" % (FillCols.FloatToString(calc.highestscore()), FillCols.FloatToString(calc.highestscore(proportion=True) * 100)))
        table[9].append("%s (%s%%)" % (FillCols.FloatToString(calc.highestscore_q()), FillCols.FloatToString(calc.highestscore_q(proportion=True) * 100)))
        table[10].append("%s (%s%%)" % (FillCols.FloatToString(calc.highestscore_a()), FillCols.FloatToString(calc.highestscore_a(proportion=True) * 100)))

    @staticmethod
    def FloatToString(num, decimalplaces=2):
        a = list("%.*f" % (decimalplaces, num))
        a.reverse()
        while (len(a) > 1) and ("." in a) and (a[0] == "0" or a[0] == "."):
            del a[0]
        a.reverse()
        return "".join(a)
