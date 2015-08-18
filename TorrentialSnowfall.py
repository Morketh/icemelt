#!/usr/bin/python
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
import ConfigParser

subprocess.call('clear')
print "Welcome: " + getpass.getuser()
print "Project Icemelt Copyright (C) 2015 Andrew Malone"

# Configuration Import

print "Activating weather patterns"
print "Activating Automated Surface Observation System (ASOS)"
print "Initilizing Torrential Snow Fall Subroutines"
print "Preparing Multipoint Thermocouple Assemblies"

db = MySQLdb.connect(config._IN_MYSQL_HOST_,config._IN_MYSQL_USR_,config._IN_MYSQL_PASS_,config._IN_MYSQL_DB_)
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

# CODE GOES HERE


cursor.close()
icemelt.close()
