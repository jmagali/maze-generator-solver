from collections import deque
from generator import find_neighbors
import random
import heapq

# Find the shortest path by combining actual cost (distance traveled from start)
# and a heuristic estimate (the predicted distance remaining to the goal)
# Faster than BFS as it prioritizes 'promising' paths
def solve_a_star(grid, width, height):
    start = grid[0][0]
    end = grid[-1][-1]
    
    counter = 0 # Tiebreaker for heap ordering
    frontier = [(0, counter, start, [start])] # Frontier is a min-heap priority queue, as A* explores lowest prioriy first
                                     # (priority, cell, path); priority is the actual cost + heuristic estimate
    total_cost = {start: 0} # Maps the cost from the start to any cell (cost = # of moves)
    steps = []
    steps.append(("explore", start.x, start.y)) 
    
    # Manhattan distance (An estimate of the number of moves to the end)
    # This heuristic is needed to predict the total cost of a path to the end
    def heuristic(current, end):
        return abs(current.x - end.x) + abs(current.y - end.y)
    
    while frontier:
        # Retrieves the most promising cell from the frontier
        current_cost, _, current, path = heapq.heappop(frontier)
        
        if current == end:
            final_path = [(c.x, c.y) for c in path]
            return {"path": final_path, "steps": steps}
        
        neighbors = find_neighbors(current, grid, width, height)
        
        for neighbor in neighbors:
            dx = current.x - neighbor.x
            dy = current.y - neighbor.y
            
            # Wall checks; Cannot continue moving in a direction if there is a wall
            if dx == -1 and current.walls["right"]:
                continue
            if dx == 1 and current.walls["left"]:
                continue
            if dy == -1 and current.walls["bottom"]:
                continue
            if dy == 1 and current.walls["top"]:
                continue
            
            # Since cost = # moves, moving to a neighbor is +1 cost
            new_cost = total_cost[current] + 1
            
            # Only proceed if this cell is unvisited or a cheaper path to the end
            if neighbor not in total_cost or new_cost < total_cost[neighbor]:
                total_cost[neighbor] = new_cost
                
                # Calculates cost of the path
                priority = new_cost + heuristic(neighbor, end)
                
                # The min-heap will sort the neighbor by priority automatically
                heapq.heappush(frontier, (priority, counter, neighbor, path + [neighbor]))
                counter += 1
                steps.append(("explore", neighbor.x, neighbor.y))
                
    return {"path": None, "steps": steps}

def solve_dfs(grid, width, height):    
    # Reset visited
    for x in range(width):
        for y in range(height):
            grid[x][y].visited = False
            
    # Entrance at top-left; exit at bottom-right
    start = grid[0][0]
    start.visited = True
    end = grid[width - 1][height - 1]
    
    stack = [(start, [start])]
    steps = []  # Track all exploration steps
    steps.append(("explore", start.x, start.y))  # Add the starting cell to ensure it is included
    
    while stack:
        current, path = stack[-1]
        
        if current == end:
            # Create the final path
            final_path = [(c.x, c.y) for c in path]
            return {"path": final_path, "steps": steps} # Steps contains exploratory and backtracking steps
        
        # Get neighbording unvisited cells
        neighbors = find_neighbors(current, grid, width, height)
        unvisited = [n for n in neighbors if not n.visited]
        
        # Randomize the order of unvisited neighbors for true DFS behavior
        random.shuffle(unvisited)
        for neighbor in unvisited:
            dx = current.x - neighbor.x
            dy = current.y - neighbor.y
            
            # Wall checks; Cannot continue moving in a direction if there is a wall
            if dx == -1 and current.walls["right"]:
                continue
            if dx == 1 and current.walls["left"]:
                continue
            if dy == -1 and current.walls["bottom"]:
                continue
            if dy == 1 and current.walls["top"]:
                continue
            
            # Add to the stack
            neighbor.visited = True
            stack.append((neighbor, path + [neighbor]))
            steps.append(("explore", neighbor.x, neighbor.y))
            
            # If the cell is valid, exit the search
            break
        # If not movement can be made, remove the neighbor from the stack
        else:
            if stack:
                backtrack_cell = stack[-1][0]
                steps.append(("backtrack", backtrack_cell.x, backtrack_cell.y))
            stack.pop()
    
    # If there is no valid solution
    return {"path": None, "steps": steps}  

def solve_bfs(grid, width, height):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Reset visited
    for x in range(width):
        for y in range(height):
            grid[x][y].visited = False

    # Entrance at top-left; exit at bottom-right
    start = grid[0][0]
    end = grid[width - 1][height - 1]

    q = deque()
    q.append((start, [start]))
    start.visited = True
    
    steps = []  # Track all exploration steps
    steps.append(("explore", start.x, start.y))  # Add the starting cell

    # Continues until there are no more unvisited nodes within the queue
    while q:
        # Removes and returns the first item (FIFO)
        node, path = q.popleft()

        # If the current node is the exit, return the path taken to get there for rendering
        # Use (x,y) and not cell object for ease of access
        if node == end:
            final_path = [(c.x, c.y) for c in path]
            return {"path": final_path, "steps": steps}

        # Checks neighbors in all 4 cardinal directions
        for dx, dy in directions:
            # Compute the neighboring cell by adding direction offsets
            nx, ny = node.x + dx, node.y + dy

            # Ensures the neighbor is within grid bounds
            if not (0 <= nx < width and 0 <= ny < height):
                continue

            neighbor = grid[nx][ny]

            # Wall checks; Cannot continue moving in a direction if there is a wall
            if dx == 1 and node.walls["right"]:
                continue
            if dx == -1 and node.walls["left"]:
                continue
            if dy == 1 and node.walls["bottom"]:
                continue
            if dy == -1 and node.walls["top"]:
                continue

            # Avoid cycles and redundency by skipping visited neighbors
            if neighbor.visited:
                continue

            # Mark before enqueing and updates path
            neighbor.visited = True
            q.append((neighbor, path + [neighbor]))
            steps.append(("explore", neighbor.x, neighbor.y))

    # If there is no valid solution
    return {"path": None, "steps": steps}