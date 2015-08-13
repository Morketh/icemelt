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

# we want NULL status. As we get Page-Not-Found (404) errors we will be updating the database so we can filter out removed guilds
# this also helps us update guild rosters more effciantly in the future
_REALM_ = "SELECT `index`,`region_id`,`realm`,`guild` FROM `guilds` WHERE `status` IS NULL;"
_INDEX_TOTAL_ = "SELECT COUNT(`index`) AS 'total' FROM `guilds` WHERE `status` IS NULL;"

icemelt = MySQLdb.connect(_IN_MYSQL_HOST_,_IN_MYSQL_USR_,_IN_MYSQL_PASS_,_IN_MYSQL_DB_)
cursor = icemelt.cursor()

# grab total entries
cursor.execute(_INDEX_TOTAL_)
cursor.fetchone()
for (total,) in cursor:
 print "Total Guilds found: "+str(total)
 bar = progressbar.ProgressBar(maxval=int(total), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()]).start()

# grab realm data
cursor.execute(_REALM_)

for (index,region_id,realm,guild) in cursor:
 url="http://us.battle.net/wow/"+region_id+"/guild/"+realm+"/"+guild.replace(" ", "_")+"/roster"
 req = urllib2.Request(url)
 bar.update(index)

 try:
     response = urllib2.urlopen(req)
 except urllib2.HTTPError as e:
     sql = "UPDATE `guilds` SET `status`=%s WHERE  `index`=%s"
     cursor.execute(sql,[e.code,index])
     icemelt.commit()
     #print(url,e.code)
     #print(e.code)
 except urllib2.URLError, e:
     print 'We failed to reach the server.'
     print 'Reason: ', e.reason
 else:    
     soup = BeautifulSoup(response.read())
     x = (len(soup.findAll('tr')) - 1)
     for row in soup.findAll('tr')[1:x]:
      col = row.findAll('td')
      name = col[0].getText()
      level = col[3].getText()
      _SQL_ = "INSERT INTO `chars` (`gid`, `rid`, `toon_name`, `lvl`, `realm`) VALUES (%s, %s, %s, %s, %s)" 
      sql_data = [index,region_id,name,level,realm]
      #print _SQL_ % sql_data
      cursor.execute(_SQL_,sql_data)
      icemelt.commit()
 #print"./TorrentialSnowfall.sh "+realm+" "+guild.replace(" ", "_")+" "+str(index)+" "+_IN_MYSQL_USR_+" "+_IN_MYSQL_PASS_+" "+_IN_MYSQL_HOST_+" "+_IN_MYSQL_PORT_+" "+_IN_MYSQL_DB_

_GUILD_STATS_ = "SELECT COUNT(DISTINCT `index`) AS 'total',`status` FROM `guilds` GROUP BY `status`;"
_REALM_POPULATION_ = "SELECT COUNT(DISTINCT `cid`) AS 'Total Toons',`realm` FROM `chars` GROUP BY `realm` ORDER BY `Total Toons` DESC;"

# Provide Guild Found Statistics on finishing up additions to the DB

print " " #new line to get the stats out of the progress bar
print "Guild statistics:"
cursor.execute(_GUILD_STATS_)
icemelt.commit()

results = cursor.fetchall()

widths = []
columns = []
tavnit = '|'
separator = '+' 

for cd in cursor.description:
    widths.append(max(cd[2], len(cd[0])))
    columns.append(cd[0])

for w in widths:
    tavnit += " %-"+"%ss |" % (w,)
    separator += '-'*w + '--+'

print(separator)
print(tavnit % tuple(columns))
print(separator)
for row in results:
    print(tavnit % row)
print(separator)

# Provide a Realm population on finishing up additions to the DB

print "Population by Realm:"
cursor.execute(_REALM_POPULATION_)
icemelt.commit()

results = cursor.fetchall()

widths = []
columns = []
tavnit = '|'
separator = '+'

for cd in cursor.description:
    widths.append(max(cd[2], len(cd[0])))
    columns.append(cd[0])

for w in widths:
    tavnit += " %-"+"%ss |" % (w,)
    separator += '-'*w + '--+'

print(separator)
print(tavnit % tuple(columns))
print(separator)
for row in results:
    print(tavnit % row)
print(separator)

cursor.close()
icemelt.close()
