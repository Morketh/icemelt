#!/usr/bin/python
##################################################################################################
#
# Copyright (C) 2015 Andrew Malone  
# 
# TITLE: IceMelt 
# 
##################################################################################################

# our variables we need later
_LOC_SQL_UPDATES_ = "./data/"

##################################################################################################
# _IN_MYSQL_USR_
# _IN_MYSQL_PASS_
# _IN_MYSQL_HOST_
# _IN_MYSQL_PORT_
# _IN_MYSQL_DB_
# _IN_SQL_FILE_
#
#
# import all of our needed functions
##################################################################################################
from subprocess import call 
import os 
import subprocess
import sys
import getpass
from time import sleep
import glob
import progressbar
import MySQLdb

## local Imports ##
from ice import config
from ice import functions as function
##################################################################################################
#
# New functions
# TODO: move these to a set of submodules
#
##################################################################################################

# lets clear our screen and give the user some information 
subprocess.call('clear') 
print "Welcome: " + getpass.getuser() 
print "Icemelt copyright (C) 2015 Andrew Malone" 
print "this install script will resume in 5 seconds"
sleep(5)

# this will delete the file and then touch it so we can write to it later
if config._IN_SQL_LOGS_:
 os.system('rm -f '+config._IN_SQL_FILE_)
 os.system('touch '+config._IN_SQL_FILE_)

#returns a LIST of values
realms = glob.glob(_LOC_SQL_UPDATES_ + '*.json')
realms = sorted(realms)

print "Inililizing.......Icemelt"
sleep(2)
print "Preparing Winter Gear......"
sleep(4)
print "Activating Thermo Sensors....... [ OK ]"

# data orginization function pulls a list of file names and orginizes them we should be able to extract a realm name from the file names for icemelt

# data we need to pass to ginsert
# $1 = File Name
# $2 = Realm Name
# $3 = Temp SQL file
# $4 = MySQL User
# $5 = MySQL password
# $6 = MySQL database
# $7 = MySQL HOST
# $8 = MySQL PORT
# fname will be in the format us_cenarius_tier12_10.json

sleep(5)

#debug dump of Glob
#var_dump(realms, '')

# set up mysql connection
db = function.MySQL_init()
cursor = db.cursor()

index = 0
bar = progressbar.ProgressBar(maxval=len(realms), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()]).start()
SQL = "REPLACE INTO `guilds` (`index`, `guild`, `region_id`, `realm`) VALUES (%s, %s, %s, %s);"
for fname in realms:
  fpointer = open(fname)
  s = fpointer.read()
  csv = s.split(",")
  gname = csv[4].split(":")[1].replace("\"","")
  realm = csv[5].split(":")[2].replace("\\","").split("/")[5]
  # clears out chat spam and makes the output show only at the top of the screen
  bar.update(index)
  index = index + 1
  rname = fname.split("_")[1].replace('.json', '')
  region = fname.split("_")[0].replace('.json', '') #gives us the region ID Name we need this to format URLS
  region = region.split("/")[-1]

  # we first need to add the Region ID to to the regions table and take the new index and add it to the guilds table
  # INSERT INTO `regions` (`name`) SELECT * FROM (SELECT %s) AS tmp WHERE NOT EXISTS (SELECT `name` FROM `regions` WHERE name = %s) LIMIT 1;
  # Insert name if it doesnt exist other wise do nothing (let MySQL silently ignore the error instead of dealing with it here)
  sql = "INSERT INTO `regions` (`name`) SELECT * FROM (SELECT %s) AS tmp WHERE NOT EXISTS (SELECT `name` FROM `regions` WHERE name = %s) LIMIT 1;"
  cursor.execute(sql,[region,region])
  db.commit()
  cursor.execute("SELECT `id` FROM `icemelt`.`regions` WHERE `name`=%s;",region)
  rid = cursor.fetchone()  
  sqldata = [index,gname,rid[0],realm]

  # INSERT data into the Guilds Table 
  cursor.execute(SQL,sqldata)
  db.commit()
bar.finish()
cursor.close()
db.close()
