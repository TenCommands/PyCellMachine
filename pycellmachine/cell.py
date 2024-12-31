
class Cell:
    def __init__(self, x, y, rotation=0):
        self.x = x
        self.y = y
        self.rotation = rotation

    def get_neighbors(self, type=4):
        if type == 4:
            """Returns the 4 neighboring positions (N, E, S, W)"""
            neighbors = [
                (self.x, self.y - 1),  # North
                (self.x + 1, self.y),  # East
                (self.x, self.y + 1),  # South
                (self.x - 1, self.y)   # West
            ]
        elif type == 8:
            """Returns the 8 neighboring positions (N, NE, E, SE, S, SW, W, NW)"""
            neighbors = [
            (self.x, self.y - 1),     # North
            (self.x + 1, self.y - 1), # Northeast
            (self.x + 1, self.y),     # East
            (self.x + 1, self.y + 1), # Southeast
            (self.x, self.y + 1),     # South
            (self.x - 1, self.y + 1), # Southwest
            (self.x - 1, self.y),     # West
            (self.x - 1, self.y - 1)  # Northwest
        ]
        else:
            raise ValueError("Invalid type. Use 4 or 8.")
        return neighbors
    
    def rotate(self, direction):
        """Rotate the cell by the specified direction."""
        if direction == 1:
            self.rotation = (self.rotation + 1) % 4
        elif direction == -1:
            self.rotation = (self.rotation - 1) % 4
        else:
            raise ValueError("Invalid direction. Use -1 or 1.")
    
    def move(self, direction):
        """Move the cell in the specified direction."""
        if direction == 0:
            self.y -= 1
        elif direction == 1:
            self.x += 1
        elif direction == 2:
            self.y += 1
        elif direction == 3:
            self.x -= 1
        else:
            raise ValueError("Invalid direction. Use 0, 1, 2, or 3.")