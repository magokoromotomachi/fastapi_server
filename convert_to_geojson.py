import csv
import time
import requests
import urllib
from geojson import Point, Feature, FeatureCollection, dump

makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
# input_file_name = "R2-kuritu-syou"
input_file_name = "H27-kuritu_tyuugattukou"


def get_point_data(file_name):
    with open(file_name, "r", encoding="shift-jis") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        point_data = []

        for line in csv_reader:
            name = f'{line[0]}小学校'
            name = f'{line[0]}中学校'
            address = f'東京都世田谷区{line[1]}'
            tel = line[2]
            fax = line[3]
            description = f'{name}<br/>{address}<br/>{tel}<br/>{fax}'
            print(description)

            s_quote = urllib.parse.quote(address)
            response = requests.get(makeUrl + s_quote)
            print(response)
            print(response.text)

            if not response.text or not response.json():
                print(f"Geolocation not found: {name}")
                continue

            print(f"Geolocation found: {name}")
            lon_lat = response.json()[0]["geometry"]["coordinates"]
            if lon_lat and len(lon_lat) == 2:
                point_data.append(
                    {

                        "title": name,
                        "description": description,
                        "longitude": lon_lat[0],
                        "latitude": lon_lat[1],
                        "color": "#ff0000",
                    }
                )
            time.sleep(1)

    return point_data


def get_feature_collection(p_data):
    features = []
    for p in p_data:
        lat, lon = p["latitude"], p["longitude"]
        feature = Feature(
            geometry=Point((lon, lat)),
            properties={
                "title": p["title"],
                "description": p["description"],
                "marker-color": p["color"],
                "marker-size": "medium",
                "stroke": "#ffffff",
                "stroke-width": 2,
            },
        )
        features.append(feature)

    return FeatureCollection(features)


if __name__ == "__main__":
    input_file = f'address_book/{input_file_name}.csv'
    output_file = f"static/json/{input_file_name}.geojson"
    point_data = get_point_data(input_file)
    feature_collection = get_feature_collection(point_data)

    with open(output_file, "w") as f:
        dump(feature_collection, f, indent=2)
