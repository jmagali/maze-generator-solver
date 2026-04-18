from generator import generate_maze
from render import draw_maze

grid, width, height = generate_maze()

draw_maze(grid, width, height)
                
