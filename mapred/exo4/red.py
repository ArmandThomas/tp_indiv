import json
import sys

data = json.load(sys.stdin)

print(data)
def calculate_amplitude(records):
    return max(record['magnitude'] for record in records)

def detect_important_events(records, threshold=5.0):
    important_events = [record for record in records if record['magnitude'] >= threshold]
    return important_events
def reducer(city, values):
    important_events = detect_important_events(values)
    amplitude = calculate_amplitude(values)
    return json.dumps({
        'ville': city,
        'amplitude': amplitude,
        'evenements_importants': important_events
    })


for city in data:
    row_data = reducer(city, data[city])
    data[city] = json.loads(row_data)

with open('output.json', 'w') as f:
    json.dump(data, f)