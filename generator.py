from cell import Cell
import random

def generate_maze():
    height = int(input("Enter the height: "))
    width = int(input("Enter the width: "))
    
    grid = create_grid(width, height)
    start = grid[0][0]
    recursive_backtrack(start, grid, [])
    print_maze(grid, width, height)
    
def print_maze(grid, width, height):
    start = (0, 0)
    end = (width - 1, height - 1)

    for y in range(height):
        top = ""
        middle = ""

        for x in range(width):
            cell = grid[x][y]

            top += "+---" if cell.walls["top"] else "+   "

            # Entry + exit handling
            if (x, y) == start:
                middle += "    "   # open entrance
            elif (x, y) == end:
                middle += "   "    # open exit
            else:
                middle += "|   " if cell.walls["left"] else "    "

        top += "+"

        # Right border handling for exit row
        if y == height - 1:
            middle += " "  # open right edge visually
        else:
            middle += "|"

        print(top)
        print(middle)

    print("+---" * width + "+")
    
    
def recursive_backtrack(cell, grid, result):
    cell.visited = True
    result.append(cell)
    
    neighbors = find_neighbords(cell, grid, len(grid), len(grid[0]))
    random.shuffle(neighbors)
    
    for neighbor in neighbors:
        if not neighbor.visited:
            remove_walls(cell, neighbor)
            recursive_backtrack(neighbor, grid, result)

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

    elif dy == 1:  # neighbor is ABOVE current
        current.walls["top"] = False
        neighbor.walls["bottom"] = False

    elif dy == -1:  # neighbor is BELOW current
        current.walls["bottom"] = False
        neighbor.walls["top"] = False
        

def create_grid(width, height):
    grid = []
    
    for x in range(width):
        row = []
        for y in range(height):
            row.append(Cell(x,y))
        grid.append(row)
        
    return grid
    
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

if __name__ == "__main__":
    generate_maze()
