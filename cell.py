class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # All walls are initially present; true is indicative of a present wall
        self.walls = {
            "top": True,
            "left": True,
            "right": True,
            "bottom": True,
        }
        
        # Marks whether a pathfinding algorithm in generation or solving has explored the cell
        # to prevent cycles and redundancy
        self.visited = False
    
    # Restores all walls to their default states
    def reset_walls(self):
        self.walls = {
            "top": True,
            "bottom": True,
            "left": True,
            "right": True
        }