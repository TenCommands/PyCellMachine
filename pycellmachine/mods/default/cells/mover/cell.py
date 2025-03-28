from pycellmachine import api

class Mover(api.Cell):
    def __init__(self, pos, dir):
        super().__init__(
            "ten.default.mover",
            pos,
            dir,
            priority=1
        )
    
    def tick(self):
        self.x += self.dir[0]
        self.y += self.dir[1]

    def render(self, screen):
        screen.blit(api.tx.get_texture("mover"), (self.x, self.y))