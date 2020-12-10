import time

def b_queens(n):
    def backtrack(row, count, node_visit):
        for col in range(n):
            available = not (cols[col] + r_diagonals[row - col] + l_diagonals[row + col])
            if available: #if there is no conflict with the previous row
                # add queens to the position
                queens.add((row, col))
                node_visit += 1
                # set deserved position for future
                cols[col] = 1
                r_diagonals[row - col] = 1
                l_diagonals[row + col] = 1
                
                if row + 1 == n: #last row means we finish and get a solution
                    count += 1
                else: # continue furture row
                    count, node_visit = backtrack(row + 1, count, node_visit)
                
                # start backtrack and clear values
                queens.remove((row, col))
                cols[col] = 0
                r_diagonals[row - col] = 0
                l_diagonals[row + col] = 0
                
        return count, node_visit

    cols = [0] * n
    r_diagonals = [0] * (2 * n - 1)
    l_diagonals = [0] * (2 * n - 1)
    queens = set()
    res = []
    count, node_visit = backtrack(0, 0, 0)
    return count, node_visit

# b_queens(12)

def e_queens(n):
    def validate(row, col):
        while row >= 0:
            for r,c in queens:
                if r == row:
                    col = c
            for r in range(row-1, -1, -1):
                if (r, col) in queens:
                    return False
            for c_l in range(col-1, -1, -1):
                if (row, c_l) in queens:
                    return False
            for c_r in range(col+1, n):
                if (row, c_r) in queens:
                    return False
            dc_l = col
            dc_r = col
            dr = row
            while dr > 0:
                dc_l -= 1
                dc_r += 1
                dr -= 1
                if (dr, dc_l) in queens or (dr, dc_r) in queens:
                    return False
            row -= 1
        return True
    
    def bruteforce(row, count, node_visit):
        for col in range(n):
            queens.add((row, col))
            node_visit += 1
            if row + 1 == n: #last row means we finish so we need to do the validation
                if validate(row, col):
                    count += 1
            else: # continue furture row
                count, node_visit = bruteforce(row + 1, count, node_visit)
            queens.remove((row, col))
        return count, node_visit
            
    queens = set()
    res = []
    count, node_visit = bruteforce(0, 0, 0)
    return count, node_visit

for i in range(4,9):
    print("n:", i)
    start = time.time()
    b_sol, b_visit = b_queens(i)
    runtime = time.time() - start
    print("Backtracking solutions:", b_sol, "\tBacktracking number of nodes visited:", b_visit, "\trun time:", runtime )
    
    start = time.time()
    e_sol, e_visit = e_queens(i)
    runtime = time.time() - start
    print("Exhaustive solutions:", e_sol, "\tExhaustive number of nodes visited:", e_visit, "\trun time:", runtime  )
    
