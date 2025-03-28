import pygame, json, numpy as math, base64, os, sys

settings = json.load(open(r'./pycellmachine/_internal/settings.json'))

#pygame.init()

def import_mods():
    _imports = {}
    for mod in os.listdir('./level/mods'):
        for cell in os.listdir(os.path.join('./level/mods', mod, 'cells')):
            for file in os.listdir(os.path.join('./level/mods', mod, 'cells', cell)):
                if file.endswith('.py') and file != '__init__.py':
                    module_name = file[:-3]
                    module_path = f'level.mods.{mod}.cells.{cell}.{module_name}'
                    try:
                        exec(f'from {module_path} import Cell')
                        cell_class = eval(f'sys.modules["{module_path}"].Cell')
                        _imports[cell_class.id] = cell_class
                    except ImportError as e:
                        print(f'Failed to import {module_name} from {mod}.{cell}: {e}')
    return _imports

__all_cells__ = import_mods()

def load_image(file, path):
    return pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(file)), path))

class vec(tuple):
    """A N-Dimensional vector"""
    def __new__(cls, *args):
        return tuple.__new__(cls, args)
    def __add__(self, other):
        return vec(*[self[i] + other[i] for i in range(len(self))])
    def __sub__(self, other):
        return vec(*[self[i] - other[i] for i in range(len(self))])
    def __mul__(self, other):
        return vec(*[self[i] * other[i] for i in range(len(self))])
    def __truediv__(self, other):
        return vec(*[self[i] / other[i] for i in range(len(self))])
    def __floordiv__(self, other):
        return vec(*[self[i] // other[i] for i in range(len(self))])
    def __mod__(self, other):
        return vec(*[self[i] % other[i] for i in range(len(self))])
    def __pow__(self, other):
        return vec(*[self[i] ** other[i] for i in range(len(self))])
    def __neg__(self):
        return vec(*[self[i]*-1 for i in range(len(self))])

class vec2(vec):
    """A 2D vector"""
    def __new__(cls, *args):
        if len(args) == 1 and isinstance(args[0], tuple):
            return vec.__new__(cls, *args[0])
        return vec.__new__(cls, *args)

def vec2_to_deg(vec: vec2) -> float:
    """Converts a 2D vector (x, y) to degrees."""
    angle_rad = math.arctan2(vec[1]*-1, vec[0])
    angle_deg = math.degrees(angle_rad) % 360
    return angle_deg

def deg_to_vec2(deg: float) -> vec2:
    """Converts degrees to a 2D vector (x, y)."""
    rad = math.radians(deg)
    x = math.cos(rad)
    y = math.sin(rad)
    return vec2(x, y)

class event:
    def __init__(self, event_type:str, **kwargs):
        self.type = event_type
        for key, value in kwargs.items():
            setattr(self, key, value)

class Grid:
    _registry = []
    def __init__(self, width: int, height: int, scale: int=1):
        self.width = width
        self.height = height
        self.scale = scale
        self.x = 0
        self.y = 0
        self.cells = []
        
        Grid._registry.append(self)
    
    @classmethod
    def __all_instances__(cls):
        return cls._registry

    def move(self, x: int, y: int):
        pass

    def events(self, event):
        pass

    def draw(self, screen):
        
        render_properties = {
                'screen': screen,
                'scale': self.scale*16,
                'offset': (self.x, self.y),
                'grid': self
            }

        # Load the background image (only once)
        if not hasattr(self, 'background_image'):
            self.background_image = pygame.image.load(r"D:\GitHub\PyCellMachine\level\_internal\assets\default\assets\level\background.png").convert_alpha()

        # Get screen height for coordinate inversion
        screen_height = screen.get_height()

        # Render the background image for each cell position
        for y in range(self.height):
            for x in range(self.width):
                # Scale the background image to match the cell size
                scaled_bg = pygame.transform.scale(
                    self.background_image, 
                    (int(self.scale*16), int(self.scale*16))
                )

                # Calculate x position (same as before)
                x_pos = self.x + x*(self.scale*16)

                # Calculate y position (inverted to start from bottom)
                # First, calculate the position from the top
                top_y = self.y + y*(self.scale*16)

                # Then invert it to position from the bottom
                # We need to account for the grid's total height
                grid_height_px = self.height * (self.scale*16)
                y_pos = screen_height - top_y - (self.scale*16)

                # Blit the scaled background at the calculated position
                screen.blit(scaled_bg, (x_pos, y_pos))

        # Render all cells
        for cell in self.cells:
            cell.render(render_properties)

    def tick(self):
        try:
            # Add timing control for tick rate
            current_time = pygame.time.get_ticks()

            # Initialize last_tick_time if it doesn't exist
            if not hasattr(self, 'last_tick_time'):
                self.last_tick_time = 0

            # Check if enough time has passed (50ms = 1/20th of a second)
            delay = 1000/0.25
            if current_time - self.last_tick_time >= delay:
                # Update the last tick time
                self.last_tick_time = current_time

                # Process ticks for all cells
                for cell in self.cells:
                    if hasattr(cell, 'tick'):
                        cell.tick()
        except Exception as e:
            print(f"Error {e}")
    
    def add_cell(self, cell):
        cell.grid = self
        self.cells.append(cell)
        # sort grid based on cell priority
        self.cells.sort(key=lambda x: x.priority)
    
    def remove_cell(self, cell):
        self.cells.remove(cell)
    
    def get_cell(self, *args):
        for cell in self.cells:
            if cell.pos == args[0]:
                return cell
        return None
    
    def save_code(self) -> str:
        """Creates a string from the level"""
        format_version = settings['options']['other']['export_format']
        if format_version == "Py1":
            width = self.width
            height = self.height
            cells = self.cells
            unique_cells = list(set([cell.id for cell in cells]))
            cell_codes = {}
            for i, cell in enumerate(unique_cells):
                cell_codes[cell] = {'b64':base64.b64encode(cell.encode()).decode(),'index':i}
            cell_info = []
            for cell in cells:
                cell_info.append(f"({cell_codes[cell.id]['index']};{cell.pos[0]};{cell.pos[1]};{"R" if cell.dir[0] == 1 else "L" if cell.dir[0] == -1 else "U" if cell.dir[1] == 1 else "D" if cell.dir[1] == -1 else "?"});")
            code = str({format_version})+"!"+str({width})+"!"+str({height})+"!"+str({f"{cell['b64']};{cell['index']};" for cell in cell_codes.values()})+"!"+str({cell for cell in cell_info})+"!"
        return code

    def load_code(self, code: str) -> None:
        """Loads a level from a string"""
        code = code.split("!")
        format_version = code[0]
        if format_version == "Py1":
            width = code[1]
            height = code[2]
            cell_codes = code[3]
            cell_info = code[4]
            cell_codes = cell_codes.split(";")
            cell_codes = {
                cell_codes[i+1]:base64(cell_codes[i]).decode() for i in range(0, len(cell_codes), 2)
            }
            cell_info = cell_info.split(";")
            cell_info = [
                (cell_info[i].split("(")[1].split(")")[0].split(";") for i in range(len(cell_info)))
            ]
            directions = {"R":vec2(1,0), "L":vec2(-1,0), "U":vec2(0,1), "D":vec2(0,-1)}
            cell_info = [
                (
                    cell_codes[cell_info[i][0]],
                    vec2(int(cell_info[i][1]), int(cell_info[i][2])),
                    directions[cell_info[i][3]]
                ) for i in range(len(cell_info))
            ]
            for cell in self.cells:
                del cell
            self.cells = []
            for cell in cell_info:
                self.add_cell(__all_cells__[cell[0]](cell[1], cell[2]))
            return


class Cell:
    """The base class for all cells. Contains basic functionality and tools for all cells to make use of. Check the [modding api docs]([wiki](https://github.com/TenCommands/pycellmachine/docs/modding_api.md)) for more information."""
    _registry = []
    def __init__(self, pos: tuple, dir: tuple, flags: list=[], priority=0, texture=None):
        self.pos = vec2(pos)
        self.dir = vec2(dir)
        self.flags = flags
        self.priority = priority
        self.texture = texture
        self.__grid__ = None
        Cell._registry.append(self)
    
    @classmethod
    def __all_instances__(cls):
        return cls._registry

    def set_rotation(self, dir: vec2):
        """Sets the direction of the cell."""
        self.dir = dir
    
    def rotate_clockwise(self):
        """Rotates the cell clockwise."""
        angle = vec2_to_deg(self.dir)
        angle += 90
        self.dir = deg_to_vec2(angle)
    
    def rotate_counterclockwise(self):
        """Rotates the cell counter-clockwise."""
        angle = vec2_to_deg(self.dir)
        angle -= 90
        self.dir = deg_to_vec2(angle)
    
    def goto(self, *args):
        """Moves the cell to a specific position."""
        if len(args) == 1:
            self.pos = args[0]

    def move(self, *args):
        """Moves the cell if the destination is within grid boundaries.\n\n
        Returns whether or not the move was successful."""
        # Calculate the new position
        if len(args) == 1:
            # Assume args[0] is a vec2
            new_pos = self.pos + args[0]
        else:
            return False
        
        # Check if the cell has a reference to its grid
        if hasattr(self, 'grid') and self.cells is not None:
            # Check if the new position is within grid boundaries
            if 0 <= new_pos[0] < self.cells.width and 0 <= new_pos[1] < self.cells.height:
                # Check if there's already a cell at the new position
                cell_at_pos = None
                for cell in self.cells.grid:
                    if hasattr(cell, 'pos') and cell.pos == new_pos:
                        cell_at_pos = cell
                        break
                
                if cell_at_pos is not None:
                    # Notify the cell about the collision
                    if hasattr(cell_at_pos, 'on'):
                        cell_at_pos.on(event("cell_collide", cell=self, dir=args[0]))
                    
                    # Determine the direction to push
                    push_dir = None
                    if len(args) == 1:
                        push_dir = args[0]
                    
                    # Try to push the cell in the same direction
                    if push_dir and hasattr(cell_at_pos, 'move'):
                        if cell_at_pos.move(push_dir):
                            self.pos = new_pos
                            return True
                        else:
                            # The cell couldn't be pushed
                            return False
                    else:
                        # Can't push the cell
                        return False
                else:
                    # No cell at the new position, just move there
                    self.pos = new_pos
                    return True
            else:
                # New position is outside grid boundaries
                return False
        else:
            # If there's no grid reference, just update the position
            self.pos = new_pos
            return True

    def render(self, render_properties):
        """Default render method for all cells. Draws a rectangle with the texture of the cell. CAN BE OVERRIDDEN."""
        if isinstance(self.texture, tuple):
            pygame.draw.rect(render_properties['screen'], self.texture, (self.x, self.y, self.width, self.height))
        else:
            screen_height = render_properties['screen'].get_height()
            scaled_texture = pygame.transform.scale(
                self.texture,
                (render_properties['scale'], render_properties['scale'])
            )
            rotation_angle = 0
            if hasattr(self, 'dir'):
                if self.dir == (0, -1):
                    rotation_angle = 90
                elif self.dir == (1, 0):
                    rotation_angle = 0
                elif self.dir == (0, 1):
                    rotation_angle = 270
                elif self.dir == (-1, 0):
                    rotation_angle = 180
            rotated_texture = pygame.transform.rotate(scaled_texture, rotation_angle)
            x_pos = render_properties['offset'][0] + self.pos[0] * render_properties['scale']
            top_y = render_properties['offset'][1] + self.pos[1] * render_properties['scale']
            grid_height_px = render_properties['grid'].height * render_properties['scale']
            y_pos = screen_height - top_y - render_properties['scale']
            render_properties['screen'].blit(
                rotated_texture,
                (x_pos, y_pos)
            )

    def play_sound(self, sound):
        """Plays a sound."""
        pygame.mixer.Sound(sound).play()
    
    def delete(self):
        """Delete cell from memory"""
        self.cells.grid.remove(self)
        del self