import sys
import json

data = {}

def reducer(row):
    if row['secousse']:
        if row['ville'] not in data:
            data[row['ville']] = []
        data[row['ville']].append(row)


for line in sys.stdin:
    line_data = reducer(json.loads(line))

with open('output.json', 'w') as f:
    json.dump(data, f)