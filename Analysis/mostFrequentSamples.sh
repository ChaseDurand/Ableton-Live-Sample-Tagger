#!/bin/bash
#Prints most commonly used samples. Accepts optional argument for number of items to print (default 25).
sqlite3 $1<<EOF
.mode column
.headers on
.width 30 10
SELECT
    samples.sampleName,
    COUNT(projectSampleMapping.sampleID) AS Frequency
FROM
    projectSampleMapping
    INNER JOIN samples ON samples.sampleID = projectSampleMapping.sampleID
GROUP BY projectSampleMapping.sampleID
ORDER BY Frequency DESC
LIMIT "${2:-25}";
EOF