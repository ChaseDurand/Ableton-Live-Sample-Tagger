import xml.etree.ElementTree as ET
import gzip
import shutil
import os
import glob
from hex import hex_parse

projects = []

print('Finding .als files.')

for file in glob.glob('/Users/chasedurand/Desktop/ZIPPED/**/*.als',
                      recursive=True):  # Find all als files in all subdirectories
    if '/Backup/' not in file:  # Filter to ignore backup als files and add remaining to list
        projects.append(file)

count = 1
total_projects = len(projects)

print(total_projects, '.als files found.\n')

print('Converting .als to .xml.')

for i in projects:
    destination = os.path.split(os.path.split(i)[0])[1] + ' - ' + os.path.splitext((os.path.split(i)[1]))[0]
    destination += '.xml'
    destination = '/Users/chasedurand/Desktop/UNZIPPED/' + destination
    with gzip.open(i, 'r') as f_in, open(destination, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print('(', count, '/', total_projects, ') Converting ', destination, sep='')
    projects[count - 1] = destination
    count += 1

print('.als to .xml conversion complete.\n')
print('Building sample table.')

count = 1

sample_set = set()
sample_dict = dict()

for i in projects:  # iterate over all xml files
    tree = ET.parse(i)
    root = tree.getroot()
    print('(', count, '/', total_projects, ') Finding samples in ', i, sep='')
    count += 1
    sample_path = ""
    #'''
    sample_set.clear()
    for sample_element in root.iter('SampleRef'):  # iterate over all sample references in project
        for data_tag in sample_element.iter('FileRef'):
            hex = data_tag.find('Data').text
            sample_name = data_tag.find('Name').get('Value') #debugging only
            try:
                hex =  ''.join(hex.split())  # Strip newlines and whitespace
                path = hex_parse(hex)
                sample_set.add(path)
            except AttributeError:
                print('could not parse path')
            '''
                for path2 in data_tag.find('SearchHint').find('PathHint'):
                    for path_element in path2.iter('RelativePathElement'):
                        sample_path += '/' + path_element.get('Dir')
                    for filename in sample_element.find('FileRef').iter('Name'):
                        sample_path += '/' + filename.get('Value')
                        sample_set.add(sample_path)
            '''
    for sample in sample_set:
        if sample in sample_dict:
            sample_dict[sample] += 1
        else:
            sample_dict[sample] = 1
    #'''

    '''

    for sample_element in root.iter('SampleRef'):  # iterate over all sample references
        sample_path = ""
        for path in sample_element.find('FileRef').find('SearchHint').find('PathHint'):
            for path_element in path.iter('RelativePathElement'):
                sample_path += '/' + path_element.get('Dir')
        for filename in sample_element.find('FileRef').iter('Name'):
            sample_path += '/' + filename.get('Value')
            sample_set.add(sample_path)

    '''

    '''
    for sample_element in root.iter('SampleRef'):  # iterate over all sample references
        sample_path = ""
        for path in sample_element.find('FileRef').find('RelativePath'):
            for path_element in path.iter('RelativePathElement'):
                sample_path += '/' + path_element.get('Dir')
        for filename in sample_element.find('FileRef').iter('Name'):
            sample_path += '/' + filename.get('Value')
            sample_set.add(sample_path)
    '''

    '''
    for  sample_element in root.iter('SampleRef'):
        sample_path = ""
        for path in sample_element.find('SourceContext'):
            for path_element in path.iter('BrowserContentPath'):
                #print(path_element)
                if "userfolder" in path_element.get('Value'):
                    sample_path = path_element.get('Value')
                    #need to parse/clean sample path here
                    sample_set.add(sample_path)
                    #print(sample_path)
    '''
count = 1
total_samples = len(sample_dict)

print(total_samples, 'unique samples found.')

#sample_set = sorted(sample_set)

#sample_dict.items()

output = [(a, b) for b, a in sample_dict.items()]
output = sorted(output, key=lambda x:x[0], reverse=True)

for i in output:
    print(i)
    count += 1

'''
for i in output:
    print('(',count,'/',total_samples,') ',i, sep='')
    count += 1
'''