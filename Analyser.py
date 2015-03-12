#!/usr/bin/python

import time
from datetime import date, datetime
import json #read json files
import glob #iterate over files in folder
import os #we need to see current working directory.  

files = glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/*.json')

weeks = {}
weekdays = {}

for f in files:
    for item in json.load(open(f)):
        # need only date, no time
        com_date = item['commit']['committer']['date'].split('T', 1) 
        com_date = com_date[0].split('-')

        
        year = int(com_date[0])
        month = int(com_date[1])
        day = int(com_date[2])
        com_date = date(year, month, day).isocalendar() # this will give you the year week day
        # week numbers
        try:
            weeks[com_date[1]] = weeks[com_date[1]] + 1 #filling weeks object.  
            #
        except KeyError:
            weeks[com_date[1]] = 1

        # weekdays
        try:
            weekdays[com_date[2]] = weekdays[com_date[2]] + 1
        except KeyError:
            weekdays[com_date[2]] = 1

most_productive_week = max(weeks, key=weeks.get) #key gets the value rather than the key
most_productive_weekday = max(weekdays, key=weekdays.get)
print

print('Most productive week in 2014: ' + str(most_productive_week) + ' had ' + str(weeks[most_productive_week]) + ' commits.')
print('Most productive weekday in 2014: ' + str(most_productive_weekday) + ' with ' + str(weekdays[most_productive_weekday]) + ' commits.')