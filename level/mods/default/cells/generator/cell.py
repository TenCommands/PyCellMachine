from level import api

class Cell(api.Cell):
    id="ten.default.generator"
    def __init__(self, pos, dir):
        super().__init__(
            pos,
            dir,
            priority=1,
            # set texture to the local mover.png file
            texture=api.load_image(__file__, "generator.png").convert_alpha()
        )
    
    def tick(self):
        # Get positions behind and in front of the generator using vec2 operations
        behind = self.pos + self.dir
        front = self.pos - self.dir

        # Check if there's a cell behind to duplicate
        cell = self.grid.get_cell(behind)
        if cell is None: 
            return  # Nothing to duplicate

        # Check if there's a cell in front
        front_cell = self.grid.get_cell(front)
        if front_cell is not None:
            # Try to push the cell in front
            push_success = front_cell.move(front - self.pos)
            if not push_success:
                return  # Can't push the cell, so don't duplicate

        # At this point, either there was no cell in front or we successfully pushed it
        # Create a duplicate of the cell behind
        cell_class = cell.__class__
        new_cell = cell_class(front, cell.dir)  # Use front position directly

        # Copy any other important attributes from the original cell
        for attr in dir(cell):
            if not attr.startswith('__') and attr not in ['pos', 'dir', 'grid']:
                if hasattr(cell, attr) and not callable(getattr(cell, attr)):
                    setattr(new_cell, attr, getattr(cell, attr))

        # Add the new cell to the grid
        self.grid.add_cell(new_cell)
        print(new_cell.id)