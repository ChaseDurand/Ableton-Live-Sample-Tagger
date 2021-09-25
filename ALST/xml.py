from pathlib import Path
import xml.etree.ElementTree as ET
'''
Functions for parsing XML files.
'''


def getRelativePath(fileRef, alsFile):
    #Given an XML FileRef tag and SQLite projectRow, return the sample's relative path
    fullPath = alsFile.parent.absolute(
    )  #Get relative path root (project file location)
    #Iterate through relative path directories then append to path
    for relativePathElement in fileRef.find('RelativePath').iter(
            'RelativePathElement'):
        fullPath = Path.joinpath(fullPath, relativePathElement.get('Dir'))
    fullPath = Path.joinpath(fullPath, fileRef.find('Name').get('Value'))
    return fullPath


def getAbsolutePath(fileRef):
    #Given an XML FileRef tag, return the sample's absolute path
    if fileRef.find('Data').text == None:
        print("     ***ERROR no data tag for",
              fileRef.find('Name').get('Value'))
        return None
    hexData = ''.join(fileRef.find(
        'Data').text.split())  #Get hex Data blob, stripping newlines
    return hex2path(hexData)


def hex2path(data):
    #Takes given hex data chunk from ALS xml file and returns filepath Path object
    #Data is roughly structured sizeOfData/data/null pattern
    dataArray = bytearray.fromhex(data)
    if not checkDataBlobSize(
            dataArray):  #Confirm header reflects datablob size
        print("*** ERROR: Data length does not match header length ***")
        print(dataArray)
        exit(1)
    foundVolume = ""
    foundPath = ""
    i = len(dataArray) - 1

    #Scan from end looking for volume and filepath indicators
    #Filepath appears after first 0x12
    #Volume appears after 0x13

    #TODO add error checking for utf-8 decode
    foundVolume = decodeDataChunk(dataArray, i, 0x13)
    foundPath = decodeDataChunk(dataArray, i, 0x12)
    if foundVolume == "" or foundPath == "":
        print("***ERROR: volume and path not found***")
        exit()
    return Path.joinpath(
        Path(foundVolume),
        str(Path(foundPath)).replace(Path(foundPath).root, "", 1))


def decodeDataChunk(dataArray, i, stopByte):
    while (i > 5):
        if (dataArray[i] == stopByte):
            dataChunkSize = dataArray[i + 1] * (16**2) + dataArray[i + 2]
            if (checkDataChunk(dataArray, i + 3, dataChunkSize)):
                return dataArray[i + 3:i + 3 + dataChunkSize].decode("utf-8")
        i -= 1
    print("***ERROR: Unable to decode data chunk***")
    exit()


def checkDataBlobSize(dataArray):
    #Confirms that the header reflects datablob size
    #First 6 bytes are the number of bytes of the data
    i = 0
    headerSize = 0
    while i < 6:
        #Convert byte based on digit significance
        headerSize += dataArray[i] * (16**(10 - 2 * i))
        i += 1
    if headerSize != len(dataArray):
        return False
    return True


def checkDataChunk(dataArray, startIndex, chunkSize):
    #Checks if we have found a valid data chunk from datablob
    #Chunks are valid if the length includes no 0x00/0xFF and terminates with 0x00/0xFF
    if (startIndex + chunkSize) >= len(dataArray):
        return False
    if (dataArray[startIndex + chunkSize] !=
            0x00) and (dataArray[startIndex + chunkSize] != 0xFF):
        return False
    if 0x00 in dataArray[startIndex:startIndex + chunkSize]:
        return False
    if 0xFF in dataArray[startIndex:startIndex + chunkSize]:
        return False
    return True