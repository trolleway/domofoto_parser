# domofoto_parser
parser for http://domofoto.ru cc-by-sa data: ex-USSR building information

# Usage

* Set in parce_city.py city code (from http://domofoto.ru/cities/)
* pip install pip install beautifulsoup4
* python parce_city.py

# Output

Output is a csv file with buildings coordinates and data field. Data licensed as cc-by-sa (http://domofoto.ru/rules/)
You can open csv in NextGIS QGIS.
I do not include address tags, because they not license-clean: almost all addreses taken from googlemaps. If you need addreses - make SPATIAL JOIN with OSM data in NextGIS QGIS or PostGIS

If you want more GIS toolchain - script printing command string for ogr2ogr utility - it process csv to geojson, so you can put data in modern software.

# Watch domofoto.ru data in android

You can view geojson on map and watch all attributes in NextGIS Mobile.
https://play.google.com/store/apps/details?id=com.nextgis.mobile
http://docs.nextgis.ru/docs_ngmobile/source/toc.html
