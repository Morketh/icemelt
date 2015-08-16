#!/usr/bin/python
##################################################################################################
#
# Copyright (C) 2013 Collective Industries code provided by Andrew Malone  
# 
# TITLE: IceMelt 
# 
# TODO: rebuild this ENTIRE thing with python code >..< Region IDs are numaric now for the rest
# of the project at this point the main data engine is pretty much broken
#
##################################################################################################

# our variables we need later
_LOC_SQL_UPDATES_ = "./data/"
_FILE_TEMP_RAW_ = "./sql_inserts.tmp"

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

##################################################################################################
#
# New functions
# TODO: move these to a set of submodules
#
##################################################################################################

def var_dump(var, prefix=''):
    """
    You know you're a php developer when the first thing you ask for
    when learning a new language is 'Where's var_dump?????'
    """
    my_type = '[' + var.__class__.__name__ + '(' + str(len(var)) + ')]:'
    print(prefix, my_type)
    prefix += '    '
    for i in var:
        if type(i) in (list, tuple, dict, set):
            var_dump(i, prefix)
        else:
            if isinstance(var, dict):
                print(prefix, i, ': (', var[i].__class__.__name__, ') ', var[i])
            else:
                print(prefix, '(', i.__class__.__name__, ') ', i)


# lets clear our screen and give the user some information 
subprocess.call('clear') 
print "Welcome: " + getpass.getuser() 
print "Icemelt copyright (C) 2015 Andrew Malone" 
print "this install script will resume in 5 seconds"
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

_IN_SQL_FILE_ = raw_input('File for SQL statments [/tmp/icemelt.sql]: ')
if _IN_SQL_FILE_ == '':
        _IN_SQL_FILE_ = '/tmp/icemelt.sql' #defualt SQL location

# this will delete the file and then touch it so we can write to it later
os.system('rm -f '+_IN_SQL_FILE_)
os.system('touch '+_IN_SQL_FILE_)

_IN_MYSQL_DB_ = raw_input('MySQL database to use [icemelt]: ')
if _IN_MYSQL_DB_ == '':
        _IN_MYSQL_DB_ = 'icemelt' #defualt mysql database

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
db = MySQLdb.connect(_IN_MYSQL_HOST_,_IN_MYSQL_USR_,_IN_MYSQL_PASS_,_IN_MYSQL_DB_)
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
  id = cursor.fetchone()  
  sqldata = [index,gname,id[0],realm]
  cursor.execute(SQL,sqldata)
  db.commit()
  # we now need to call the ginsert script with the user provided variables
  #os.system("./ginsert "+fname+" "+rname+" "+_IN_SQL_FILE_+" "+_IN_MYSQL_USR_+" "+_IN_MYSQL_PASS_+" "+_IN_MYSQL_DB_+" "+_IN_MYSQL_HOST_+" "+_IN_MYSQL_PORT_+" "+region)
bar.finish()
cursor.close()
db.close()
