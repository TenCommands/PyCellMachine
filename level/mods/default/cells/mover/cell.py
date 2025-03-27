from level import api

class Cell(api.Cell):
    id="ten.default.mover"
    def __init__(self, pos, dir):
        super().__init__(
            pos,
            dir,
            priority=2,
            # set texture to the local mover.png file
            texture=api.load_image(__file__, "mover.png").convert_alpha()
        )
    
    def tick(self):
        self.move(self.dir)