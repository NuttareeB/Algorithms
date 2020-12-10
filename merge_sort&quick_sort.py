import numpy as np
import time
import matplotlib.pyplot as plt

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

def plot(merge_t, quick_t, title):
    plt.title(title)
    plt.xlabel("Array size")
    plt.ylabel("Time")
    plt.plot(merge_t)
    plt.plot(quick_t)
    plt.legend(["MergeSort", "QuickSort"], loc ="lower right") 
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
    for i in range(1000):
        random_arr = np.random.randint(-100, high=100, size=i).tolist()
        srt_perf(mergesort, random_arr, merge_t)
        srt_perf(quicksort, random_arr, quick_t) 
    plot(merge_t, quick_t, "performance for randomly sorted array")

#     sorted array input
    merge_t = []
    quick_t = []
    for i in range(1000):
        sorted_arr = sorted(np.random.randint(-100, high=100, size=i).tolist())
        srt_perf(mergesort, sorted_arr, merge_t)
        srt_perf(quicksort, sorted_arr, quick_t) 
    plot(merge_t, quick_t, "performance for array that is already sorted")

#perf()
print(mergesort([9,7,7,3,2,9,6,1]))
print(quicksort([9,7,7,3,2,9,6,1]))
