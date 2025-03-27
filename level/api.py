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
    def __init__(self, width: int, height: int, scale: int=1, offset: vec2=vec2(0, 0)):
        self.width = width
        self.height = height
        self.scale = scale
        self.x = 0
        self.y = 0
        self.grid = []
        Grid._registry.append(self)
    
    @classmethod
    def __all_instances__(cls):
        return cls._registry

    def move(self, x: int, y: int):
        self.x += x
        self.y += y
    
    def events(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            # Store the key state when keys are pressed or released
            self._update_key_states()
        
        # Check key states every frame, not just on KEYDOWN events
        self._process_movement_from_keys()
    
    def _update_key_states(self):
        # Get the current state of all keys
        self.key_states = pygame.key.get_pressed()
    
    def _process_movement_from_keys(self):
        # Only proceed if key_states has been initialized
        if not hasattr(self, 'key_states'):
            self._update_key_states()
            return
            
        keys = settings['options']['keybinds']
        
        # Check if the movement keys are currently pressed
        if self.key_states[getattr(pygame, 'K_' + keys['up'].lower())]:
            self.move(0, -1)
        if self.key_states[getattr(pygame, 'K_' + keys['left'].lower())]:
            self.move(-1, 0)
        if self.key_states[getattr(pygame, 'K_' + keys['down'].lower())]:
            self.move(0, 1)
        if self.key_states[getattr(pygame, 'K_' + keys['right'].lower())]:
            self.move(1, 0)


    def draw(self, screen):
        render_properties = {
                'screen': screen,
                'scale': self.scale*16,
                'offset': (self.x, self.y),
                'grid': self
            }
        # render a gray square for each cell position
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (50,50,50), (self.x+x*(self.scale*16), self.y+y*(self.scale*16), (self.scale*16), (self.scale*16)))
        
        for cell in self.grid:
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
                for cell in self.grid:
                    if hasattr(cell, 'tick'):
                        cell.tick()
        except Exception as e:
            print(f"Error {e}")

    
    def add_cell(self, cell):
        cell.grid = self
        self.grid.append(cell)
        # sort grid based on cell priority
        self.grid.sort(key=lambda x: x.priority)
    
    def remove_cell(self, cell):
        self.grid.remove(cell)
    
    def get_cell(self, *args):
        for cell in self.grid:
            if cell.pos == args[0]:
                return cell
        return None


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
        """Moves the cell if the destination is within grid boundaries.
        Returns True if the movement was successful, False otherwise."""
        # Calculate the new position
        if len(args) == 1:
            # Assume args[0] is a vec2
            new_pos = self.pos + args[0]
        else:
            return False
        
        # Check if the cell has a reference to its grid
        if hasattr(self, 'grid') and self.grid is not None:
            # Check if the new position is within grid boundaries
            if 0 <= new_pos[0] < self.grid.width and 0 <= new_pos[1] < self.grid.height:
                # Check if there's already a cell at the new position
                cell_at_pos = None
                for cell in self.grid.grid:
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
                            # The cell was successfully pushed, we can move to its previous position
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
            # This is the original behavior
            self.pos = new_pos
            return True  # Assume success in this case
        
        return False  # Default return if none of the above conditions are met

    def render(self, render_properties):
        """Default render method for all cells. Draws a rectangle with the texture of the cell. CAN BE OVERRIDDEN."""
        if isinstance(self.texture, tuple):
            pygame.draw.rect(render_properties['screen'], self.texture, (self.x, self.y, self.width, self.height))
        else:
            # Get screen height to calculate inverted y-coordinate
            screen_height = render_properties['screen'].get_height()

            # Scale the texture
            scaled_texture = pygame.transform.scale(
                self.texture,
                (render_properties['scale'], render_properties['scale'])
            )

            # Determine rotation angle based on self.dir
            rotation_angle = 0
            if hasattr(self, 'dir'):
                if self.dir == (0, -1):  # up
                    rotation_angle = 90  # Change from 0 to 270
                elif self.dir == (1, 0):  # right
                    rotation_angle = 0    # Change from 90 to 0
                elif self.dir == (0, 1):  # down
                    rotation_angle = 270   # Change from 180 to 90
                elif self.dir == (-1, 0):  # left
                    rotation_angle = 180  # Change from 270 to 180
            # Rotate the scaled texture
            rotated_texture = pygame.transform.rotate(scaled_texture, rotation_angle)

            # Calculate position with inverted y-coordinate
            # Original: y increases downward
            # New: y increases upward
            x_pos = render_properties['offset'][0] + self.pos[0] * render_properties['scale']

            # Invert the y-coordinate:
            # 1. Calculate the position from the top (as before)
            top_y = render_properties['offset'][1] + self.pos[1] * render_properties['scale']

            # 2. Invert it to position from the bottom
            # We need to consider:
            #   - The grid's height in cells
            #   - The cell's size (scale)
            #   - The grid's offset

            # Calculate the total height of the grid in pixels
            grid_height_px = render_properties['grid'].height * render_properties['scale']

            # Calculate the inverted y position
            y_pos = screen_height - top_y - render_properties['scale']

            # Blit the scaled texture at the calculated position
            render_properties['screen'].blit(
                rotated_texture,
                (x_pos, y_pos)
            )

    def play_sound(self, sound):
        """Plays a sound."""
        pygame.mixer.Sound(sound).play()