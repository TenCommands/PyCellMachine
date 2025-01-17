import pycellmachine as pcm

class Mover(pcm.Cell):
    def __init__(self, pos, dir):
        super().__init__(
            "mover",
            pos,
            dir,
            flags=["can_rotate"],
            priority=1
        )
    
    def tick(self):
        self.x += self.dir[0]
        self.y += self.dir[1]
    
    def render(self, grid):
        self.image = grid.cell_size_x_half_half_half
        self.rect = self.image.get_rect(center=(self.x, self.y))