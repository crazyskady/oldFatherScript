#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys

class metroNode(object):
	def __init__(self, name="Unknown"):
		self._nodeName      = name
		self._relationNodes = {}
		return

	def getNodeName(self):
		return self._nodeName

	def addRelationNode(self, relationNodeName, distance):
		if relationNodeName not in self._relationNodes.keys():
			self._relationNodes[relationNodeName] = distance
		return

	def getRelationNodes(self):
		return self._relationNodes

class metroLine(object):
	def __init__(self, line):
		self._nodes = []

		preNode = None
		preDist = 0
		curNode = None
		for idx, item in enumerate(line):
			if item.isdigit() == False: # means a node
				curNode = metroNode(item)
				if preNode != None:
					curNode.addRelationNode(preNode.getNodeName(), preDist)
					preNode.addRelationNode(curNode.getNodeName(), preDist)
				self._nodes.append(curNode)
				preNode = curNode

			else: # means a distance
				preDist = int(item)

		return

	def getNodes(self):
		return self._nodes

	def showLine(self):
		line = []
		for idx, item in enumerate(self._nodes):
			line.append(item.getNodeName())
		print(' - '.join(line))
		return


# ugly design, metroMap don't use metroNode...... 
class metroMap(object):
	def __init__(self):
		self._nodes = {}  # {"NodeA": {"NodeB":123}, "NodeB":{"NodeA":123, "NodeC":22}, "NodeC":{"NodeB":22}}
		self._traverseStack = []
		self._savedPaths = []
		return

	def getAllNodes(self):
		return self._nodes

	def addNewMetroLine(self, line):
		for idx, item in enumerate(line.getNodes()):
			if item.getNodeName() not in self._nodes.keys():
				self._nodes[item.getNodeName()] = item.getRelationNodes()
			else:
				# check the relation nodes
				curRelation = self._nodes[item.getNodeName()]
				newRelation = item.getRelationNodes()

				for idx1, item1 in enumerate(newRelation.keys()):
					if item1 not in curRelation.keys():
						self._nodes[item.getNodeName()][item1] = newRelation[item1]
		return

	def calculatePathLength(self, path):
		nodeList = path.split('--')
		totLen   = 0
		for idx, node in enumerate(nodeList):
			if idx == (len(nodeList) - 1):
				return totLen
			totLen = totLen + int(self._nodes[node][nodeList[idx+1]])

		return 0

	def calculatePrice(self, lineLen):
		if lineLen <= 10000:
			return 2
		elif lineLen <= 16000:
			return 3
		elif lineLen <= 22000:
			return 4
		elif lineLen <= 30000:
			return 5
		elif lineLen <= 38000:
			return 6
		elif lineLen <= 48000:
			return 7
		elif lineLen <= 58000:
			return 8
		elif lineLen <= 70000:
			return 9
		elif lineLen <= 84000:
			return 10
		else:
			return 11 + (lineLen - 84000) / 14000

	def getPaths(self, sNodeName, eNodeName):
		self._traverseStack = []
		self._savedPaths    = []
		self._getPaths(sNodeName, None, sNodeName, eNodeName)

		print("Find following pathes:")
		for idx, item in enumerate(self._savedPaths):
			print("%s, 总长度: %d" % (item, self.calculatePathLength(item)))
		return

	def getShortestPath(self, sNodeName, eNodeName, printLineFlag = False):
		self._traverseStack = []
		self._savedPaths    = []
		self._getPaths(sNodeName, None, sNodeName, eNodeName)
		shortestLen  = 99999999
		shortestLine = ""
		
		for idx, item in enumerate(self._savedPaths):
			curLen = self.calculatePathLength(item)
			if shortestLen > curLen:
				shortestLen  = curLen
				shortestLine = item
		print(("%s - %s 最短路径长度为: %d, 票价为: %d") % (sNodeName, eNodeName, shortestLen, self.calculatePrice(shortestLen)))
		if printLineFlag:
			print("路线为: %s\n" % (shortestLine,))
		if shortestLen == 99999999:
			print("-"*20)
			print("ERROR line: ", sNodeName, " -- ", eNodeName)
			for idx, item in enumerate(self._savedPaths):
				print(item)
			print("-"*20)
		return

	def _getPaths(self, cNodeName, pNodeName, sNodeName, eNodeName):
		if cNodeName != None and pNodeName != None and cNodeName == pNodeName:
			return False

		if cNodeName == None:
			return False

		i = 0
		self._traverseStack.append(cNodeName)
		if cNodeName == eNodeName:
			self._savedPaths.append('--'.join(self._traverseStack))
			return True
		else:
			relations = list(self._nodes[cNodeName].keys())
			relations.sort()
			nNodeName = relations[i]
			while nNodeName != None:
				if pNodeName != None and (nNodeName == sNodeName or nNodeName == pNodeName or nNodeName in self._traverseStack):
					i = i + 1
					if i >= len(relations):
						nNodeName = None
					else:
						nNodeName = relations[i]
					continue

				self._getPaths(nNodeName, cNodeName, sNodeName, eNodeName)

				i = i + 1
				if i >= len(relations):
					nNodeName = None
				else:
					nNodeName = relations[i]

				self._traverseStack.pop()
		return False

	def showMap(self):
		print(self._nodes)

pMap = metroMap()

