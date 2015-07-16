#!/usr/bin/env python
# -*- coding: utf-8 -*-

# anchor extraction from html document
from bs4 import BeautifulSoup
import urllib2
import urlparse
import re
import csv
import time


cityId='712'









webpage = urllib2.urlopen('http://domofoto.ru/list.php?cid='+cityId)
soup = BeautifulSoup(webpage)
maxST=0
for element in soup.find_all('a'):
	url=element.get('href', '/')
	if url.find('st')>0: #TODO rename
		par = urlparse.parse_qs(urlparse.urlparse(url).query)
		currentST=int(par['st'][0])
		if currentST > maxST:
			maxST=currentST
#print 'max st='+str(maxST)
#получили смещение максимальной страницы города

#определение списка адресов отдельных страниц домов города
recPerPage=30
pagesCount = maxST // recPerPage

housesPages=[]

for pageST in range(0,pagesCount+1): #
	url="http://domofoto.ru/list.php?cid="+cityId+"&st="+str(pageST*recPerPage)
	#print url
	housesPages.append(url)

#print housesPages

housesIds=[]
housenumber=0
allhousescnt=pagesCount*recPerPage

for housePage in housesPages:
	
	webpage = urllib2.urlopen(housePage)
	soup = BeautifulSoup(webpage)
	for element in soup.find_all('a'):
		url=element.get('href', '/')
		if url.find('house')>0: #TODO rename
			#print url
			houseId=url[7:-1]
			#print houseId
			housesIds.append(houseId)

#print housesIds
webpage=0

from time import gmtime, strftime


csvFileName='domofoto_'+strftime("%Y-%m-%d-%H-%M-%S", gmtime())
writer = csv.writer(open(csvFileName+'.csv', 'w'))
writer.writerow(['x','y','projectCode','projectName','seriesCode','seriesName','constructionStartDate','constructionEndDate','mode','levels'])

#write vrt file for open csv in ogr2ogr
vrt_file='''
<OGRVRTDataSource>
  <OGRVRTLayer name="'''+csvFileName+'''">
        <LayerSRS>WGS84</LayerSRS>
        <SrcDataSource>'''+csvFileName+'''.csv</SrcDataSource>
        <GeometryType>wkbPoint</GeometryType>
        <GeometryField encoding="PointFromColumns" x="x" y="y"/>
    </OGRVRTLayer>
</OGRVRTDataSource>
'''
vrtf = open(csvFileName+".vrt","w")
vrtf.write(vrt_file)
vrtf.close()


for houseId in housesIds:
	housenumber=housenumber+1 #for progress display 
	housePageURL='http://domofoto.ru/house/'+houseId+'/'
	print housePageURL + ' ' +str(housenumber) + '/'+str(allhousescnt)


	constructionEndDate=''
	constructionStartDate=''
	seriesCode=''
	seriesName=''
	projectCode=''
	projectName=''
	mode=''
	levels=''

	webpage = urllib2.urlopen(housePageURL)
	#soup = BeautifulSoup(webpage)
	html = webpage.read()

	coordsPart=re.search('initialize\(\[(.+?), ',html)
	if coordsPart:
		y = coordsPart.group(1)

	coordsPart=re.search(',(.+?)\], true',html)
	if coordsPart:
		x = coordsPart.group(1)

	coordsPart=re.search('Проект.*projects/(.+?)/',html)
	if coordsPart:
		projectCode = coordsPart.group(1)

	coordsPart=re.search('Серия.*projects/(.+?)/',html)
	if coordsPart:
		seriesCode = coordsPart.group(1)

	coordsPart=re.search('Проект.*proj.*>(.+?)</a>',html)
	if coordsPart:
		projectName = coordsPart.group(1)

	coordsPart=re.search('Серия.*proj.*>(.+?)</a>',html)
	if coordsPart:
		seriesName = coordsPart.group(1)

	coordsPart=re.search('Окончание.*строительства.*<b>(.+?)</b>',html)
	if coordsPart:
		constructionEndDate = coordsPart.group(1)

	coordsPart=re.search('Начало.*строительства.*<b>(.+?)</b>',html)
	if coordsPart:
		constructionStartDate = coordsPart.group(1)

	coordsPart=re.search('Текущее состояние.*&nbsp;(.+?)&nbsp;</td></tr>',html)
	if coordsPart:
		mode = coordsPart.group(1)

	coordsPart=re.search('Этажность.*d">(.+?)</td></tr>',html)
	if coordsPart:
		levels = coordsPart.group(1)




	row=[x,y,projectCode,projectName,seriesCode,seriesName,constructionStartDate,constructionEndDate,mode,levels]
	writer.writerow(row)	

	#quit()
	#print html

ogr2ogrString='''ogr2ogr -overwrite -f "GeoJSON" '''+csvFileName+'''.geojson '''+csvFileName+'''.vrt'''
print ogr2ogrString
