import pandas as pd
import csv, json

raw_data = pd.read_csv('../Data_Crawel/Community_Issue_Data/Raw_data/Openeuler-所有社区的信息.csv',
                       usecols=['full_name', 'name', 'forks_count', 'stargazers_count', 'watchers_count',
                                'open_issues_count']
                       )
raw_data.to_csv('../Data_Crawel/Community_Issue_Data/Raw_data/temp.csv', index=None)


def csv2json(path, filenames):
    csvfile = open(path, 'r')
    print(type(csvfile))
    # csvfile = raw_data
    jsonfile = open(path[0:-4] + '.json', 'w')
    reader = csv.DictReader(csvfile, filenames)
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n')
    print('over')
    return path[0:-4] + '.json'


path = '../Data_Crawel/Community_Issue_Data/Raw_data/temp.csv'
filenames = ('full_name', 'name', 'forks_count', 'stargazers_count', 'watchers_count',
             'open_issues_count')
path = csv2json(path, filenames)
print(path)
