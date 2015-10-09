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

## GLOBALS ##

## functions ##

## MAIN PROG ##


## temp file opener just to reduce data calls to Blizzard ##
with open('auctions.json') as data_file:    
    data = json.load(data_file)

print "Parsing AH data"
print "Realms found:"
for realm in data["realms"]:
	print realm["name"]

table = PrettyTable()
table.padding_width = 1 # One space between column edges and contents (default)

for entry in data["auctions"]:
	table.add_row([entry["auc"],entry["item"],entry["owner"],entry["buyout"],entry["quantity"]])
	
print table
