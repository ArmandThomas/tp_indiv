import sys
import json

data = {}
def calculate_amplitude(records):
    return max(record['magnitude'] for record in records)

def detect_important_events(records, threshold=5.0):
    important_events = [record for record in records if record['magnitude'] >= threshold]
    return important_events

def reducer_by_city(row):
    if row['secousse']:
        if row['ville'] not in data:
            data[row['ville']] = []
        data[row['ville']].append(row)
def reducer_evenements_importants(city, values):
    important_events = detect_important_events(values)
    amplitude = calculate_amplitude(values)
    return json.dumps({
        'ville': city,
        'amplitude': amplitude,
        'evenements_importants': important_events
    })

def correlations_between_evenements(city, values):
    for record in values['evenements_importants']:
        for record2 in values['evenements_importants']:
            if record != record2:
                if record['magnitude'] == record2['magnitude']:
                    return json.dumps({
                        'ville': city,
                        'evenement1': record,
                        'evenement2': record2,
                        'correlation': 'Les deux événements ont la même magnitude'
                    })
                else:
                    return json.dumps({
                        'ville': city,
                        'evenement1': record,
                        'evenement2': record2,
                        'correlation': 'Les deux événements n\'ont pas la même magnitude',
                        'difference': record['magnitude'] - record2['magnitude']
                    })

for line in sys.stdin:
    reducer_by_city(json.loads(line))

for city in data:
    row_data = reducer_evenements_importants(city, data[city])
    data[city] = json.loads(row_data)
    corr_data = correlations_between_evenements(city, data[city])
