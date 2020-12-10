import networkx as nx
import numpy as np
from random import choice
import time
import matplotlib.pyplot as plt

def generate_random_graph(n):
    p = 2 / n * np.log(n)
    G = nx.gnp_random_graph(n, p)
    for u, v in G.edges:
        G.edges[u,v]["weight"] = np.random.randint(1, 1000)
    return G

def makeset(u, parent, rank):
    parent[u] = u
    rank[u] = 0

def find(x, parent):
    while x != parent[x]:
        x = parent[x]
    return x
    
def union(x, y, parent, rank):
    rx = find(x, parent)
    ry = find(y, parent)
    
    if rx == ry:
        return
    
    if rank[rx] > rank[ry]:
        parent[ry] = rx
    else:
        parent[rx] = ry
        if rank[rx] == rank[ry]:
            rank[ry] += 1
            
def kruskal(G):
    parent = [-1] * len(G)
    rank = [-1] * len(G)
    for u in G.nodes:
        makeset(u, parent, rank)
    x=[]
    total_weight = 0
    sorted_edge = sorted(G.edges(data=True), key = lambda t: t[2].get('weight', 1))
    
    for u, v, w in sorted_edge:
        if find(u, parent) != find(v, parent):
            total_weight += w['weight']
            x.append((u,v))
            union(u, v, parent, rank)
        
    return x, total_weight

heap_size = 0
def min_heapify(a, i, position):
    global heap_size
    left_i = (2*i)+1
    right_i = (2*i)+2
    
    min_i = i
    
    if right_i < heap_size and a[right_i][1] < a[i][1]:
        min_i = right_i
        
    if left_i < heap_size and a[left_i][1] < a[min_i][1]:
        min_i = left_i
        
    if min_i != i:
        position[a[min_i][0]] = i
        position[a[i][0]] = min_i

        a[i], a[min_i] = a[min_i], a[i]
        min_heapify(a, min_i, position)
    
def build_min_heap(a, position):
    n = heap_size
    for i in range((n-2)//2, -1, -1):
        min_heapify(a, i, position)

def deletemin(a, position):
    global heap_size
    n = heap_size
    if heap_size == 0:
        return
    
    position[a[n-1][0]] = 0
    position[a[0][0]] = n - 1
    
    res = a[0]
    a[0], a[n-1]= a[n-1], a[0]
    a.pop()
    
    heap_size -= 1
    min_heapify(a, 0, position)
    
    return res
    
def decrease_key(a, v, new_weight, position):
    idx = position[v]
    for i in range(heap_size):
        if a[i][0]==v:
            idx=i
            break
            
    a[idx][1] = new_weight
    
    parent = (idx-1)//2
    
    while idx > 0 and a[idx][1] < a[parent][1]:
        position[a[idx][0]] = parent
        position[a[parent][0]] = idx
        a[idx], a[parent] = a[parent], a[idx]
        idx = (idx-1)//2
        parent = (idx-1)//2


def prim(G):
    global heap_size
    cost = [float('inf')] * len(G)
    prev = [None] * len(G)
    s = np.random.randint(len(G))
    cost[s] = 0
    
    heap=[]
    position = [-1] * len(G)
    for i, node in enumerate(G):
        heap.append([node, cost[i]])
        position[node] = i
        
    heap_size = len(heap)
    build_min_heap(heap, position)
    while heap_size>0:
        u = deletemin(heap, position)
        u = u[0]
        for v in G.neighbors(u):
            w = G.edges[u, v]["weight"]
            if position[v] < heap_size and cost[v] > w:
                cost[v] = w
                prev[v] = u
                decrease_key(heap, v, cost[v], position)
    
    x = []
    total_weight = 0
    for i in range(len(G)):
        if prev[i] is not None:
            x.append((prev[i], i))
            total_weight += G.edges[prev[i], i]["weight"]
    return x, total_weight

def plot_time(title, k, p):
    plt.title(title)
    plt.xlabel("No. of nodes")
    plt.ylabel("Time (Seconds)")
    plt.plot(k)
    plt.plot(p)
    plt.legend(["Kruskel's", "Prim's"], loc ="lower right")
    plt.xticks(np.arange(10), ['1100', '1200', '1300', '1400', '1500', '1600', '1700', '1800', '1900', '2000'])
    plt.show()
    
# avg_k_time = []
# avg_p_time = []
# for i in range(11, 21):
#     sum_k_time = 0
#     sum_p_time = 0
#     for j in range(100):
#         n = i*100
#         G = generate_random_graph(n)
#         start = time.time()
#         k = kruskal(G)
#         sum_k_time += time.time()-start
#         start = time.time()
#         p = prim(G)
#         sum_p_time += time.time()-start
#     avg_k_time.append(sum_k_time/100)
#     avg_p_time.append(sum_p_time/100)
    
# plot_time("The average running times", avg_k_time, avg_p_time)
# print("Average Kruskal's:", avg_k_time)
# print("Average Prim's:", avg_p_time)

for i in range(11, 21):
    n = i*100
    G = generate_random_graph(n)
    k = kruskal(G)
    p = prim(G)
    
    print("kruskal: size:", n, "| no. of edges:", len(k[0]), "| weight:", k[1])
    print("prim: \t size:", n, "| no. of edges:", len(p[0]), "| weight:", p[1])


