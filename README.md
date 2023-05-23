# FASTAPI SERVER

営業地図をPythonで作成するためのサーバー

## 概要

Python FastAPI Serverで、Webサーバーを立てる。  
Jinja2で、HTMLをレンダリングする。  
make_geojson.pyで、CSVからGeojsonを作成する。  
capture_screen.pyで、Selenium Webdriverでスクリーンショットを撮る。  

## 仕様

- [x] FastAPI
- [x] Jinja2
- [x] Selenium
- [x] Geojson
- [x] Requests
- [x] Uvicorn
- [x] Chromedriver

## ディレクトリ構成

```Console
root --- main.py (FastAPI)
     |--- templates --- index.html (jinja2)
     |--- static
     |      |--- css --- sytle.css
     |      |--- geojson --- hoge.geojson (make_geojson.py)
     |--- address_book --- address_book.csv (make_geojson.py)
     |--- screenshot --- screenshots.png (capture_screen.py)
     |--- make_geojson.py
     |--- capture_screen.py
     |--- README.md
     |--- requirements.txt
```

## package install

```Console
$ pip install fastapi uvicorn jinja2 requests geojson selenium
```

## server start

```Console
$ uvicorn main:app --reload

or

$ python -m uvicorn main:app --reload
```

## Geojson

csvからgeojsonを作成する。住所録の形式により、変更が必要。

```Console
$ python make_geojson.py
```

## Screenshots (Selenium Webdriver) --- Not working

Selenium Webdriverでスクリーンショットを撮る。地図の描画に時間がかかりすぎて、読み込み中の画面が撮れてしまう。

```Console
$ brew install chromedriver (Mac)
$ python capture_screen.py
```