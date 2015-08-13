# Replace the guildname in the output with a MySQL INSERT statement so we can forward the data to MySQL
gsub($0,"INSERT INTO `guilds`(`region_id`, `realm`, `guild`) VALUES (\"REGION_ID\",\"REALM_NAME\",\""$GUILD_VALUE"\");")
