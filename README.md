Windows-8-Challenge-Stats
=========================

Scripts for generating stats for the Super User Windows 8 Challenge

Currently hosted at http://win8challengestats.co.cc

---

#Licensing

## Main code

Copyright 2012 Bob Rao

Licensed under the GNU GPLv3

* stats.py

 Start point. Takes user input and generates output HTML.

* CalcCols.py

 Calculates data for a column in the results table and adds said column to the table.

* DivideByZero.py

 Overrides the builtin float and int classes to provide divide by zero support for floats. Divisions by zero return float("NaN").

* GetData.py

 Downloads data from the StackExchange API, applies the appropriate filtering and saves to a file (`data.json`).
 
 Should be run as a cron job, to avoid hammering the API. Every 5 minutes is the recommended maximum.

* TimeDiff.py

 Converts two times (as seconds) into a text string of the form "x hours, y minutes and z seconds", dropping any zeroes.

## Other modules

###HTML.py
Copyright Philippe Lagadec
> HTML.py - v0.04 2009-07-28 Philippe Lagadec

> This module provides a few classes to easily generate HTML code such as tables
> and lists.

> Project website: http://www.decalage.info/python/html

> License: CeCILL (open-source GPL compatible), see source code for details.
>          http://www.cecill.info