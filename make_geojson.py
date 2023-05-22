import csv
import time
import requests
import urllib
from geojson import Point, Feature, FeatureCollection, dump

makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
input_file = 'address_book/member_list.csv'
outfile = "static/json/no_tokyo_publisher.geojson"
tokyo_ku_dict = {
    'chiyoda': '千代田区',
    'chuo': '中央区',
    'minato': '港区',
    'shinjuku': '新宿区',
    'bunkyo': '文京区',
    'taito': '台東区',
    'sumida': '墨田区',
    'koto': '江東区',
    'shinagawa': '品川区',
    'meguro': '目黒区',
    'ota': '大田区',
    'setagaya': '世田谷区',
    'shibuya': '渋谷区',
    'nakano': '中野区',
    'suginami': '杉並区',
    'toshima': '豊島区',
    'kita': '北区',
    'arakawa': '荒川区',
    'itabashi': '板橋区',
    'nerima': '練馬区',
    'adachi': '足立区',
    'katsushika': '葛飾区',
    'edogawa': '江戸川区'
}


def get_point_data(file_name, selected_ku):
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        csv_reader = csv.reader(f)
        point_data = []

        for line in csv_reader:
            name = line[0]
            address = line[4]

            if f'東京都{selected_ku}' in address:
                s_quote = urllib.parse.quote(address)
                response = requests.get(makeUrl + s_quote)

                if not response.json():
                    print(f'Geolocation not found: {name}')
                    continue

                print(f'Geolocation found: {name}')
                lng_lat = response.json()[0]["geometry"]["coordinates"]
                if lng_lat and len(lng_lat) == 2:
                    point_data.append({
                        'title': name,
                        'description': address,
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
        feature = Feature(geometry=Point((lon, lat,)),
                          properties={'title': p['title'], 'description': p['description'], 'marker-color': p['color'],
                                      'marker-size': 'medium', 'stroke': '#ffffff', 'stroke-width': 2})
        features.append(feature)

    return FeatureCollection(features)


if __name__ == '__main__':
    for ku_en, ku in tokyo_ku_dict.items():
        output_file = f'static/json/{ku_en}_tokyo_publisher.geojson'
        point_data = get_point_data(input_file, ku)
        feature_collection = get_feature_collection(point_data)

        with open(output_file, 'w') as f:
            dump(feature_collection, f, indent=2)
