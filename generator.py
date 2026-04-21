from cell import Cell
import random

# Simplest and worst maze generation
def generate_maze_binary_tree(width, height):
    grid = create_grid(width, height)
    steps = []
    
    # Loops through each cell in the maze grid
    for y in range(height):
        for x in range(width):
            # Calculate the neigboring coordinates
            right = x + 1
            down = y + 1
            
            # Valid directions
            options = []
            
            # Ensures the bounding walls are not removed
            if right < width:
                options.append("r")
            if down < height:
                options.append("d")
            
            # Randomly select a direction if carving is possible
            if options:
                option = random.choice(options)
            
                # Remove the corresponding wall from both neighboring cells
                if option == "r":
                    grid[x][y].walls["right"] = False
                    grid[right][y].walls["left"] = False
                    
                    # Track carving for animation
                    steps.append((grid[x][y], grid[right][y]))
                elif option == 'd':
                    grid[x][y].walls["bottom"] = False
                    grid[x][down].walls["top"] = False
                    steps.append((grid[x][y], grid[x][down]))
                
    return grid, width, height, steps

# Unfirorm maze with better distribution and less directional bias
# Grows from a random start point
def generate_maze_prims(width, height):
    grid = create_grid(width, height)
    steps = []
    
    # Selects a random cell within the maze as the start
    start = grid[random.randint(0, width - 1)][random.randint(0, height - 1)]
    start.visited = True
    
    # Let the frontier be all adjacent cells not visited
    # Prim's expans from known cells to unknown cells
    frontier = find_neighbords(start, grid, width, height)
    
    while frontier:
        # Take a cell from the frontier and pair it to an adjacent visited neighbor
        current = random.choice(frontier)
        neighbors = find_neighbords(current, grid, width, height)
        visited_neighbors = [n for n in neighbors if n.visited]
        neighbor = random.choice(visited_neighbors)

        # Connect the cell to the visited cells
        remove_walls(current, neighbor)
        steps.append((current, neighbor))
        
        # Remove current from the frontier as it is visited are part of the maze
        frontier.remove(current)
        current.visited = True
        
        # Expand the frontier from the new cell
        # TODO: Possible inefficiency; O(n) operation, maybe use set?
        frontier += [n for n in neighbors if not n.visited and not n in frontier]
        
    return grid, width, height, steps

# Explores deep into the maze before backtracking
# A more traditional maze with longer corridors
def generate_maze_dfs(width, height):
    grid = create_grid(width, height)
    steps = []
    
    start = grid[0][0]
    stack = [start]

    while stack:
        # Use the cell at the top of the stack
        current = stack[-1]
        current.visited = True

        # Get neighbording unvisited cells
        neighbors = find_neighbords(current, grid, width, height)
        unvisited = [n for n in neighbors if not n.visited]

        # If you can keep brancing from the current, do so
        if unvisited:
            # Retrive a random unvisited neighbor
            neighbor = random.choice(unvisited)

            # Carve the walls, adding it to the maze and the stack for future brancing
            remove_walls(current, neighbor)
            steps.append((current, neighbor))
            neighbor.visited = True
            stack.append(neighbor)
        # If you cannot branch from the current, backtrack to the next cell in the stack
        else:
            stack.pop()
    
    return grid, width, height, steps

# You need the current and neighbor bc you need to remove the walls on both cells
def remove_walls(current, neighbor):
    # Determines the direction of horizontal and vertical position of neighbor from current
    dx = current.x - neighbor.x
    dy = current.y - neighbor.y
    
    # Since walls are properties of cells and not edges, both must be updated
    if dx == 1:  # neighbor is LEFT of current
        current.walls["left"] = False
        neighbor.walls["right"] = False
    elif dx == -1:  # neighbor is RIGHT of current
        current.walls["right"] = False
        neighbor.walls["left"] = False

    if dy == 1:  # neighbor is ABOVE current
        current.walls["top"] = False
        neighbor.walls["bottom"] = False
    elif dy == -1:  # neighbor is BELOW current
        current.walls["bottom"] = False
        neighbor.walls["top"] = False

def create_grid(width, height):
    return [[Cell(x, y) for y in range(height)] for x in range(width)]
    
def find_neighbords(cell, grid, width, height):
    dirs = [(1,0), (0,1), (-1,0), (0,-1)]

    neighbors = []
    
    for dx, dy in dirs:
        # Determine the neighbors in each direaction
        nx, ny = cell.x + dx, cell.y + dy
        
        # Ensure that the neighbor is within the grid bounds
        if 0 <= nx < width and 0 <= ny < height:
            neighbors.append(grid[nx][ny])
            
    return neighbors
