#!/bin/bash
#Prints high level summary for project and sample counts.
sampleCount=`sqlite3 $1 "SELECT COUNT(*) FROM samples"`
projectCount=`sqlite3 $1 "SELECT COUNT(*) FROM projects"`
missingCount=`sqlite3 $1 "SELECT COUNT(*) FROM samples WHERE found = 0"`
missingPercent=`echo "scale=1; 100*$missingCount/$sampleCount" | bc`
echo "Database contains $sampleCount samples across $projectCount projects."
echo "$missingCount samples not found ($missingPercent%)."