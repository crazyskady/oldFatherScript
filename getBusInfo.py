# coding: utf-8
import sys

stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr 
reload(sys)
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde 
sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup

def getLineList():
	headers      =  {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}
	lineInfo_url = 'http://nanjing.8684.cn'
	html_content = requests.get(lineInfo_url, headers=headers)

	Soup = BeautifulSoup(html_content.text, 'lxml')

	all_tag_a = Soup.find('div',class_='bus_kt_r1').find_all('a')

	line_list = []
	index = 0
	totalIndex = len(all_tag_a)
	for tag_a in all_tag_a:
		print("Progress: %d / %d" % (index, totalIndex))
		index = index + 1
		href_a = tag_a['href']
		html_url = lineInfo_url + href_a
		second_html_content = requests.get(html_url,headers=headers)

		Soup2 = BeautifulSoup(second_html_content.text, 'lxml')
		all_tag_a2 = Soup2.find('div',class_='cc_content').find_all('div')[-1].find_all('a')
		index2 = 0
		totalIndex2 = len(all_tag_a2)
		for tag_a2 in all_tag_a2:
			print("Progress: %d / %d (%d / %d)" % (index, totalIndex, index2, totalIndex2))
			index2 = index2 + 1
			if index2 == 2:
				return
			href_a2 = tag_a2['href']
			html_bus = lineInfo_url + href_a2

			thrid_html_content = requests.get(html_bus,headers=headers)
			Soup3 = BeautifulSoup(thrid_html_content.text, 'lxml')

			bus_name = Soup3.find('div',class_='bus_i_t1').find('h1').get_text()	
			information = [bus_name]
			line_list.append(information)

	fn = open("line_info.txt",'w')
	for line in line_list:
		fn.write(str(line)+'\n')
	fn.close()

def getLineDigitalArray():
	import re

	line_info   = open('line_info.txt', 'r')
	lines       = line_info.readlines()
	lineInfoSet = set()
	for idx, item in enumerate(lines):
		newStr = item.decode("unicode-escape")
		lineInfoSet.add(int(re.findall("\d+", newStr)[0]))
	lineInfoArr = list(lineInfoSet)
	lineInfoArr.sort()

	return lineInfoArr

def BusStations(buslist):
	busstation = []
	buslinename = buslist["name"]
	busstation.append(buslinename)
	stations = buslist["stations"]
	for station in stations:
		stationname = station["name"]
		busstation.append(stationname)
	return busstation

def getBusDetailInfo():
	import pickle
	import time

	lines = getLineDigitalArray()
	line_numbers = len(lines)
	counter      = 0

	busInfos = {}
	for i in lines:
		time.sleep(2)
		url = 'https://gaode.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12&city=320100&keywords=' + str(i) + '%E8%B7%AF'
		#url = 'https://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12&city=320100&keywords=' + str(i) + '%E8%B7%AF'
		json_obj = requests.get(url)

		data = json_obj.json()

		try:
			if (data["data"]["message"]) and (data["data"]["busline_list"]):
				buslists = data["data"]["busline_list"]  # busline
				print("-----------Line %d have %d lines: " % (i, len(buslists)))
				for idx, item in enumerate(buslists):
					buslist = buslists[idx]
					busstations = BusStations(buslist)
					if busstations[0].startswith(u"溧水") or busstations[0].startswith(u"高淳"):
						print("Skip Lishui and Gaocun>>>>>>>>>>>>>> ", busstations[0])
						continue
					busInfos[busstations[0]] = busstations[1:]

		except TypeError:
			print("Type Exception: %d", counter)
		else:
			counter = counter + 1
			print("Handling %d / %d" % (counter, line_numbers))

	with open("line_detail_dict.file", "wb") as f:
		pickle.dump(busInfos, f)

	return

def dumpBusDetailInfo():
	import pickle

	lines = getLineDigitalArray()
	with open("line_detail_dict.file", "rb") as f:
		d = pickle.load(f)

	location = open('busline_detail_Info.txt', 'w')

	# cleanup
	for lno in lines:
		testStr = str(lno) + u"路"
		tmpKey = []
		for i in d.keys():
			if i.startswith(testStr):
				tmpKey.append(i)

		tmpKey.sort()

		for j in tmpKey:
			location.write(j+"\n\n")
			location.write("-".join(d[j])+"\n\n")

	location.close()

getLineList()
getBusDetailInfo()
dumpBusDetailInfo()

