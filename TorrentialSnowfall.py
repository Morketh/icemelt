
#
# Name: TorrentialSnowfall
# Purpose: Pulls toon info directly from Blizzard using the icemelt Guild roster
# Copyright (C) Andrew Malone 2015
#


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
import urllib2
from BeautifulSoup import BeautifulSoup

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

print "Activating weather patterns"
sleep(2)

os.system("clear")
print "Activating Automated Surface Observation System (ASOS)"
print "Initilizing Torrential Snow Fall Subroutines"
print "Preparing Multipoint Thermocouple Assemblies"

db = MySQLdb.connect(_IN_MYSQL_HOST_,_IN_MYSQL_USR_,_IN_MYSQL_PASS_,_IN_MYSQL_DB_)
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database Version Info: %s " % data
db.close()

# main work horse for the weather control system
# SELECT `index`,`realm`,`guild` FROM `guilds`;
# SELECT COUNT(`index`) AS 'total' FROM `guilds`;

# we want NULL status. As we get Page-Not-Found (404) errors we will be updating the database so we can filter out removed guilds
# this also helps us update guild rosters more effciantly in the future
# a status of 200 means FOUND and we can just UPDATE data
# NULL will be used for not processed
# anything else will be asumed as not found
_REALM_ = "SELECT `index`,`region_id`,`realm`,`guild` FROM `guilds` WHERE `status` IS NULL;"
_INDEX_TOTAL_ = "SELECT COUNT(`index`) AS 'total' FROM `guilds` WHERE `status` IS NULL;"

icemelt = MySQLdb.connect(_IN_MYSQL_HOST_,_IN_MYSQL_USR_,_IN_MYSQL_PASS_,_IN_MYSQL_DB_)
cursor = icemelt.cursor()