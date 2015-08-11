# Replace the guildname in the output with a MySQL INSERT statement so we can forward the data to MySQL
# GID is going to be a foriegn key matching toon with Guilds
# $0 should be a comma seperated list of GID, Toon_Name, Realm_Name
# running this script will add in the CURRENT_TIMESTAMP into the table
# A lookup for the GID should be preformed inorder to build said list
# an INDEX will automaticly be generated when inserting the toon into the DataBase
gsub($0,"INSERT INTO `chars` (`gid`, `toon_name`, `realm`, `updaded`) VALUES ("$0", CURRENT_TIMESTAMP);")
