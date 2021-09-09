import sqlite3
from sqlite3 import Error
from pathlib import Path
from itertools import combinations
import operator
import sys
'''
Get most common pairs of samples from database.
'''

print("***WARNING: This operation may take time for large databases***")

#If database wasn't given as argument, then prompt user for db path.
if len(sys.argv) == 1:
    while True:
        dbPath = Path(input("Enter Ableton Live Projects directory: "))
        if dbPath.exists():
            break
        else:
            print(dbPath, " is not a valid path!")
else:
    dbPath = sys.argv[1]

#If optional int items to show was given as argumnt, then set items to display or default.
if len(sys.argv) == 3:
    pairsToShow = int(sys.argv[2])
else:
    pairsToShow = 25

try:
    conn = sqlite3.connect(str(dbPath))
except Error as e:
    print(e)
    exit()
cursor = conn.cursor()

projectSelection = cursor.execute(
    """SELECT DISTINCT projectID FROM projectSampleMapping""")
pairsCount = {}
#For each als, get all samples and record combinations
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
    samples.sort(
    )  #Sort to ensure pairs are counted in same order (i.e. won't record 1-2 and 2-1 separately)
    combos = combinations(samples, 2)
    for pair in combos:
        if pair in pairsCount:
            pairsCount[pair] += 1
        else:
            pairsCount[pair] = 1
#Sort counts of all combinations
sortedPairsCount = sorted(pairsCount.items(),
                          key=operator.itemgetter(1),
                          reverse=True)

i = 0
output = [[0] * 3 for j in range(pairsToShow)]
#For most common samples, convert sampleID to sampleName for display
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
header = ["Sample 1", "Sample 2", "Frequency"]
output.insert(0, header)
print()
for row in output:
    print("{: <40} {: <40} {: <40}".format(*row))
if i == len(sortedPairsCount):
    print("No samples remaining.")
conn.close
exit()