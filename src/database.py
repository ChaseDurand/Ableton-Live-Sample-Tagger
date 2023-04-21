import sqlite3
from sqlite3 import Error
from pathlib import Path
'''
Functions for handling database operations.
'''


def initializeDatabase(projectPathRoot):
    # If database doesn't exist in given directory, create database with needed tables.
    # Regardless, return connection to database.
    dbPath = projectPathRoot.joinpath(str(projectPathRoot) + '/ALST.db')
    conn = None
    try:
        conn = sqlite3.connect(dbPath)
    except Error as e:
        print(e)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Check if database with tables already exists
    try:
        cursor.execute("""
            CREATE TABLE projects (
                projectID INTEGER PRIMARY KEY,
                projectName TEXT,
                setName TEXT,
                projectPath TEXT UNIQUE,
                setPath TEXT,
                setModDate INTEGER,
                lastModified
            )
        """)
    except Error as e:
        # print(e)
        print("Database already exists.")
        return conn
    cursor.execute("""
        CREATE TABLE samples (
            sampleID INTEGER PRIMARY KEY,
            sampleName TEXT,
            path TEXT,
            found INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE projectSampleMapping (
            mappingID INTEGER PRIMARY KEY,
            projectID INTEGER,
            sampleID INTEGER
        )
    """)
    cursor.close()
    conn.commit()
    return conn


def alsInDB(alsFile, cur):
    #Check if a given project+set appear in the DB
    result = cur.execute(
        'SELECT * FROM projects WHERE projectName= ? AND setName=?;',
        (str(alsFile.parent.name), str(alsFile.name)))
    resultCount = len(result.fetchall())
    if resultCount == 0:
        #Project is not in DB
        return False
    if resultCount == 1:
        #Project is in DB
        return True
    print("***ERROR: Multiple instances of project in DB***")
    exit(1)


def alsUpToDate(alsFile, cur):
    #Check if a given project+set are up to date in the DB
    result = cur.execute(
        'SELECT * FROM projects WHERE projectName= ? AND setName=?;',
        (str(alsFile.parent.name), str(alsFile.name)))
    if (alsFile.stat().st_mtime != result.fetchone()['setModDate']):
        return False
    return True


def addALStoDB(alsFile, cur):
    cur.execute('''
        INSERT OR REPLACE INTO projects (projectPath, setName, setModDate)
        VALUES (?, ?, ?);
        ''', (str(alsFile), alsFile.name, alsFile.stat().st_mtime))
    
    if (alsInDB(alsFile, cur)):
        # Update mod date
        cur.execute(
            "UPDATE projects SET setModDate=? WHERE projectName=? AND setName=?;",
            (alsFile.stat().st_mtime, str(
                alsFile.parent.name), str(alsFile.name)))
        print("Updated", alsFile.name, "in DB.")
    else:
        # New ALS, add to DB
        cur.execute(
            "INSERT INTO projects (projectName, setName, projectPath, setModDate) VALUES (?,?,?,?)",
            (str(alsFile.parent.name), str(
                alsFile.name), str(alsFile), alsFile.stat().st_mtime))
        print("Added", alsFile.name, "to DB.")
    
    result = cur.execute('SELECT * FROM projects WHERE projectPath = ?;',
                         (str(alsFile), ))
    return result.fetchone()['projectID']




def addSampletoDB(samplePath, cur):
    #Add sample to DB if not already in
    result = cur.execute('SELECT * FROM samples WHERE path= ?;',
                         (str(samplePath), ))
    if (len(result.fetchall()) == 0):
        #Sample is new
        sampleName = samplePath.name
        cur.execute(
            "INSERT INTO samples (sampleName, path, found) VALUES (?,?,?)",
            (sampleName, str(samplePath), samplePath.exists()))
    #Get sample ID
    result = cur.execute('SELECT * FROM samples WHERE path = ?;',
                         (str(samplePath), ))
    return result.fetchone()['sampleID']


def addProjectSampleMapping(projectID, sampleID, cur):
    #Add project-sample mapping to DB if not already in
    result = cur.execute(
        'SELECT * FROM projectSampleMapping WHERE projectID = ? AND sampleID = ?;',
        (projectID, sampleID))
    if (len(result.fetchall()) == 0):
        cur.execute(
            "INSERT INTO projectSampleMapping (projectID, sampleID) VALUES (?,?)",
            (projectID, sampleID))
    return