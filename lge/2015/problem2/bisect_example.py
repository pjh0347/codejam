import bisect

def findGT(a, x):
	i = bisect.bisect_right(a, x)
	return i

def findLT(a, x):
	i = bisect.bisect_left(a, x)
	return i - 1

print findGT([1,3,5,6,9,15,20,40,50], 9)
print findGT([1,3,5,6,9,15,20,40,50], 15)
print findGT([1,3,5,6,9,15,20,40,50], 10)
print findGT([1,3], 2)
print findGT([1,3], 4)
print "--------------------------------"
print findLT([1,3,5,6,9,15,20,40,50], 9)
print findLT([1,3,5,6,9,15,20,40,50], 15)
print findLT([1,3,5,6,9,15,20,40,50], 10)
print findLT([1,3], 2)
print findLT([1,3], 4)
print findLT([1,3], 0)

def index(a, x):
	'Locate the leftmost value exactly equal to x'
	i = bisect_left(a, x)
	if i != len(a) and a[i] == x:
		return i
	raise ValueError

def find_lt(a, x):
	'Find rightmost value less than x'
	i = bisect_left(a, x)
	if i:
		return a[i-1]
	raise ValueError

def find_le(a, x):
	'Find rightmost value less than or equal to x'
	i = bisect_right(a, x)
	if i:
		return a[i-1]
	raise ValueError

def find_gt(a, x):
	'Find leftmost value greater than x'
	i = bisect_right(a, x)
	if i != len(a):
		return a[i]
	raise ValueError

def find_ge(a, x):
	'Find leftmost item greater than or equal to x'
	i = bisect_left(a, x)
	if i != len(a):
		return a[i]
	raise ValueError

