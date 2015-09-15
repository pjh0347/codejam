# coding:utf-8

NOTICE = """
###############################################################################################
# PyPy (http://pypy.org/) 로 실행 해주세요.                                                   #
# Python (https://www.python.org/) 으로 실행 시 제한된 시간 내에 출력되지 않을 수 있습니다.   #
###############################################################################################
"""

from multiprocessing import Pool
import pprint
import os
import time

class Problem(object):

	def __init__(self, inputFile, outputFile, parser, solver, merger, parallel=1):
		object.__init__(self)
		self.inputFile = inputFile
		self.outputFile = outputFile
		self.parser = parser
		self.solver = solver
		self.merger = merger
		self.pool = Pool(processes=parallel)
	
	def run(self):
		inputData = self.read()
		inputList = self.parser(inputData)
		outputList = self.solve(inputList)
		outputData = self.merger(outputList)
		self.write(outputData)

	def read(self):
		f = open(self.inputFile)
		inputData = f.read()
		f.close()
		return inputData

	def write(self, outputData):
		f = open(self.outputFile, 'w')
		f.write(outputData)
		f.close()

	def solve(self, inputList):
		return self.pool.map(self.solver, inputList)

def parser(inputData):
	inputList = []

	lineList = inputData.splitlines()
	#print lineList

	idx = 0
	t = int(lineList[idx])

	for i in range(t):
		idx += 1
		[n, k] = map(int, lineList[idx].split(' '))
		linkList = []
		for j in range(n-1):
			idx += 1
			linkList.append( map(int, lineList[idx].strip().split(' ')) )
		roomList = []
		for j in range(k):
			idx += 1
			try: roomList.append( map(int, lineList[idx].strip().split(' ')) )
			except: print lineList[idx]
		inputItem = {}
		inputItem['n'] = n
		inputItem['k'] = k
		inputItem['linkList'] = linkList
		inputItem['roomList'] = roomList
		inputList.append(inputItem)

	#pprint.pprint(inputList)

	return inputList

class Node(object):

	def __init__(self, roomNumber):
		self.roomNumber = roomNumber
		self.parentNode = None
		self.childNode = []
		self.depth = 0

	def __str__(self):
		if self.parentNode == None:
			return "Node(number:%d, parent:None, depth:0)" % self.roomNumber
		else:
			return "Node(number:%d, parent:%d, depth:%d)" % \
				(self.roomNumber, self.parentNode.roomNumber, self.depth)

def solver(inputItem):
	n = inputItem['n']
	k = inputItem['k']
	linkList = inputItem['linkList']
	roomList = inputItem['roomList']
	print "solver", n, k

	rootNode = None
	nodeList = [None for i in range(500001)]
	for link in linkList:
		[number1, number2] = link
		if nodeList[number1] == None:
			nodeList[number1] = Node(number1)
		if nodeList[number2] == None:
			nodeList[number2] = Node(number2)
		if rootNode == None:
			rootNode = nodeList[number1] 

	for link in linkList:
		[number1, number2] = link
		node1 = nodeList[number1]
		node2 = nodeList[number2]
		if node1 == rootNode or node1.parentNode:
			node2.parentNode = node1
			node2.depth = node1.depth + 1
			node1.childNode.append(node2)
		elif node2.parentNode:
			node1.parentNode = node2
			node1.depth = node2.depth + 1
			node2.childNode.append(node1)
		else:
			print node1, node2
			raise Exception

	leafNodeList = []
	for node in nodeList:
		if node and len(node.childNode) == 0:
			leafNodeList.append(node)
	leafNodeList = filter(lambda x: x.depth >= 10000, leafNodeList)
	leafNodeList = sorted(leafNodeList, cmp=lambda x,y: x.depth-y.depth, reverse=True)

	cacheList = []
	if len(leafNodeList) > 0:
		leafNode = leafNodeList[0]
		tmpNode = leafNode
		cacheList = [None for i in range(leafNode.depth+1)]
		for i in range(leafNode.depth+1):
			cacheList[leafNode.depth-i] = tmpNode
			tmpNode = tmpNode.parentNode
	print "cacheList len : ", len(cacheList)

	print "[%d] search start." % os.getpid()
	retList = []
	cnt = 0
	for roomNumber in roomList:
		if cnt % 100 == 0: print "[%d] %d" % (os.getpid(), cnt)
		cnt += 1
		[number1, number2] = roomNumber
		node1 = nodeList[number1]
		node2 = nodeList[number2]

		cacheFound = False
		depthDiff = node1.depth - node2.depth
		node1Path = [node1]
		node2Path = [node2]
		if depthDiff > 0:
			if depthDiff > 10000 and cacheList:
				try:
					node1Idx = cacheList.index(node1)
					node1 = cacheList[node1Idx-depthDiff]
					cacheFound = True
				except ValueError:
					pass
			if not cacheFound:
				for i in range(1, depthDiff+1):
					node1 = node1.parentNode
					node1Path.append(node1)
		elif depthDiff < 0:
			if -depthDiff > 10000 and cacheList:
				try:
					node2Idx = cacheList.index(node2)
					node2 = cacheList[node2Idx+depthDiff]
					cacheFound = True
				except ValueError:
					pass
			if not cacheFound:
				for i in range(1, -depthDiff+1):
					node2 = node2.parentNode
					node2Path.append(node2)

		for i in range(1, node1.depth+1):
			if node1.roomNumber == node2.roomNumber:
				break
			else:
				node1 = node1.parentNode
				node2 = node2.parentNode
				if not cacheFound:
					node1Path.append(node1)
					node2Path.append(node2)

		if cacheFound:
			nodePathCnt = (nodeList[number1].depth - node1.depth) + (nodeList[number2].depth - node1.depth) + 1
			if nodePathCnt % 2 == 0:
				if depthDiff >= 0:
					middleRoomNumber = cacheList[nodeList[number1].depth-(nodePathCnt//2)+1].roomNumber
				else:
					middleRoomNumber = cacheList[nodeList[number2].depth-(nodePathCnt//2)].roomNumber
			else:
				if depthDiff >= 0:
					middleRoomNumber = cacheList[nodeList[number1].depth-nodePathCnt//2].roomNumber
				else:
					middleRoomNumber = cacheList[nodeList[number2].depth-nodePathCnt//2].roomNumber
			#print "#####", nodeList[number1].depth, nodeList[number2].depth, node1.depth, nodePathCnt, middleRoomNumber
		else:
			node1Path.pop()
			node2Path.reverse()
			nodePath = node1Path + node2Path
			nodePathCnt = len(nodePath)
			if nodePathCnt % 2 == 0:
				middleRoomNumber = nodePath[(nodePathCnt//2)-1].roomNumber
			else:
				middleRoomNumber = nodePath[nodePathCnt//2].roomNumber

		retList.append( str(middleRoomNumber) )

	ret = '\r\n'.join(retList)
	print "[%d] search end." % os.getpid()
	return ret

def merger(outputList):
	return '\r\n'.join(outputList) + '\r\n'

if __name__ == '__main__':
	print NOTICE
	p = Problem(inputFile='problem4.in',
				outputFile='problem4.out',
				parser=parser,
				solver=solver,
				merger=merger,
				parallel=4)
	p.run()

