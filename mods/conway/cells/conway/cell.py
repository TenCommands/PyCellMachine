import pycellmachine as pcm

class ConwayCell(pcm.Cell):
    def __init__(self, x, y, rotation=0):
        super().__init__(x, y, rotation)
        self.alive = False

    def update(self, grid):
        neighbors = self.get_neighbors(8)
        alive_neighbors = sum(1 for pos in neighbors if pos in grid and isinstance(grid[pos], ConwayCell) and grid[pos].alive)
        
        if self.alive:
            # Cell dies if it has fewer than 2 or more than 3 live neighbors
            if alive_neighbors < 2 or alive_neighbors > 3:
                self.alive = False
                self.rotation = 1
            else:
                self.rotation = 0
        else:
            # Dead cell becomes alive if it has exactly 3 live neighbors
            if alive_neighbors == 3:
                self.alive = True
                self.rotation = 0
            else:
                self.rotation = 1
