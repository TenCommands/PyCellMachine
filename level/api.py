import pygame, json, numpy as math, base64, os, sys

settings = json.load(open(r'./pycellmachine/_internal/settings.json'))

#pygame.init()

x, y = 0, 0

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

def load_image(path):
    return pygame.image.load(path)

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

class vec2(vec):
    """A 2D vector"""
    def __new__(cls, x, y):
        return vec.__new__(cls, (x, y))

def vec2_to_deg(vec: vec2) -> float:
    """Converts a 2D vector (x, y) to degrees."""
    angle_rad = math.arctan2(vec[1], vec[0])
    angle_deg = math.degrees(angle_rad) % 360
    return angle_deg

def deg_to_vec2(deg: float) -> vec2:
    """Converts degrees to a 2D vector (x, y)."""
    rad = math.radians(deg)
    x = math.cos(rad)
    y = math.sin(rad)
    return vec2(x, y)

# create event handler decorator which gives the event information to the function
# the event handler decorator should be used on a function that takes an event as an argument
#def event_handler(event_type): 
#    def decorator(func):
#        def wrapper(self, event):
#            if event.type == event_type:
#                func(self, event)
#                return func(self, event)

class event:
    def __init__(self, *args):
        self.type = args[0]
        self.cell = args[1]

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
        # Add timing control for tick rate
        current_time = pygame.time.get_ticks()
        
        # Initialize last_tick_time if it doesn't exist
        if not hasattr(self, 'last_tick_time'):
            self.last_tick_time = 0
        
        # Check if enough time has passed (50ms = 1/20th of a second)
        if current_time - self.last_tick_time >= 50:
            # Update the last tick time
            self.last_tick_time = current_time
            
            # Process ticks for all cells
            for cell in self.grid:
                cell.tick()

    
    def add_cell(self, cell):
        cell.grid = self
        print(cell.pos)
        self.grid.append(cell)
    
    def remove_cell(self, cell):
        self.grid.remove(cell)
    
    def get_cell(self, x, y):
        for cell in self.grid:
            if cell.pos == (x, y):
                return cell
        return None


class Cell:
    """The base class for all cells. Contains basic functionality and tools for all cells to make use of. Check the [modding api docs]([wiki](https://github.com/TenCommands/pycellmachine/docs/modding_api.md)) for more information."""
    _registry = []
    def __init__(self, id: str, pos: tuple, dir: tuple, flags: list=[], priority=0, texture=None):
        self.id = id
        self.pos = pos
        self.dir = dir
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
        elif len(args) == 2:
            self.pos = (args[0], args[1])

    def move(self, *args):
        """Moves the cell if the destination is within grid boundaries."""
        # Calculate the new position
        if len(args) == 1:
            new_pos = (self.pos[0] + args[0][0], self.pos[1] + args[0][1])
        elif len(args) == 2:
            new_pos = (self.pos[0] + args[0], self.pos[1] + args[1])
        else:
            return  # Invalid arguments
        
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
                        cell_at_pos.on(event("cell_collide", self))
                    
                    # Determine the direction to push
                    push_dir = None
                    if len(args) == 1:
                        push_dir = args[0]
                    elif len(args) == 2:
                        push_dir = (args[0], args[1])
                    
                    # Try to push the cell in the same direction
                    if push_dir and hasattr(cell_at_pos, 'move'):
                        cell_at_pos.move(push_dir)
                        
                        # Now check if the cell was actually moved
                        # If it was moved, we can move to its previous position
                        if cell_at_pos.pos != new_pos:
                            self.pos = new_pos
                else:
                    # No cell at the new position, just move there
                    self.pos = new_pos
        else:
            # If there's no grid reference, just update the position
            # This is the original behavior
            self.pos = new_pos


    def render(self, render_properties):
        """Default render method for all cells. Draws a rectangle with the texture of the cell. CAN BE OVERRIDDEN."""
        if isinstance(self.texture, tuple):
            pygame.draw.rect(render_properties['screen'], self.texture, (self.x, self.y, self.width, self.height))
        else:
            # Determine rotation angle based on self.dir
            rotation_angle = 0
            if hasattr(self, 'dir'):
                rotation_angle = vec2_to_deg(self.dir)
            
            # Scale the texture
            scaled_texture = pygame.transform.scale(
                self.texture,
                (render_properties['scale'], render_properties['scale'])
            )
            
            # Rotate the scaled texture
            rotated_texture = pygame.transform.rotate(scaled_texture, rotation_angle)
            
            # Calculate position adjustments for rotated texture
            # Rotation might change the size of the surface, so we need to center it
            pos_x = render_properties['offset'][0] + self.pos[0] * render_properties['scale']
            pos_y = render_properties['offset'][1] + self.pos[1] * render_properties['scale']
            
            # Center the rotated texture on the cell position
            pos_x += (render_properties['scale'] - rotated_texture.get_width()) // 2
            pos_y += (render_properties['scale'] - rotated_texture.get_height()) // 2
            
            # Blit the rotated and scaled texture
            render_properties['screen'].blit(
                rotated_texture,
                (pos_x, pos_y)
            )

    
    def play_sound(self, sound):
        """Plays a sound."""
        pygame.mixer.Sound(sound).play()