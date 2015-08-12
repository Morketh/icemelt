#!/usr/bin/python

#
# Title: Cold-Air-Funnel
# Purpose: Pulls guilds and realms out of icemelt DB and preps the TorrentialSnowFall script
#
# Copyright (C) Andrew Malone 2015
from __future__ import generators    # needs to be at the top of your module
import MySQLdb
import os
from subprocess import call
import os
import subprocess
import sys
import getpass
from time import sleep
import progressbar

#
# we need to add a group select to mysql calls
# 
def ResultIter(cursor, arraysize=50):
    'An iterator that uses fetchmany to keep memory usage down'
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result





db = MySQLdb.connect("localhost","icemelt","icemelt","icemelt" )
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version : %s " % data
db.close()

print "Activating weather patterns"

# main work horse for the weather control system
# SELECT `realm` FROM `guilds` WHERE `index`=_INDEX_
# SELECT COUNT(`index`) AS 'indexes' FROM `guilds`;
# SELECT `guild` FROM `guilds` WHERE `index`=_INDEX_

_REALM_ = "SELECT `realm`,`guild` FROM `guilds`;"
_TOTAL_ = "SELECT COUNT(`index`) AS 'indexes' FROM `guilds`;"

icemelt = MySQLdb.connect("localhost","icemelt","icemelt","icemelt")
cursor = icemelt.cursor()

cursor.execute(_REALM_) # we always start at 1

for (realm,guild) in ResultIter(cursor):
 print("Guild: "+guild.replace(" ", "_")+" is on realm: "+realm)
 #os.system("./TorrentialSnowfall.sh "+realm+" "+guild.replace(" ", "_"))
cursor.close()
icemelt.close()
