
class Grid:
    def __init__(self, width=100, height=100, scale=1, offset_x=0, offset_y=0):
        self.width = width
        self.height = height
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.cells = {}  # Dictionary to store active cells

    def add_cell(self, cell):
        """Add a cell to the grid at specified coordinates"""
        self.cells[(cell.x, cell.y)] = cell

    def remove_cell(self, x, y):
        """Remove a cell from the grid at specified coordinates"""
        if (x, y) in self.cells:
            del self.cells[(x, y)]

    def get_cell(self, x, y):
        """Get a cell at specified coordinates"""
        return self.cells.get((x, y))

    def move(self, dx, dy):
        """Move the entire grid by changing the offset"""
        self.offset_x += dx
        self.offset_y += dy

    def scale_grid(self, factor):
        """Scale the grid by a factor"""
        if factor > 0:
            self.scale *= factor
        else:
            raise ValueError("Scale factor must be positive")

    def get_screen_coordinates(self, x, y):
        """Convert grid coordinates to screen coordinates"""
        screen_x = (x + self.offset_x) * self.scale
        screen_y = (y + self.offset_y) * self.scale
        return screen_x, screen_y

    def get_grid_coordinates(self, screen_x, screen_y):
        """Convert screen coordinates to grid coordinates"""
        grid_x = (screen_x / self.scale) - self.offset_x
        grid_y = (screen_y / self.scale) - self.offset_y
        return int(grid_x), int(grid_y)

    def is_within_bounds(self, x, y):
        """Check if coordinates are within grid bounds"""
        return 0 <= x < self.width and 0 <= y < self.height
