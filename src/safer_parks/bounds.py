from shapely import Point, LineString, remove_repeated_points, unary_union
import numpy as np
import matplotlib.pyplot as plt
import osmnx as ox


# This is a very basic boundary calculation
def basic_boundary(location = "Peel Park, Bradford, UK"):
    tags = {"leisure": "park"}
    parks = ox.features.features_from_address(location, tags, 200)
    park = parks.iloc[0]
    park_polygon = park.geometry  # unbuffered!
    return park_polygon

# more complex park boundary calculation

def park_greenspace_boundary():
    pass

def buffer_network(park_polygon, buffer_m=0.001, type="walk"):
    network_buffer = park_polygon.buffer(buffer_m)
    G = ox.graph_from_polygon(network_buffer, network_type=type)
    return G