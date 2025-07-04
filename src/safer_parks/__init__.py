from . import bounds
from . import entrances

# This line by default imports the basic_boundary function as park_polygon
# This should hopefully make it easier to swap out the boundary function in future
# for more complex function
from .bounds import basic_boundary as park_polygon