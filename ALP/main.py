import xml.etree.ElementTree as ET
import gzip
import shutil
import os
import glob
from hex import hex_parse
from xmp_tagger import xmp_tag
import getpass
from natsort import natsorted

project_path = '/Users/chasedurand/Desktop/ZIPPED'
xml_path = '/Users/chasedurand/Desktop/UNZIPPED'

#Enables incremental print outputs for different stages
verbose = True

projects = [] #List of paths of ALS project files

print('Finding .als files.')
for file in glob.glob(project_path + '/**/*.als',
                      recursive=True):  # Find all als files in all subdirectories
    if '/Backup/' not in file:  # Filter to ignore backup als files and add remaining to list
        projects.append(file)
count = 1
total_projects = len(projects)
print(total_projects, '.als files found.\n')

#Coverts (unzips) all ALS files to XML
print('Converting .als to .xml.')
for i in projects:
    destination = '/' + os.path.split(os.path.split(i)[0])[1] + ' - ' + os.path.splitext((os.path.split(i)[1]))[0] #Preserves project and set name
    destination += '.xml'
    destination = xml_path + destination
    with gzip.open(i, 'r') as f_in, open(destination, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    if verbose:
        print('(', count, '/', total_projects, ') Converting ', destination, sep='')
    projects[count - 1] = destination
    count += 1
print('.als to .xml conversion complete.\n')

print('Building sample table.')

count = 1

#Use set to find unique samples in project to count sample only once per project (ex. same file in sampler and audio track)
#Use dictionary to count number of projects each unique sample appears in (max occurances equal to number of projects)
#Missing set/dict for files that can no longer be found
sample_set = set()
sample_missing_set = set()
sample_dict = dict()
sample_missing_dict = dict()

for xml in projects:  # iterate over all xml files
    tree = ET.parse(xml)
    root = tree.getroot()
    if verbose:
        print('(', count, '/', total_projects, ') Finding samples in ', xml, sep='')
        count += 1
    sample_path = ""
    #'''
    sample_set.clear()
    for sample_element in root.iter('SampleRef'):  # iterate over all sample references in project
        for data_tag in sample_element.iter('FileRef'):
            hex = data_tag.find('Data').text
            sample_name = data_tag.find('Name').get('Value') #debugging when finding names of samples that messed up
            try:
                hex =  ''.join(hex.split())  # Strip newlines and whitespace
                path = hex_parse(hex)
                if os.path.isfile(path):
                    sample_set.add(path)
                else:
                    sample_missing_set.add(path)
            except AttributeError:
                print('could not parse path')

    for sample in sample_set:
        if sample in sample_dict:
            sample_dict[sample] += 1
        else:
            sample_dict[sample] = 1

    for sample in sample_missing_set:
        if sample in sample_missing_dict:
            sample_missing_dict[sample] += 1
        else:
            sample_missing_dict[sample] = 1

#Print all unique samples
count = 1
total_samples = len(sample_dict)
print(total_samples, 'unique samples found.')
output = [(a, b) for b, a in sample_dict.items()]   #Reverse dictionary of unique samples
output = sorted(output, key=lambda x:x[0], reverse=True)    #Sort unique samples by most occurances
if verbose:
    for i in output:
        print(i)
count = 1



#print missing samples
'''
total_samples = len(sample_missing_dict)
print(total_samples, 'missing samples found.')
output = [(a, b) for b, a in sample_missing_dict.items()]
output = sorted(output, key=lambda x:x[0], reverse=True)

for i in output:
    print(i)
    count += 1
'''

#For all found existing samples, need to filter

user = getpass.getuser()
lib_path = '/Users/'+user+'/Library/Preferences/Ableton'
live_pref = os.listdir(lib_path)
live_pref = natsorted(live_pref)
live_pref = live_pref[len(live_pref)-1]
lib_path = lib_path + '/' + live_pref + '/Library.cfg'
f = open(lib_path)

user_folders = []

for line in f:
    if 'UserFolderInfo Id' in line:
        user_folders.append(line.split('Path=\"')[1].split('\"')[0])
f.close()

samples = sample_dict.keys()

sample_valid = []

for i in samples:
    if any(x in i for x in user_folders):
        sample_valid.append(i)
print(len(sample_valid),'out of',total_samples,' samples in user library will be indexed.')

for i in sample_valid:
    xmp_tag(i)