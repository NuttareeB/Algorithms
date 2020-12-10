import time
import random
import string
import statistics
import matplotlib.pyplot as plt

def editDistance(x, y):
    d = [[0]*(len(y)+1) for i in range(len(x)+1)]
    for i in range(len(x)):
        d[i][0]=i
    for j in range(len(y)):
        d[0][j]=j
    for i in range(len(x)):
        for j in range(len(y)):
            if x[i]==y[j]:
                d[i+1][j+1] = min(d[i][j+1]+1, d[i+1][j]+1, d[i][j])
            else:
                d[i+1][j+1] = min(d[i][j+1]+1, d[i+1][j]+1, d[i][j]+1)
    return d[len(x)][len(y)]

def plot_time(avg_time):
    plt.title("Time taken for each length of strings")
    plt.xlabel("length of strings")
    plt.ylabel("Time (Seconds)")
    plt.plot(avg_time)
#     plt.legend(["Kruskel's", "Prim's"], loc ="lower right")
    plt.xticks(range(10), ['100', '200', '300', '400', '500', '600', '700', '800', '900', '1000'])
    plt.show()
    
print("Edit distance of \"BABBLE\", \"APPLE\" is:",  editDistance("BABBLE", "APPLE"))
print()
print("Edit distance of \"ATCAT\", \"ATTATC\" is:",  editDistance("ATCAT", "ATTATC"))
print()
print("Edit distance of \"taacttctagtacatacccgggttgagcccccatttcttggttggatgcgaggaacattacgctagaggaacaacaaggtcagaggcctgttactcctat\", \"taacttctagtacatacccgggttgagcccccatttccgaggaacattacgctagaggaacaacaaggtcagaggcctgttactcctat\" is:",  editDistance("taacttctagtacatacccgggttgagcccccatttcttggttggatgcgaggaacattacgctagaggaacaacaaggtcagaggcctgttactcctat", "taacttctagtacatacccgggttgagcccccatttccgaggaacattacgctagaggaacaacaaggtcagaggcctgttactcctat"))
print()
print("Edit distance of \"CGCAATTCTGAAGCGCTGGGGAAGACGGGT\", \"TATCCCATCGAACGCCTATTCTAGGAT\" is:",  editDistance("CGCAATTCTGAAGCGCTGGGGAAGACGGGT", "TATCCCATCGAACGCCTATTCTAGGAT"))
print()
print("Edit distance of \"tatttacccaccacttctcccgttctcgaatcaggaatagactactgcaatcgacgtagggataggaaactccccgagtttccacagaccgcgcgcgatattgctcgccggcatacagcccttgcgggaaatcggcaaccagttgagtagttcattggcttaagacgctttaagtacttaggatggtcgcgtcgtgccaa\", \"atggtctccccgcaagataccctaattccttcactctctcacctagagcaccttaacgtgaaagatggctttaggatggcatagctatgccgtggtgctatgagatcaaacaccgctttctttttagaacgggtcctaatacgacgtgccgtgcacagcattgtaataacactggacgacgcgggctcggttagtaagtt\" is:",  editDistance("tatttacccaccacttctcccgttctcgaatcaggaatagactactgcaatcgacgtagggataggaaactccccgagtttccacagaccgcgcgcgatattgctcgccggcatacagcccttgcgggaaatcggcaaccagttgagtagttcattggcttaagacgctttaagtacttaggatggtcgcgtcgtgccaa", "atggtctccccgcaagataccctaattccttcactctctcacctagagcaccttaacgtgaaagatggctttaggatggcatagctatgccgtggtgctatgagatcaaacaccgctttctttttagaacgggtcctaatacgacgtgccgtgcacagcattgtaataacactggacgacgcgggctcggttagtaagtt"))

# avg_times = []
# times = []
# for n in range(100, 1001, 100):
#     for i in range(100):
#         random_x = ''.join(random.choice(string.ascii_letters) for i in range(n))
#         random_y = ''.join(random.choice(string.ascii_letters) for i in range(n))
#         start = time.time();
#         edit_distance = editDistance(random_x, random_y)
#         times.append(time.time()-start)
#     avg_times.append(statistics.mean(times))
#     times = []
    
# plot_time(avg_times)
