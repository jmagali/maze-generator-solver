from generator import generate_maze
from render import draw_maze

grid, width, height = generate_maze()

for x in range(width):
    for y in range(height):
        cell = grid[x][y]
        print(f"({cell.x}, {cell.y}), {cell.walls}")

draw_maze(grid, width, height)
                
