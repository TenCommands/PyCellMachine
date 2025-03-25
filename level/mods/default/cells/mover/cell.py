from level import api
import os

class Cell(api.Cell):
    id="ten.default.mover"
    def __init__(self, pos, dir):
        super().__init__(
            "ten.default.mover",
            pos,
            dir,
            priority=1,
            # set texture to the local mover.png file
            texture=api.load_image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mover.png")).convert_alpha()
        )
    
    def tick(self):
        self.move(self.dir)