#!/usr/bin/python

## hopefully we can avoide disaster if we dont import this in a main program
try:
  config
except NameError:
  import config


## Local Imports for these functions ##
import MySQLdb


## MySQL init function added an error handler + a config data setting dump should be able to use this for all IceMelt database connections
def MySQL_init():
    """Set up the Connection using config/ice.conf
    returns a standard DB Cursor Object"""
    try:
        db = MySQLdb.connect(config._IN_MYSQL_HOST_,config._IN_MYSQL_USR_,config._IN_MYSQL_PASS_,config._IN_MYSQL_DB_)
        cur = db.cursor()
        return cur
    except MySQLdb.Error:
        print "There was a problem in connecting to the database."
        print "Please ensure that the database exists on the target system, and that you have configured the settings properly in config/ice.conf"
        print "Config DUMP:"
        print "HOST: %s\nUSER: %s\nPASS: %s\nDATABASE: %s" %(config._IN_MYSQL_HOST_,config._IN_MYSQL_USR_,config._IN_MYSQL_PASS_,config._IN_MYSQL_DB_)
        exit(4) #unclean exit with out Traceback
    except MySQLdb.Warning:
        pass
