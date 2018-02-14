#!/usr/bin/python

#
# Title: Cold-Air-Funnel, Stage 2 of
#
# Background: Ive been building and designing this script system based off of an idea from Katamitsu. 
# According to his research notes he can manualy crossrefrance any toon on a Bnet account based on Achevments and Pet battle data.
# taking this into account i have devised a series of scripts to "Crawl" through blizzards web page and mine out the data used for his
# toon refrance system. 
#
# Purpose: Pulls guilds and realms out of icemelt DB and preps the TorrentialSnowFall subroutines.
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
import ConfigParser
from ice import config

subprocess.call('clear')
print("Welcome: " + getpass.getuser())
print("Project Icemelt Copyright (C) 2015 Andrew Malone")
print("Resuming in 5 seconds")
sleep(5)

db = MySQLdb.connect(config._IN_MYSQL_HOST_,config._IN_MYSQL_USR_,config._IN_MYSQL_PASS_,config._IN_MYSQL_DB_)
cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("Database version: %s " % data)
sleep(5)
db.close()

print("Activating weather patterns")
sleep(2)

os.system("clear")
print("Activating White-Out weather conditions")
print("Initilizing Torrential Snow Fall Subroutines")
print("Preparing Multipoint Thermocouple Assemblies")

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

_BAR_TOTAL_ =  "SELECT COUNT(`index`) AS 'total' FROM `guilds`;"

icemelt = MySQLdb.connect(config._IN_MYSQL_HOST_,config._IN_MYSQL_USR_,config._IN_MYSQL_PASS_,config._IN_MYSQL_DB_)
cursor = icemelt.cursor()

# grab total entries
cursor.execute(_BAR_TOTAL_)

cursor.fetchone()
for (total,) in cursor:
 cursor.execute(_INDEX_TOTAL_)
 (index,) = cursor.fetchone()
 if (index,) > 0:
  print("Total Guilds not Processed: %s out of %s" % (str(index),str(total)))
  bar = progressbar.ProgressBar(maxval=int(total), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()]).start()
 else:
  print("All guilds seem to be have been entered into the data base")
  print("if you would like to UPDATE guild info please use the update tool")
# grab realm data
cursor.execute(_REALM_)

for (index,region_id,realm,guild) in cursor:
 region_query = "SELECT `name` FROM `regions` WHERE `id` = %s;"
 cursor.execute(region_query,region_id)
 rname = cursor.fetchone()
 url="http://us.battle.net/wow/"+''.join(rname)+"/guild/"+realm+"/"+guild.replace(" ", "_")+"/roster"
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
 except urllib2.URLError as e:
     print('We failed to reach the server.')
     print('Reason: ', e.reason)
 else:
     sql = "UPDATE `icemelt`.`guilds` SET `status`=%s, `fid`=%s WHERE  `index`=%s;"
     soup = BeautifulSoup(response.read())
     x = (len(soup.findAll('tr')) - 1)
     faction = soup.findAll(attrs={'class':"faction"})
     for r in faction:
       if r.string == "Horde":
	_F_ID_ = 2
       elif r.string == "Alliance":
        _F_ID_ = 1
        
     cursor.execute(sql,[response.getcode(),_F_ID_,index])
     icemelt.commit()

     for row in soup.findAll('tr')[1:x]:
      col = row.findAll('td')
      name = col[0].getText()
      level = col[3].getText()
      _SQL_ = "INSERT INTO `chars` (`gid`, `rid`, `toon_name`, `lvl`, `realm`, `fid`) VALUES (%s, %s, %s, %s, %s, %s)" 
      sql_data = [index,region_id,name,level,realm,_F_ID_]
      #print _SQL_ % sql_data
      cursor.execute(_SQL_,sql_data)
      icemelt.commit()
 #print"./TorrentialSnowfall.sh "+realm+" "+guild.replace(" ", "_")+" "+str(index)+" "+_IN_MYSQL_USR_+" "+_IN_MYSQL_PASS_+" "+_IN_MYSQL_HOST_+" "+_IN_MYSQL_PORT_+" "+_IN_MYSQL_DB_

_GUILD_STATS_ = "SELECT COUNT(DISTINCT `index`) AS 'total',`status` FROM `guilds` GROUP BY `status`;"
_REALM_POPULATION_ = "SELECT COUNT(DISTINCT `cid`) AS 'Total Toons',`realm` FROM `chars` GROUP BY `realm` ORDER BY `Total Toons` DESC;"

# Provide Guild Found Statistics on finishing up additions to the DB

print(" ") #new line to get the stats out of the progress bar
print("Guild statistics:")
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

print("Population by Realm:")
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

# TODO move above code into a function so we can preform multiple status updates
#
# Population by Level: SELECT `lvl`, COUNT(distinct `cid`) AS 'toons', `realm` FROM `chars` GROUP BY `lvl` ORDER BY `toons` DESC;
# Population by Region: SELECT COUNT(`cid`) AS `total`, `rid` FROM `chars` GROUP BY `rid`;
# Population by Race:
# Population by Class:
# Population by Spec:
# Population by Faction: SELECT `fid` AS 'Faction', COUNT(`cid`) AS `total` FROM `chars` GROUP BY `Faction`;


cursor.close()
icemelt.close()
