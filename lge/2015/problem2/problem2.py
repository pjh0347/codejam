# coding:utf-8

from multiprocessing import Pool
import bisect
import pprint

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
		[n, k, w] = map(int, lineList[idx].split(' '))
		l = []
		for j in range(n):
			idx += 1
			#l.append( lineList[idx].strip() )
			l.append( map(int, lineList[idx].split(' ')) )

		inputItem = {}
		inputItem['n'] = n
		inputItem['k'] = k
		inputItem['w'] = w
		inputItem['l'] = l
		inputList.append(inputItem)

	#pprint.pprint(inputList)

	return inputList

def solver(inputItem):
	n = inputItem['n']
	k = inputItem['k']
	w = inputItem['w']
	print "solver", n,k,w

	minX = None
	maxX = None
	minY = None
	maxY = None
	yDict = {}
	outsideYDict = {}

	if n <= 3:
		return 'YES'

	for item in inputItem['l']:
		[x, y] = item
		if minX == None:
			minX = x
			maxX = x
			minY = y
			maxY = y
		else:
			minX = min(x, minX)
			maxX = max(x, maxX)
			minY = min(y, minY)
			maxY = max(y, maxY)
		if not yDict.has_key(y):
			yDict[y] = 0
		yDict[y] += 1

	for item in inputItem['l']:
		[x, y] = item
		if (x > minX + w) and (x < maxX - w):
			outsideYDict[y] = None

	yList = sorted(yDict.keys())
	#print yList

	outsideYList = sorted(outsideYDict.keys())
	#print outsideYList

	tmpSum = 0
	ySumList = []
	for y in yList:
		tmpSum += yDict[y]
		ySumList.append(tmpSum)

	if len(outsideYList) == 0:
		return 'YES'
	elif len(outsideYList) == 1:
		if outsideYList[0] in [yList[0], yList[-1]]:
			return 'YES'
		else:
			for i in range(w+1):
				lowerY = filter(lambda v: v < outsideYList[0] - w + i, yList)
				lowerYCnt = 0
				for y in lowerY:
					lowerYCnt += yDict[y]
				upperY = filter(lambda v: v > outsideYList[0] + i, yList)
				upperYCnt = 0
				for y in upperY:
					upperYCnt += yDict[y]
				if min(lowerYCnt, upperYCnt) <= k:
					return 'YES'
			return 'NO'
	elif len(outsideYList) >= 2:
		if (outsideYList[0] <= yList[0] + w) and (outsideYList[1] >= yList[-1] - w):
			return 'YES'
		else:
			tmpList = []
			if yList[0] != outsideYList[0]:
				tmpList.append(yList[0])
			tmpList += outsideYList
			if yList[-1] != outsideYList[-1]:
				tmpList.append(yList[-1])

			for i in range(len(tmpList)-1):
				#if i % 100 == 0: print "i = ", i
				lowerYCnt = 0
				idx = bisect.bisect_left(yList, tmpList[i]-w)
				if idx:
					lowerYCnt = ySumList[idx-1]
				upperYCnt = 0
				idx = bisect.bisect_right(yList, tmpList[i+1]+w)
				if idx != len(yList):
					upperYCnt = ySumList[-1] - ySumList[idx-1]
				if lowerYCnt + upperYCnt <= k:
					return 'YES'
			return 'NO'

def merger(outputList):
	return '\r\n'.join(outputList) + '\r\n'

if __name__ == '__main__':
	p = Problem(inputFile='problem2.in',
				outputFile='problem2.out',
				parser=parser,
				solver=solver,
				merger=merger,
				parallel=4)
	p.run()

