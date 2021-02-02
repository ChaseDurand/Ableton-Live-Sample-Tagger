#Takes given hex data chunk from ALS xml file and returns filepath string
def hex_parse(data):
    path = bytearray.fromhex(data)
    found_path = ''

    #Finds : which looks to be uniquely found in the sample path
    #I should probably figure out what the rest of the hex is and how it's structured
    #This implementation ignores volumes, which appears to be stored early in the hex, so I'm unsure how it handles samples from another volume, such as a USB drive
    i = 0
    while i < len(path):
        if (path[i] != 0x00) and (path[i] != 0xFF):
            first_index = i
            length = path[i]
            offset = 1
            found_string = ''
            while (offset <= length) and (path[first_index+offset] != 0x00) and (path[first_index+offset] != 0xFF):
                if(first_index+offset) == len(path):
                    print('woah now')
                found_string += chr(path[first_index+offset])
                #print(chr(path[first_index + offset]), end='')
                offset += 1
            if offset == length+1:
                #possible valid string
                if found_string != '/':
                    found_path = found_string
            i = first_index+offset
            #i = i+length
        #print(path[i])
        i += 1
    found_path = '/' + found_path
    return(found_path)