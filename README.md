##INSTALL

you will need to have the module progress bar installed to use this

```bash
easy_install progressbar
# or
pip install progressbar
```

Pretty simple little program. IceMelt.py is Stage 1 data scraper building a database based off the wowprogress export data
Depending on CPU Core speed this might take some time however running on a Dell Poweredge 2850 yeilds a complete guild table in roughly 25 minutes
Stage 2 is the Cold-air-funnel.py This will pull guilds/region_ids/realms from the guild table look up each roster on blizzard formatting the URL: "http://us.battle.net/wow/REGION/guild/REALM/GUILD/roster"
This will give us a Guild Roster with toon names in it Cold-air-funnel.py will parse that roster and "Funnel" the data into the Chars table at last check run time is looking to be roughly 11 Days.
Stage 3 has not been implimented as of yet how ever future design plans include a full cross refrance system for every field of data
