from generator import generate_maze
from render import draw_maze, animate_solution
from solver import solve

grid, width, height = generate_maze()

for x in range(width):
    for y in range(height):
        cell = grid[x][y]
        
while True:
    mode = input("Enter 1/2 for Draw Mode or Solve Mode: ")
    
    if mode == "1" or mode == "2":
        break

if mode == "1":
    draw_maze(grid, width, height)
else:
    path = solve(grid, width, height)
    animate_solution(grid, width, height, path)
                
