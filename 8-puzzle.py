from collections import deque
import time

def move(state, action):
    no_of_elements = len(state)
    board_size = int(no_of_elements**0.5)
    
    new_state = state.copy()
    
    vacant_index = new_state.index(0)
    
    if action == "D":
        if vacant_index not in range(0, board_size): #top of the board
            new_state[vacant_index], new_state[vacant_index-board_size] = new_state[vacant_index-board_size], new_state[vacant_index]
            return new_state
    elif action == "L":
        if vacant_index not in range(board_size-1, no_of_elements, board_size):
            new_state[vacant_index], new_state[vacant_index+1] = new_state[vacant_index+1], new_state[vacant_index]
            return new_state
    elif action == "U":
        if vacant_index not in range(no_of_elements-board_size, no_of_elements):
            new_state[vacant_index], new_state[vacant_index+board_size] = new_state[vacant_index+board_size], new_state[vacant_index]
            return new_state
    elif action == "R":
        if vacant_index not in range(0, no_of_elements, board_size):
            new_state[vacant_index], new_state[vacant_index-1] = new_state[vacant_index-1], new_state[vacant_index]
            return new_state
        
    return None
    
def create_neighbors(node):
    neighbors = []
    
    #down
    d_state = move(node[0], "D")
    if d_state:
        neighbors.append([d_state, node[1]+1, node[2] + ", D" if node[2] else "D"])
    #right
    r_state = move(node[0], "R")
    if r_state:
        neighbors.append([r_state, node[1]+1, node[2] + ", R" if node[2] else "R"])
    #up
    u_state = move(node[0], "U")
    if u_state:
        neighbors.append([u_state, node[1]+1, node[2] + ", U" if node[2] else "U"])
    #left
    l_state = move(node[0], "L")
    if l_state:
        neighbors.append([l_state, node[1]+1, node[2] + ", L" if node[2] else "L"])
    
    return neighbors
    
    
def puzzle(initial_state):
    initial_state = initial_state[0]+initial_state[1]+initial_state[2]
    visited_states = set()
    queue = deque([(initial_state, 0, "")])
    level = 0
    node_count = 0
    cumulative_node_count = 0
    while queue:
        node = queue.popleft()
        if level == node[1]:
            node_count += 1
        else:
            print("level:", level, ", \tnode_count:", node_count, "\t" if node_count < 100 else "" ,"\tcumulative_node_count:", cumulative_node_count)
            level += 1
            node_count = 1
        cumulative_node_count += 1
        state_id = "".join([str(n) for n in node[0]])
        visited_states.add(state_id)
        
        #create neighbors
        neighbors = create_neighbors(node)
        
        for neighbor in neighbors:
            neighbor_id = "".join([str(n) for n in neighbor[0]])
            if neighbor_id not in visited_states:
                queue.append(neighbor)
                visited_states.add(neighbor_id)
        
    print("level:", level, ", \tnode_count:", node_count, "\t" if node_count < 100 else "" , "\tcumulative_node_count:", cumulative_node_count)
    print("solved\n")
    
    node[0] = [node[0][:3]]+[node[0][3:6]]+[node[0][6:9]]
    return node
                
initial_state = [[1,2,3],[8,0,4],[7,6,5]] # goal state from requirement

start = time.time()
result_node = puzzle(initial_state)
print("results:\t", result_node[0], "\ndepth:\t\t", result_node[1], "\nsolution:\t", result_node[2])
print("\nrunning time:", time.time()-start, "seconds")
