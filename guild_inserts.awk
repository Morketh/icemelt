# Replace the guildname in the output with a MySQL INSERT statement so we can forward the data to MySQL
gsub($0,"INSERT INTO `guilds`(`realm`, `guild`) VALUES (\"REALM_NAME\",\""$GUILD_VALUE"\");")
