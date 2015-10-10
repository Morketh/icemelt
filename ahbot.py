#!/usr/bin/python

###########################
#
# AUTHOR: Andrew Malone
# PURPOSE: Scrape AH data compile a MySQL DB and keep updated
# WHY: needed a way to check AH data and look at Price trends
#
###########################

import json
from prettytable import PrettyTable
from pprint import pprint
import urllib2

## local modles ##
from ice import config

## GLOBALS ##
API_URL = "https://us.api.battle.net/wow/"

ITEM_URL = API_URL + "item/"
ITEM_URL_END = "?locale=en_US&apikey=%s" % (config.STORM_API_KEY)

AH_URL = API_URL + "auction/data/"
AH_URL_END = "?locale=en_US&apikey=%s" % (config.STORM_API_KEY)

#config.STORM_API_KEY we need this for our API calls to Blizzard

## functions ##

## MAIN PROG ##


## temp file opener just to reduce data calls to Blizzard ##
#with open('auctions.json') as data_file:    
#    data = json.load(data_file)

## WEB API handle
REALM = "Misha"
ITEM = "18803"

# we should grab some data from Blizzard directly with this API call
files = json.load(urllib2.urlopen(AH_URL+REALM+AH_URL_END))
print "JSON files:\n%s" % (files)
for atr in files["files"]:
	atr["url"]
	atr["lastModified"]

# grab actual AH DATA from the Blizzard Web API using the returned atributes from above call
data = json.load(urllib2.urlopen(atr["url"]))



print "Parsing AH data"
print "Realms found:"
for realm in data["realms"]:
	print realm["name"]

table = PrettyTable()
table.padding_width = 2 # Two spaces between column edges and contents (default is 1)

for entry in data["auctions"]:
	table.add_row([entry["auc"],entry["item"],entry["owner"],entry["buyout"],entry["quantity"]])
	
print table

