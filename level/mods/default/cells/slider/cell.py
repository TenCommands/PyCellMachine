from level import api

class Cell(api.Cell):
    id="ten.default.slider"
    def __init__(self, pos, dir):
        super().__init__(
            pos,
            dir,
            flags=["can_rotate"],
            texture=api.load_image(__file__, "slider.png").convert_alpha()
        )
    
    def on(self, event):
        if event.type == "cell_collide":
            if abs(event.dir[0]) == abs(self.dir[0]) or abs(event.dir[1]) == abs(self.dir[1]):
                self.move(event.dir)
                # Move event.cell in the opposite direction it came from effectively reversing the effects the move that triggered this collision
                event.cell.move(-event.dir)