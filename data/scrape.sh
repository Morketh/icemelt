#!/bin/bash

# grab the page scrape it
curl http://www.wowprogress.com/export/ranks/ | 

# look for the links
grep "<a href=" |
sed "s/<a href/\\n<a href/g" |
sed 's/\"/\"><\/a>\n/2' |
grep href |

# sor the links
sort |

# display only uniqe links in order
uniq |

# strip off the <a href=" AND "></a>
# we end up links that we can attach to the above URL to pull more data
sed '{s:<a href="::g; s:"></a>::g;}' |

# append the links to the URL and WGET them
xargs -I % wget http://www.wowprogress.com/export/ranks/%

clear

echo "Total downloaded files: "$(ls -1 | wc -l)
