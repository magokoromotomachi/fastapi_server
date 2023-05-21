import csv
import time
import requests
import urllib
from geojson import Point, Feature, FeatureCollection, dump


input_file = 'address/member_list.csv'
outfile = "out.geojson"
makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="

def get_point_data(file_name):
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        csv_reader = csv.reader(f)
        point_data = []

        for i, line in enumerate(csv_reader):
            if i >= 10:
                # print(point_data)
                break
            # print(line)
            s_quote = urllib.parse.quote(line[4])
            response = requests.get(makeUrl + s_quote)
            lng_lat = response.json()[0]["geometry"]["coordinates"]
            point_data.append({
                'title': line[0],
                'description': line[4],
                'latitude': lng_lat[1],
                'longitude': lng_lat[0],
                'color': '#ff0000'
            })
            time.sleep(1)

    return point_data

point_data = get_point_data(input_file)
print(point_data)

# Prepare Geojson FeatureCollection
ft_all = []
for i, p in enumerate(point_data):
    lat, lon = p['latitude'], p['longitude']
    ft = Feature(geometry = Point((lon, lat,)),
                 properties = {'title': p['title'], 'description': p['description'], 'marker-color': p['color'],
                               'marker-size': 'medium','stroke': '#ffffff', 'stroke-width': 2})
    ft_all.append(ft)
ft_colct = FeatureCollection(ft_all)

with open(outfile, 'w') as f:
    dump(ft_colct, f, indent=2)