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
import shlex
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

subprocess.call('clear')
print "Welcome: " + getpass.getuser()
print "Project Icemelt Copyright (C) 2015 Andrew Malone"
print "Resuming in 5 seconds"
sleep(5)

_IN_MYSQL_USR_ = raw_input('Database User Name [icemelt]: ')
if _IN_MYSQL_USR_ == '':
        _IN_MYSQL_USR_ = 'icemelt' #defualt user name

_IN_MYSQL_PASS_ = raw_input('password for '+_IN_MYSQL_USR_+' [icemelt]: ')
if _IN_MYSQL_PASS_ == '':
        _IN_MYSQL_PASS_ = 'icemelt' #defualt password

_IN_MYSQL_HOST_ = raw_input('Database Host Name [localhost]: ')
if _IN_MYSQL_HOST_ == '':
        _IN_MYSQL_HOST_ = 'localhost' #defualt hostname

_IN_MYSQL_PORT_ = raw_input('Database Port Number [3306]: ')
if _IN_MYSQL_PORT_ == '':
        _IN_MYSQL_PORT_ = '3306' #defualt mysql port number

_IN_MYSQL_DB_ = raw_input('MySQL database to use [icemelt]: ')
if _IN_MYSQL_DB_ == '':
        _IN_MYSQL_DB_ = 'icemelt' #defualt mysql database


db = MySQLdb.connect(_IN_MYSQL_HOST_,_IN_MYSQL_USR_,_IN_MYSQL_PASS_,_IN_MYSQL_DB_)
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version: %s " % data
db.close()

print "Activating weather patterns"
sleep(2)

os.system("clear")
print "Activating White-Out weather conditions"
print "Initilizing Torrential Snow Fall Subroutines"
print "Preparing Multipoint Thermocouple Assemblies"

# main work horse for the weather control system
# SELECT `index`,`realm`,`guild` FROM `guilds`;
# SELECT COUNT(`index`) AS 'total' FROM `guilds`;

_REALM_ = "SELECT `index`,`realm`,`guild` FROM `guilds`;"
_INDEX_TOTAL_ = "SELECT COUNT(`index`) AS 'total' FROM `guilds`;"

icemelt = MySQLdb.connect(_IN_MYSQL_HOST_,_IN_MYSQL_USR_,_IN_MYSQL_PASS_,_IN_MYSQL_DB_)
cursor = icemelt.cursor()

# grab total entries
cursor.execute(_INDEX_TOTAL_)
for (total,) in cursor:
  print "Total Guilds found: "+str(total)
  bar = progressbar.ProgressBar(maxval=int(total), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()]).start()

# grab realm data
cursor.execute(_REALM_)

for (index,realm,guild) in ResultIter(cursor):
 bar.update(index)
 
 # This will call a subprocess and then WAIT for that to finish before activating a new one this way we can make sure data is in the right order and that Blizzard wont lock us out of the page
 call(shlex.split("./TorrentialSnowfall.sh "+realm+" "+guild.replace(" ", "_")+" "+str(index)+" "+_IN_MYSQL_USR_+" "+_IN_MYSQL_PASS_+" "+_IN_MYSQL_HOST_+" "+_IN_MYSQL_PORT_+" "+_IN_MYSQL_DB_))
 
 #print"./TorrentialSnowfall.sh "+realm+" "+guild.replace(" ", "_")+" "+str(index)+" "+_IN_MYSQL_USR_+" "+_IN_MYSQL_PASS_+" "+_IN_MYSQL_HOST_+" "+_IN_MYSQL_PORT_+" "+_IN_MYSQL_DB_

cursor.close()
icemelt.close()
