import csv
import time
import requests
import urllib
from geojson import Point, Feature, FeatureCollection, dump


input_file = 'address/member_list.csv'
outfile = "static/json/publisher.geojson"
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


def get_feature_collection(p_data):
    features = []
    for p in p_data:
        lat, lon = p['latitude'], p['longitude']
        feature = Feature(geometry = Point((lon, lat,)),
                    properties = {'title': p['title'], 'description': p['description'], 'marker-color': p['color'],
                                'marker-size': 'medium','stroke': '#ffffff', 'stroke-width': 2})
        features.append(feature)

    return FeatureCollection(features)


point_data = get_point_data(input_file)
# print(point_data)
feature_collection = get_feature_collection(point_data)


with open(outfile, 'w') as f:
    dump(feature_collection, f, indent=2)