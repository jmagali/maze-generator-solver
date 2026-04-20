class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {
            "top": True,
            "left": True,
            "right": True,
            "bottom": True,
        }
        self.visited = False
    
    def reset_walls(self):
        self.walls = {
            "top": True,
            "bottom": True,
            "left": True,
            "right": True
        }