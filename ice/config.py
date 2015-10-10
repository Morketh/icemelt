#!/usr/bin/python
##################################################################################################
#
# Copyright (C) 2015 Andrew Malone 
# 
# AUTHOR: Andrew Malone 
#  
# TITLE: config
#
# PURPOSE: configuration related data for icemelt
#
#
##################################################################################################

import ConfigParser
import os

ice = ConfigParser.ConfigParser()
ice.read(os.path.abspath("config/ice.conf"))
ice.sections()

## Config Parse Helper ##

def ConfigSectionMap(section):
    dict1 = {}
    options = ice.options(section)
    for option in options:
        try:
            dict1[option] = ice.get(section, option)
            if dict1[option] == -1:
                print("Skipping: %s %s" % (section,option))
        except:
            print("exception on %s %s!" % (section,option))
            dict1[option] = None
    return dict1



# Set up config values
_IN_MYSQL_HOST_ = ConfigSectionMap("IceMeltDB")['host']
_IN_MYSQL_USR_ = ConfigSectionMap("IceMeltDB")['user']
_IN_MYSQL_PASS_ = ConfigSectionMap("IceMeltDB")['password']
_IN_MYSQL_DB_ = ConfigSectionMap("IceMeltDB")['database']

# Logs enabled? if so set path otherwise we dont care.
_IN_SQL_LOGS_ = ConfigSectionMap("SqlLogs")['enabled']
if _IN_SQL_LOGS_:
 _IN_SQL_FILE_ = ConfigSectionMap("SqlLogs")['path']

# API Key section
API_KEY_ENABLED = ConfigSectionMap("AHBot")['enabled']
if API_KEY_ENABLED:
	API_KEY_FILE = ConfigSectionMap("AHBot")['keyfile']
	STORM_API_KEY = [line.rstrip('\n') for line in open(API_KEY_FILE)][0]
