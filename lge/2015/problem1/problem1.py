# coding:utf-8

from multiprocessing import Pool
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
		n = int(lineList[idx])
		l = []
		for j in range(n):
			idx += 1
			l.append( lineList[idx].strip() )

		inputItem = {}
		inputItem['l'] = l
		inputList.append(inputItem)

	#pprint.pprint(inputList)

	return inputList

neighborList = [[False for j in range(10)] for i in range(10)]
neighborList[1][2] = '-'
neighborList[1][4] = '|'
neighborList[1][5] = '\\'
neighborList[2][1] = '-'
neighborList[2][3] = '-'
neighborList[2][4] = '/'
neighborList[2][5] = '|'
neighborList[2][6] = '\\'
neighborList[3][2] = '-'
neighborList[3][5] = '/'
neighborList[3][6] = '|'
neighborList[4][1] = '|'
neighborList[4][2] = '/'
neighborList[4][5] = '-'
neighborList[4][7] = '|'
neighborList[4][8] = '\\'
neighborList[5][1] = '\\'
neighborList[5][2] = '|'
neighborList[5][3] = '/'
neighborList[5][4] = '-'
neighborList[5][6] = '-'
neighborList[5][7] = '/'
neighborList[5][8] = '|'
neighborList[5][9] = '\\'
neighborList[6][2] = '\\'
neighborList[6][3] = '|'
neighborList[6][5] = '-'
neighborList[6][8] = '/'
neighborList[6][9] = '|'
neighborList[7][4] = '|'
neighborList[7][5] = '/'
neighborList[7][8] = '-'
neighborList[7][0] = '\\'
neighborList[8][4] = '\\'
neighborList[8][5] = '|'
neighborList[8][6] = '/'
neighborList[8][7] = '-'
neighborList[8][9] = '-'
neighborList[8][0] = '|'
neighborList[9][5] = '\\'
neighborList[9][6] = '|'
neighborList[9][8] = '-'
neighborList[9][0] = '/'
neighborList[0][7] = '\\'
neighborList[0][8] = '|'
neighborList[0][9] = '/'

directionList = [[[False for k in range(10)] for j in range(10)] for i in range(10)]
directionList[1][2][3] = True
directionList[3][2][1] = True
directionList[4][5][6] = True
directionList[6][5][4] = True
directionList[7][8][9] = True
directionList[9][8][7] = True
directionList[1][4][7] = True
directionList[7][4][1] = True
directionList[2][5][8] = True
directionList[8][5][2] = True
directionList[3][6][9] = True
directionList[9][6][3] = True
directionList[5][8][0] = True
directionList[0][8][5] = True
directionList[3][5][7] = True
directionList[7][5][3] = True
directionList[1][5][9] = True
directionList[9][5][1] = True

def calcPhoneNumberScore(number):
	global neighborList, directionList

	number = map(int, number)

	score = 0
	for i in range(1, len(number)):
		if i == 1:
			v1 = number[0]
			v2 = number[1]
			if v1 == v2: pass
			elif neighborList[v1][v2]:
				score += 1
			else:
				score += 2
		else:
			v1 = number[i-2]
			v2 = number[i-1]
			v3 = number[i]
			v12 = neighborList[v1][v2]
			v23 = neighborList[v2][v3]
			if v2 == v3: pass
			#elif v12 and v12 == v23:
			elif directionList[v1][v2][v3]:
				score += 1
			elif v23:
				score += 2
			else:
				score += 3

	return score

def solver(inputItem):
	minScore = None
	phoneNumber = ""

	for item in inputItem['l']:
		score = calcPhoneNumberScore(item)
		if minScore == None or minScore > score:
			minScore = score
			phoneNumber = item

	return phoneNumber

def merger(outputList):
	return '\r\n'.join(outputList) + '\r\n'

if __name__ == '__main__':
	p = Problem(inputFile='problem1.in',
				outputFile='problem1.out',
				parser=parser,
				solver=solver,
				merger=merger,
				parallel=4)
	p.run()

