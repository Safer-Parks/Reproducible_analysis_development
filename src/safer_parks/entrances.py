from shapely import Point, LineString, remove_repeated_points, unary_union
import numpy as np
import matplotlib.pyplot as plt
import osmnx as ox

def interpolated(G, park_polygon):
    entrance_points = []
    for u, v in G.edges():
        u_pt = Point(G.nodes[u]['x'], G.nodes[u]['y'])
        v_pt = Point(G.nodes[v]['x'], G.nodes[v]['y'])
        if park_polygon.contains(u_pt) != park_polygon.contains(v_pt):
            # Edge crosses boundary, interpolate intersection
            line = LineString([u_pt, v_pt])
            intersection = line.intersection(park_polygon.boundary)
            if not intersection.is_empty:
                if intersection.geom_type == 'Point':
                    entrance_points.append(intersection)
                elif intersection.geom_type == 'MultiPoint':
                    entrance_points.extend(intersection.geoms)
    print(f"Found {len(entrance_points)} entrance nodes, note that these need to be deduplicated.")
    merged_points = unary_union(entrance_points)
    merged_points_list = [(merged_points.geoms[i].x, merged_points.geoms[i].y) for i in range(len(merged_points.geoms))]
    print(f"Found {len(merged_points_list)} entrance nodes after deduplication.")
    return merged_points

def tagged(location):
    # Tags likely to denote entrances
    entrance_tags = {
        "entrance": True,
        "barrier": ["gate", "entrance"]
    }

    # Pull geometries tagged as entrances
    entrances = ox.features.features_from_address(location, entrance_tags, 300)

    # Filter to point geometries (actual entrance nodes)
    entrance_points_tag = entrances[entrances.geom_type == "Point"]

    print(f"Found {len(entrance_points_tag)} explicitly tagged entrance nodes.")
    return entrance_points_tag