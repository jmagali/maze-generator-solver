import matplotlib.pyplot as plt

def draw_maze(grid, width, height):
    fig, ax = plt.subplots()
    
    for x in range(width):
        for y in range(height):
            cell = grid[x][y]
            
            # If there is a wall in any direction, draw it
            if cell.walls["top"]:
                ax.plot([x, x+1], [y+1, y+1], "k")
            if cell.walls["bottom"]:
                ax.plot([x, x+1], [y, y], "k")
            if cell.walls["left"]:
                ax.plot([x, x], [y, y+1], "k")
            if cell.walls["right"]:
                ax.plot([x+1, x+1], [y, y+1], "k")
                
    ax.plot([0, 0], [0, 1], color="green", linewidth=3)
    ax.plot([width, width], [height-1, height], color="red", linewidth=3)
    
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.axis("off")
    
    plt.show()