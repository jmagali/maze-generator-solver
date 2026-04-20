from cell import Cell
import random

def generate_maze_binary_tree(width, height):
    grid = create_grid(width, height)
    steps = []
    
    for y in range(height):
        for x in range(width):
            right = x + 1
            down = y + 1
            
            options = []
            
            if right < width:
                options.append("r")
            if down < height:
                options.append("d")
            
            if options:
                option = random.choice(options)
            
                if option == "r":
                    grid[x][y].walls["right"] = False
                    grid[right][y].walls["left"] = False
                    steps.append((grid[x][y], grid[right][y]))
                elif option == 'd':
                    grid[x][y].walls["bottom"] = False
                    grid[x][down].walls["top"] = False
                    steps.append((grid[x][y], grid[x][down]))
                
    return grid, width, height, steps

def generate_maze_prims(width, height):
    grid = create_grid(width, height)
    steps = []
    
    start = grid[random.randint(0, width - 1)][random.randint(0, height - 1)]
    start.visited = True
    
    # Let the frontier be all adj cells not visited
    frontier = find_neighbords(start, grid, width, height)
    
    while frontier:
        # Take a cell from the frontier and pair it to an adj visited neighbor
        current = random.choice(frontier)
        neighbors = find_neighbords(current, grid, width, height)
        visited_neighbors = [n for n in neighbors if n.visited]
        neighbor = random.choice(visited_neighbors)

        # Connect the cell to the visited cells and remove it from the frontier
        remove_walls(current, neighbor)
        steps.append((current, neighbor))
        frontier.remove(current)
        current.visited = True
        
        # Expand the frontier from the new cell
        frontier += [n for n in neighbors if not n.visited and not n in frontier]
        
    return grid, width, height, steps

def generate_maze_dfs(width, height):
    grid = create_grid(width, height)
    steps = []

    start = grid[0][0]
    stack = [start]

    while stack:
        current = stack[-1]
        current.visited = True

        neighbors = find_neighbords(current, grid, width, height)
        unvisited = [n for n in neighbors if not n.visited]

        if unvisited:
            neighbor = random.choice(unvisited)

            remove_walls(current, neighbor)
            steps.append((current, neighbor))
            
            neighbor.visited = True
            stack.append(neighbor)
        else:
            stack.pop()
    
    return grid, width, height, steps

# You need the current and neighbor bc you need to remove the walls on both cells
def remove_walls(current, neighbor):
    dx = current.x - neighbor.x
    dy = current.y - neighbor.y
    
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
