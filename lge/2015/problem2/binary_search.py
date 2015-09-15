def binarySearch(array, value, low=0, high=0):
    if low > high:
            return False
    mid = (low+high) // 2
    if array[mid] > value:
            return binarySearch(array, value, low, mid-1)
    elif array[mid] < value:
            return binarySearch(array, value, mid+1, high)
    else:
            return mid

print binarySearch([1,3,5,6,9,15,20,40,50], 9, low=0, high=8)
print binarySearch([1,3,5,6,9,15,20,40,50], 15, low=0, high=8)
print binarySearch([1,3,5,6,9,15,20,40,50], 10, low=0, high=8)
