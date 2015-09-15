# coding:utf-8

from multiprocessing import Pool
from collections import deque
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
		[n, m] = map(int, lineList[idx].split(' '))
		l = []
		for j in range(m):
			idx += 1
			l.append( map(int, lineList[idx].split(' ')) )

		inputItem = {}
		inputItem['n'] = n
		inputItem['m'] = m
		inputItem['l'] = l
		inputList.append(inputItem)

	#pprint.pprint(inputList)

	return inputList

def calc(line):
	global l

	s = 0
	for (r1, r2) in l:
		#print r1, r2, l.index(r1), l.index(r2) 
		s += abs( line.index(r1) - line.index(r2) )
	return s

def recursive(oldLine, newLine=[]):
	#print "param : ", oldLine, newLine
	if len(oldLine) == 0:
		c = calc(newLine)
		#print c
		return c
	left = recursive(oldLine[1:], newLine+[oldLine[0]])
	right = recursive(oldLine[:-1], newLine+[oldLine[-1]])
	return min(left, right)

def solver(inputItem):
	global l

	n = inputItem['n']
	m = inputItem['m']
	l = inputItem['l']
	print "solver", n, m#, l

	minSum =  recursive(range(1,n+1))
	#print minSum
	return str(minSum)

def merger(outputList):
	return '\r\n'.join(outputList) + '\r\n'

if __name__ == '__main__':
	p = Problem(inputFile='problem3.in',
				outputFile='problem3.out',
				parser=parser,
				solver=solver,
				merger=merger,
				parallel=1)
	p.run()

