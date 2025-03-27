from level import api

class Cell(api.Cell):
    id="ten.default.push"
    def __init__(self, pos, dir):
        super().__init__(
            pos,
            dir,
            flags=["can_rotate"],
            texture=api.load_image(__file__, "push.png").convert_alpha()
        )