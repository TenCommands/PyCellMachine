from level import api
import os

class Cell(api.Cell):
    id="ten.default.slider"
    def __init__(self, pos, dir):
        super().__init__(
            "ten.default.slider",
            pos,
            dir,
            flags=["can_rotate"],
            priority=1,
            texture=api.load_image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "slider.png")).convert_alpha()
        )
    
    def tick(self):
        pass
    
    def on(self, event):
        if event.type == "cell_collide":
            if abs(event.cell.dir[0]) == abs(self.dir[0]) or abs(event.cell.dir[1]) == abs(self.dir[1]):
                self.move(event.cell.dir)
                #move the event.cell in the opposite direction of event.cell.dir which is a tuple (0,1) up, (1,0) right, (0,-1) down, (-1,0) left
                event.cell.move((-event.cell.dir[0], -event.cell.dir[1]))