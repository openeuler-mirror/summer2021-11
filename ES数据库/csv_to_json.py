import csv
import json

def csv2json(path,filenames):
    csvfile = open(path, 'r')
    jsonfile = open(path[-4]+'.json', 'w')
    reader = csv.DictReader(csvfile, filenames)
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n')
    return jsonfile