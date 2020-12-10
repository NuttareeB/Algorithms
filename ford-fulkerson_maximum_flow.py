import networkx as nx
import numpy as np
import heapq as hq
from random import choice
import time
import matplotlib.pyplot as plt
import statistics

def generate_random_graph(n):
    p = 2 / n * np.log(n)
    G = nx.gnp_random_graph(n, p, directed=True)
    for u, v in G.edges:
        G.edges[u,v]["weight"] = np.random.randint(1, 101) # np random; the high value is exclusive
    return G

def short_pipes(G, s, t, parent):
    #BFS
    visited = [False] * len(G)
    queue = []
    queue.append(s)
    
    while queue:
        u = queue.pop();
        for v in G.neighbors(u):
            w = G.edges[u,v]["weight"]
            if not visited[v] and w > 0:
                queue.append(v)
                visited[v] = True;
                parent[v] = u
    return True if visited[t] else False

heap_size = 0
def max_heapify(a, i, position):
    global heap_size
    left_i = (2*i)+1
    right_i = (2*i)+2
    
    min_i = i
    
    if right_i < heap_size and a[right_i][1] > a[i][1]:
        min_i = right_i
        
    if left_i < heap_size and a[left_i][1] > a[min_i][1]:
        min_i = left_i
        
    if min_i != i:
        position[a[min_i][0]] = i
        position[a[i][0]] = min_i

        a[i], a[min_i] = a[min_i], a[i]
        max_heapify(a, min_i, position)
    
def build_max_heap(a, position):
    global heap_size
    n = heap_size
    for i in range((n-2)//2, -1, -1):
        max_heapify(a, i, position)
        
def deletemax(a, position):
    global heap_size
    n = heap_size
    if n == 0:
        return
    
    position[a[n-1][0]] = 0
    position[a[0][0]] = n - 1
    
    res = a[0]
    a[0], a[n-1]= a[n-1], a[0]
    a.pop()
    
    heap_size -= 1
    max_heapify(a, 0, position)
    
    return res

def increase_key(a, v, new_weight, position):
    idx = position[v]
    for i in range(heap_size):
        if a[i][0]==v:
            idx=i
            break
    a[idx][1] = new_weight
    
    parent = (idx-1)//2
    while idx > 0 and a[idx][1] > a[parent][1]:
        position[a[idx][0]] = parent
        position[a[parent][0]] = idx
        a[idx], a[parent] = a[parent], a[idx]
        idx = (idx-1)//2
        parent = (idx-1)//2

def fat_pipes(G, s, t, parent):
    global heap_size
    flow = [0] * len(G)
    flow[s] = float('inf')
    position = [-1] * len(G)
    
    heap=[]
    for i, node in enumerate(G):
        heap.append([node, flow[i]])
        position[node] = i
    
    heap_size = len(heap)
    build_max_heap(heap, position)
    while heap_size>0:
        u = deletemax(heap, position)
        u = u[0]
        for v in G.neighbors(u):
            w = G.edges[u, v]["weight"]
            if flow[v] < min(flow[u], w):
                flow[v] = min(flow[u], w)
                parent[v] = u
                increase_key(heap, v, flow[v], position)
                
    return True if flow[t]>0 else False
    
def ford_fulkerson(G, s, t, func):
    parent = [-1] * len(G)
    max_flow = 0
    
    residual_net = set()
    path_flows = []
    while func(G, s, t, parent):
        path_flow = float("Inf")
        sink = t
        while(sink != s):
            path_flow = min(path_flow, G.edges[parent[sink], sink]["weight"])
            sink = parent[sink]
    
        path_flows.append(path_flow)
        max_flow += path_flow
        
        v = t
        while(v != s):
            u = parent[v]
            G.edges[u, v]["weight"] -= path_flow
            if G.has_edge(v, u):
                G.edges[v, u]["weight"] += path_flow
            else:
                G.add_edge(v, u, weight=path_flow)
            residual_net.add((v,u))
            v = parent[v]
            
    res_flow = []
    for v, u in residual_net:
        if G.edges[v, u]["weight"] > 0:
            res_flow.append((u, v, G.edges[v, u]["weight"]))
    return max_flow, res_flow, path_flows

def plot_time(title, k, p):
    plt.title(title)
    plt.xlabel("No. of nodes")
    plt.ylabel("Time (Seconds)")
    plt.plot(k)
    plt.plot(p)
    plt.legend(["Short pipes", "Fat pipes"], loc ="lower right")
    plt.xticks(np.arange(10), ['100', '200', '300', '400', '500', '600', '700', '800', '900', '1000'])
    plt.show()
    
def flow():
    avg_time_short = []
    avg_time_fat = []
    count = 0
    for i in range(1, 11):
        n = i*100
        G = generate_random_graph(n)
        s = np.random.choice(G.nodes(), 1)[0]
        u = s
        for i in range(10000):
            u = np.random.choice(list(G.neighbors(u)), 1)[0]
        t = u
        short_pipes_graph = G.copy()
        fat_pipes_graph = G
        time_each_short = []
        time_each_fat = []
#         for _ in range(100):
#             start = time.time()
#             short_pipes_res = ford_fulkerson(short_pipes_graph, s, t, short_pipes)
#             time_each_short.append(time.time()-start)
#     #         print("size:", n)
#     #         print("short pipes max flow:\t", short_pipes_res[0], "\trunning time:", time.time()-start, "seconds")
            
#             start2 = time.time()
#             fat_pipes_res = ford_fulkerson(fat_pipes_graph, s, t, fat_pipes)
#             time_each_fat.append(time.time()-start2)
#     #         print("fat pipes max flow:\t", fat_pipes_res[0], "\trunning time:", time.time()-start, "seconds")
#     #         print()
        start = time.time()
        short_pipes_res = ford_fulkerson(short_pipes_graph, s, t, short_pipes)
        time_each_short.append(time.time()-start)
        print("size:", n)
        print("short pipes max flow:\t", short_pipes_res[0], "\trunning time:", time.time()-start, "seconds")
#        print(short_pipes_res[2])

        start2 = time.time()
        fat_pipes_res = ford_fulkerson(fat_pipes_graph, s, t, fat_pipes)
        time_each_fat.append(time.time()-start2)
        print("fat pipes max flow:\t", fat_pipes_res[0], "\trunning time:", time.time()-start, "seconds")
#        print(fat_pipes_res[2])
        print()
        avg_time_short.append(statistics.mean(time_each_short))
        avg_time_fat.append(statistics.mean(time_each_fat))

    plot_time("The average running times from 100 iterations.", avg_time_short, avg_time_fat)
    print("avg_time_short:")
    print(avg_time_short)
    print("avg_time_fat:")
    print(avg_time_fat)
    
def test(s, t, edges):
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    short_pipes_graph = G.copy()
    short_pipes_res = ford_fulkerson(short_pipes_graph, s, t, short_pipes)
    print("input:\t", s, ",", t, ",", edges)
    print("short pipes result:\t(", short_pipes_res[0], ",", short_pipes_res[1], ")")
    fat_pipes_graph = G
    fat_pipes_res = ford_fulkerson(fat_pipes_graph, s, t, fat_pipes)
    print("fat pipes result:\t(", fat_pipes_res[0], ",", fat_pipes_res[1], ")")
    
    
test(0,3,[(0, 1, 1), (0, 2, 5), (1, 2, 1), (2, 3, 2), (1, 3, 6)])
print()
test(0,4,[(0, 1, 2), (0, 3, 6), (1, 2, 3), (1, 3, 8), (1, 4, 5), (2, 4, 7), (3, 4, 9)])
print()
flow()
