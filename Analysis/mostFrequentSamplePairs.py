import sqlite3
from sqlite3 import Error
from pathlib import Path
from itertools import combinations
import operator

print("***WARNING: This operation may take time for large databases***")
while True:
    dbPath = Path(input("Enter Ableton Live Projects directory: "))
    if dbPath.exists():
        break
    else:
        print(dbPath, " is not a valid path!")

try:
    conn = sqlite3.connect(str(dbPath))
except Error as e:
    print(e)
    exit()

cursor = conn.cursor()

projectSelection = cursor.execute(
    """SELECT DISTINCT projectID FROM projectSampleMapping""")
pairsCount = {}
for als in projectSelection.fetchall():
    setName = cursor.execute(
        """SELECT setName FROM projects WHERE projects.projectID =?;""",
        (als[0], ))
    print("Getting samples from:", setName.fetchone()[0])

    samples = []
    sampleSelection = cursor.execute(
        """SELECT sampleID FROM projectSampleMapping WHERE projectID=?;""",
        (als[0], ))
    for items in sampleSelection.fetchall():
        samples.append(items[0])
    samples.sort()
    combos = combinations(samples, 2)
    for pair in combos:
        if pair in pairsCount:
            pairsCount[pair] += 1
        else:
            pairsCount[pair] = 1

sortedPairsCount = sorted(pairsCount.items(),
                          key=operator.itemgetter(1),
                          reverse=True)

i = 0
pairsToShow = 10
output = [[0] * 3 for j in range(pairsToShow)]
while i < pairsToShow and i < len(sortedPairsCount):

    sampleIDa = sortedPairsCount[i:i + 1][0][0][0]
    sampleIDb = sortedPairsCount[i:i + 1][0][0][1]
    output[i][2] = sortedPairsCount[i:i + 1][0][1]
    output[i][0] = cursor.execute(
        """SELECT sampleName FROM samples WHERE sampleID=?;""",
        (sampleIDa, )).fetchone()[0]
    output[i][1] = cursor.execute(
        """SELECT sampleName FROM samples WHERE sampleID=?;""",
        (sampleIDb, )).fetchone()[0]
    i += 1
for row in output:
    print("{: >40} {: >40} {: >40}".format(*row))
conn.close
exit()
