import xml.etree.ElementTree as ET
import gzip
import shutil
import os
import glob
import collections

projects = []

print('Finding .als files.')

for file in glob.glob('/Users/chasedurand/Desktop/ZIPPED2/**/*.als', recursive=True): #Find all als files in all subdirectories
    if '/Backup/' not in file: #Filter to ignore backup als files and add remaining to list
        projects.append(file)

count_projects = 1
total_projects = len(projects)

print(total_projects, '.als files found.')

print('Converting .als to .xml.')

for i in projects:
    destination = os.path.split(os.path.split(i)[0])[1] + ' - ' + os.path.splitext((os.path.split(i)[1]))[0]
    destination+='.xml'
    destination = '/Users/chasedurand/Desktop/UNZIPPED2/' + destination
    with gzip.open(i, 'r') as f_in, open(destination, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print('(', count_projects, '/', total_projects, ') ', destination, sep='')
    projects[count_projects-1] = destination
    count_projects += 1

print('.als to .xml conversion complete.')
print('Building sample table.')


for i in projects:
    tree = ET.parse(i) #get XML file
    root = tree.getroot()
    print(i)
    sample_path = ""
    sample_set = set()

    for sample_element in root.iter('SampleRef'): #iterate over all sample references
            sample_path = ""
            for path in sample_element.find('FileRef').find('SearchHint').find('PathHint'):
                    for path_element in path.iter('RelativePathElement'):
                            sample_path += '/' + path_element.get('Dir')
            for filename in sample_element.find('FileRef').iter('Name'):
                    sample_path += '/' + filename.get('Value')
                    sample_set.add(sample_path)
    print("\n".join(sorted(sample_set)))
