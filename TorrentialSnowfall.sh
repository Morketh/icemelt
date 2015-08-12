#!/bin/bash
#
# Name: TorrentialSnowfall
# Purpose: Pulls toon list directly from Blizzard using Guild Names in the IceMelt DB
# Copyright (C) Andrew Malone 2015
#

# so far preliminary research indicates that a simple look up of the guild name should yeild a guild roster
#
# wget --quiet -O- http://us.battle.net/wow/en/guild/REALM_NAME/GUILD_NAME/roster |
# grep "wow/en/character" |
# sed '{s:<td class="name"><strong><a href="::g; s:</a></strong></td>::g; s:" class=":,:g;s:">:,:g}'
#
# This should produce output in a CSV format: /wow/en/character/misha/Rageena/,color-c9,Rageena
# Feild $2 is just an HTML color used on the webpage and can be safly forgotten
# Field $1 is the URL which gets appended directly to us.battle.net
# Field $3 is the Toon name
# Database entry will only Contain Realm,Toon in order to compress data since the URL can be reproduced in a simple algorithym


# Since the URL is dynamic based on DB entries we need to pull from the DB generate a URL and push results back into MySQL
# structure of Program:
# ->Python app to pull from DB and generate a URL (Also grabs MySQL credentials in order to set up the login process)
# -->Bash program to retrive HTML page and filter data and insert into DB

wget --quiet -O- http://us.battle.net/wow/en/guild/$1/$2/roster |
grep "wow/en/character" |
sed '{s:<td class="name"><strong><a href="::g; s:</a></strong></td>::g; s:" class=":,:g;s:">:,:g}' |
awk -F "," '{print $1}' |
awk -F "/" '{print $5, $6}'

# Above will output Realm Char pair like: misha Feleana