njLine1 = ["迈皋桥", "1142", "红山动物园", "1121", "南京站", "1691", "新模范马路", "1061", "玄武门", "1254", "鼓楼", "862", "珠江路", "1147", "新街口", "1125", "张府园", "909", "三山街", "1914", "中华门", "2093", "安德门", "1455", "天隆寺", "1283", "软件大道", "1076", "花神庙", "1853", "南京南站", "2276", "双龙大道", "1345", "河定桥", "904", "胜太路", "1332", "百家湖", "1475", "小龙湾", "1135", "竹山路", "1919", "天印大道", "1312", "龙眠大道", "1550", "南医大江苏经贸学院", "2720", "南京交院", "1964", "中国药科大学"]
njLine2 = ["油坊桥", "2361", "雨润大街", "1622", "元通", "1262", "奥体东站", "1379", "兴隆大街", "1473", "集庆门大街", "1312", "云锦路", "1257", "莫愁湖", "1002", "汉中门", "874", "上海路", "745", "新街口", "1022", "大行宫", "1024", "西安门", "1300", "明故宫", "1521", "苜蓿园", "1307", "下马坊", "937", "孝陵卫", "1168", "钟灵街", "2779", "马群", "3015", "金马路", "1675", "仙鹤门", "1326", "学则路", "1519", "仙林中心", "1066", "羊山公园", "1947", "南大仙林校区", "1846", "经天路"]
njLine3 = ["林场", "2537", "星火路", "1049", "东大成贤学院站", "1127", "泰冯路", "1407", "天润城", "1854", "柳洲东路", "3535", "上元门", "961", "五塘广场", "1845", "小市", "1379", "南京站", "2017", "南京林业大学新庄", "2851", "鸡鸣寺", "858", "浮桥", "859", "大行宫", "931", "常府街", "1067", "夫子庙", "1308", "武定门", "1143", "雨花门", "977", "卡子门", "1153", "大明路", "1137", "明城大道", "1222", "南京南站", "1105", "宏运大道", "1826", "胜太西路", "1791", "天元西路", "2343", "九龙湖", "1526", "诚信大道",  "1301", "东大九龙湖校区", "2995", "秣周东路"]
njLine4 = ["龙江站", "1574", "草场门站", "1828", "云南路站", "821", "鼓楼", "1359", "鸡鸣寺", "807", "九华山站", "1391", "岗子村站", "2018", "蒋王庙站", "1128", "王家湾站", "2749", "聚宝山站", "2569", "徐庄站", "2564", "金马路", "3233", "汇通路站", "1187", "灵山站", "1938", "东流站", "2454", "孟北站", "2185", "桦墅站", "3212", "仙林湖站"]
njLine10= ["安德门", "2157", "小行", "1307", "中胜", "1400", "元通", "1865", "奥体中心", "848", "梦都大街", "1512", "绿博园", "1350", "江心洲", "4545", "临江青奥体育公园", "833", "浦口万汇城", "1134", "南京工业大学", "1427", "龙华路", "1154", "文德路", "1729", "雨山路"]
njLineS1= ["禄口机场", "7926", "翔宇路南", "4234", "翔宇路北", "7283", "正方中路", "4723", "吉印大道", "3242", "河海大学佛城西路", "3552", "翠屏山", "4077", "南京南站"]
njLineS3= ["南京南站", "1963", "景明佳园站", "1470", "铁心桥站", "1507", "春江路站", "1446", "贾西站", "1608", "油坊桥", "1187", "永初路站", "1154", "平良大街站", "949", "吴侯街站",  "1037", "高庙路站", "2007", "天保站", "1525", "刘村站", "9844", "马骡圩站", "2099", "兰花塘站", "1324", "双垅站", "1471", "石碛河站", "1350", "桥林新城站", "1998", "林山站", "1712", "高家冲站"]
njLineS7= ["禄口机场", "962", "空港新城江宁站", "5486", "柘塘站", "5502", "空港新城溧水站", "3138", "群力站", "5236", "卧龙湖站", "2423", "溧水站", "1529", "中山湖站", "2261", "幸庄站", "1229",  "无想山站"]
njLineS8= ["泰山新村", "1236", "泰冯路", "2741", "高新开发区", "2830", "信息工程大学", "1401", "卸甲甸", "1829", "大厂", "2151", "葛塘", "3880", "长芦", "1567", "化工园", "2893", "六和开发区", "2077", "龙池", "2375", "雄州", "1606", "凤凰山公园", "1475", "方州广场", "6112", "沈桥", "4971", "八百桥", "5475", "金牛湖"]
njLineS9= ["翔宇路南", "10003", "铜山站", "7374", "石湫站", "11219", "明觉站", "16912", "团结圩", "6232", "高淳站"]

Lines = [njLine1, njLine2, njLine3, njLine4, njLine10, njLineS1, njLineS3, njLineS7, njLineS8, njLineS9]

for line in Lines:
	pline = metroLine(line)
	#pline.showLine()
	pMap.addNewMetroLine(pline)

#pMap.showMap()
#pMap.getShortestPath("百家湖", "张府园", True)
pMap.getShortestPath("上海路", "马群", True)
pMap.getShortestPath("上海路", "金马路", True)
#pMap.getPaths("中国药科大学", "张府园")
#pMap.getPaths("百家湖", "新街口")
'''
nodeNames = list(pMap.getAllNodes().keys())
nodeNum   = len(nodeNames)
for idx, item in enumerate(nodeNames):
	if (idx+1) == (nodeNum-1):
		print("遍历完成！！！")
		sys.exit(0)

	for idx1, item1 in enumerate(nodeNames):
		if item == item1:
			continue
		pMap.getShortestPath(item, item1)
'''