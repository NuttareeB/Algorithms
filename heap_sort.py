import numpy as np
import time
import matplotlib.pyplot as plt
#--------------------------------------- heap part

def max_heapify(a, i, n):
    left_i = (2*i)+1
    right_i = (2*i)+2
    
    max_i = i
    
    if right_i < n and a[right_i] > a[i]:
        max_i = right_i
        
    if left_i < n and a[left_i] > a[max_i]:
        max_i = left_i
        
    if max_i != i:
        a[i], a[max_i] = a[max_i], a[i]
        max_heapify(a, max_i, n)
    
def build_max_heap(a):
    n = len(a)
    for i in range((n-2)//2, -1, -1):
        max_heapify(a, i, n)
        
def heapsort(a):
    build_max_heap(a)
    n = len(a)
    
    for i in range(n-1, 0, -1):
        a[i], a[0] = a[0], a[i]
        max_heapify(a, 0, i)
        
    return a
        
#--------------------------------------- heap part

def mergesort(arr):
    if len(arr) < 2:
        return arr

    half = len(arr)//2
    left = mergesort(arr[0:half])
    right = mergesort(arr[half:len(arr)])

    res = []
    while left and right:
        if left[0] < right[0]:
            res.append(left.pop(0))
        else:
            res.append(right.pop(0))
        
    if left:
        res.extend(left)
    if right:
        res.extend(right)
    
    return res

def quicksort(arr):
    if len(arr) < 2:
        return arr
    
    pivot = arr[0]
    left = [x for x in arr if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    
    return quicksort(left) + [pivot] + quicksort(right)

def plot(merge_t, quick_t, heap_t, title):
    plt.title(title)
    plt.xlabel("Array size")
    plt.ylabel("Time")
    plt.plot(merge_t)
    plt.plot(quick_t)
    plt.plot(heap_t)
#     plt.legend(["MergeSort", "HeapSort"], loc ="upper left")
    plt.legend(["MergeSort", "QuickSort", "HeapSort"], loc ="upper left")
    plt.show()
    
def srt_perf(fn, a_input, time_arr):
    start = time.time()
    merge_res = fn(a_input)
    end = time.time()
    time_arr.append(end-start)
    
def perf():
    
#     random array input
    merge_t = []
    quick_t = []
    heap_t = []
    for i in range(3000):
        random_arr = np.random.randint(-100, high=100, size=i).tolist()
        srt_perf(mergesort, random_arr, merge_t)
        srt_perf(quicksort, random_arr, quick_t)
        srt_perf(heapsort, random_arr, heap_t)
    plot(merge_t, quick_t, heap_t, "performance for randomly sorted array")

#     sorted array input
    merge_t = []
    quick_t = []
    heap_t = []
    for i in range(2500):
        sorted_arr = sorted(np.random.randint(-100, high=100, size=i).tolist())
        srt_perf(mergesort, sorted_arr, merge_t)
        srt_perf(quicksort, sorted_arr, quick_t)
        srt_perf(heapsort, sorted_arr, heap_t)
    plot(merge_t, quick_t, heap_t, "performance for array that is already sorted")

#----------------------------------------Kth element----------------------------------------------
def kth_element(arr1, arr2, begin1, begin2, end1, end2, k) :

# let n = length of array 1
# let m = length of array 2
# to handle the case that k is out of bound
    if k > len(arr1) + len(arr2) - 1:
        return "no element"
    
# output from another array when there is no remaining element needed to be considered from another array
# when an 2 pointers of an array has reach the same point (begin = end),
# it means that we will consider k's element from another array
    if begin1 == end1:
        return arr2[begin2+k]
    if begin2 == end2:
        return arr1[begin1+k]
    
# find the middle point of each array input
    mid1 = (end1 - begin1) // 2
    mid2 = (end2 - begin2) // 2

    if k > mid1 + mid2:
# If k > mid1 + mid2, we know that the index that we are looking for is either on the higher value side of
# one array or it is in another array.
        if arr1[begin1+mid1] > arr2[begin2+mid2]:
# If k > mid1 + mid2 and the value where the mid1 pointer points in array1 is more than
# the value where the mid2 pointer points in array2, we know that we can ignore
# the small value of arr2 from the begining to the element that mid2 points to.
# therefore, we will set the new begin2 pointer to begin2 + mid2 + 1

# as we reduce the array size by half in array2, the time complexity will be T(m/2)
            return kth_element(arr1, arr2, begin1, begin2 + mid2 + 1, end1, end2, k - mid2 - 1);
        else:
# If k > mid1 + mid2 and the value where the mid1 pointer points in array1 is less than or equal to
# the value where the mid2 pointer points in array2, we know that we can ignore
# the small value of arr1 from the begining to the element that mid1 points to.
# therefore, we will set the new begin1 pointer to begin1 + mid1 + 1

# as we reduce the array size by half in array2, the time function will be T(n/2)
            return kth_element(arr1, arr2, begin1 + mid1 + 1, begin2, end1, end2, k - mid1 - 1)

    else:
# In the case that k <= mid1 + mid2, we know that we can ignore half of the part of one of the arrays
# that has the middle value more than another array.
        if arr1[begin1+mid1] > arr2[begin2+mid2] :
# When middle value of the position that we pay attention to in array1 is more than array2,
# we can move the pointer that points to the end of array1 to middle part of the space we are considering.

# Therefore, we can reduce number of elements in array1 that we focus on by half,
# which bring the time function to T(n/2)
            return kth_element(arr1, arr2, begin1, begin2, begin1 + mid1, end2, k)
        else:
# This part do the same thing as the if condition but in this case the middle of the space
# ,that we pay attention to, in array2 is more than or equal to the middle element's value in array 1.

# Therefore, we can reduce number of elements in array2 that we focus on by half,
# which bring the time function to T(m/2)
            return kth_element(arr1, arr2, begin1, begin2, end1, begin2 + mid2, k)

random_arr = np.random.randint(-10, high=10, size=10)
print("random arr:", random_arr)
print("heap sort:", heapsort(random_arr))
print()
print("kth element")
arr1 = [2,4,6,7]
arr2 = [1,3,5,8]
for k in range(8):
    res = kth_element(arr1, arr2, 0, 0, len(arr1), len(arr2),  k)
    print("k:", k, ", res:", res)
