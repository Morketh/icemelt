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
import urllib2
from BeautifulSoup import BeautifulSoup
import ConfigParser
from ice import config

subprocess.call('clear')
print("Project Icemelt Copyright (C) 2015 Andrew Malone")
print("Activating Torrential Snow fall subroutines: "+sys.argv[1])
# Configuration Import

# main work horse for the weather control system
# SELECT `index`,`realm`,`guild` FROM `guilds`;
# SELECT COUNT(`index`) AS 'total' FROM `guilds`;

# we want NULL status. As we get Page-Not-Found (404) errors we will be updating the database so we can filter out removed guilds
# this also helps us update guild rosters more effciantly in the future
# a status of 200 means FOUND and we can just UPDATE data
# NULL will be used for not processed
# anything else will be asumed as not found
icemelt = MySQLdb.connect(config._IN_MYSQL_HOST_,config._IN_MYSQL_USR_,config._IN_MYSQL_PASS_,config._IN_MYSQL_DB_)
cursor = icemelt.cursor()

cursor.execute("SELECT * FROM `icemelt`.`realms`")
# CODE GOES HERE
for (index,realm) in cursor:
 url="http://us.battle.net/wow/en/character/%s/%s/simple" % (realm,sys.argv[1])
 req = urllib2.Request(url)

 try:
     response = urllib2.urlopen(req)
 except urllib2.HTTPError as e:
     if e.code == 503: # we want to track 503's inorder to update those requests later (in the event we get any)
        sql = "INSERT INTO `chars` (`rid`, `toon_name`, `realm`, `status`) VALUES (5, %s,%s,%s);"
        sql_data = [sys.argv[1],realm,e.code]
        cursor.execute(sql,sql_data)
        icemelt.commit()
 except urllib2.URLError as e:
     print('We failed to reach the server.')
     print('Reason: ', e.reason)
 else: # must mean its 200 OK
     sql = "INSERT INTO `chars` (`rid`, `toon_name`, `realm`) VALUES (5, %s,%s);"
     sql_data = [sys.argv[1],realm]
     # out put the INSER sql
     #print "SQL: "+sql % (sys.argv[1],realm)
     cursor.execute(sql,sql_data)
     icemelt.commit()

cursor.close()
icemelt.close()
