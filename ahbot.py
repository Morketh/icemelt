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
import MySQLdb


## local imports ##
from ice import config
from ice import functions as function

## GLOBALS ##
API_URL = "https://us.api.battle.net/wow/"

ITEM_URL = API_URL + "item/"
ITEM_URL_END = "?locale=en_US&apikey=%s" % (config.STORM_API_KEY)

AH_URL = API_URL + "auction/data/"
AH_URL_END = "?locale=en_US&apikey=%s" % (config.STORM_API_KEY)

#config.STORM_API_KEY we need this for our API calls to Blizzard

## functions ##

## MAIN PROG ##

############################################### init section

cursor = function.MySQL_init()

## Temporary Global Variables (will be replaed with SQL provided variables)
REALM = "Misha"
ITEM = "18803"

# Do we have the API key???? if not exit program we need it to do anything with the Auction House
if not config.STORM_API_KEY:
	print "No API Key supplied please set up an API key with Blizzard and then add it to config/key.pcf"
	exit()

# we should grab some data from Blizzard directly with this API call
files = json.load(urllib2.urlopen(AH_URL+REALM+AH_URL_END))
for atr in files["files"]:
	atr["url"]
	atr["lastModified"]

# grab actual AH DATA from the Blizzard Web API using the returned atributes from above call
data = json.load(urllib2.urlopen(atr["url"]))

print "Parsing AH data"
print "Realms found:"
for realm in data["realms"]:
	print realm["name"]

table = PrettyTable(["Auction ID", "Item ID", "Seller", "Seller Realm", "Bid", "Buy Out Price", "Stack Size"])

table.padding_width = 2 # Two spaces between column edges and contents (default is 1)

## Align every thing right and then realign Seller Left
table.align = "r"
table.align["Seller"] = "l"
table.align["Seller Realm"] = "l"

## Sort Table 
table.sortby = "Item ID"

## display a MySQL Console like Table with the AH Data

## SQL INSERT used to add data to the IceMelt DB 
sql = "INSERT INTO `regions` (`name`) SELECT * FROM (SELECT %s) AS tmp WHERE NOT EXISTS (SELECT `name` FROM `regions` WHERE name = %s) LIMIT 1;"

for entry in data["auctions"]:
	row = [
		entry["auc"],
		entry["item"],
		entry["owner"],
		entry["ownerRealm"],
		entry["bid"],
		entry["buyout"],
		entry["quantity"]
		]
#	cursor.execute(sql,)
#	db.commit()
	table.add_row(row)

print table
