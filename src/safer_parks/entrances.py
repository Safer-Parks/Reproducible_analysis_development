from shapely import Point, LineString, remove_repeated_points, unary_union
import numpy as np
import matplotlib.pyplot as plt
import osmnx as ox
import geopandas as gpd

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

def plot(G, interp_points="na", tagged_points="na"):
    fig, ax = ox.plot_graph(
        G,
        node_color='gray',
        node_size=10,
        show=False,
        close=False
    )

    if not interp_points == "na":
        xs = [pt.x for pt in interp_points.geoms]
        ys = [pt.y for pt in interp_points.geoms]
        ax.scatter(xs, ys, c='magenta', s=40, marker='x', label=f'Deduplicated interpolated entrances (N={len(xs)})', zorder=4)

    if isinstance(tagged_points, gpd.GeoDataFrame):
        xs = tagged_points.geometry.x
        ys = tagged_points.geometry.y
        ax.scatter(xs, ys, c='yellow', s=200, alpha=0.7, marker='*', label=f'OSM-tagged Entrances (N={len(xs)})', zorder=4)
    ax.legend()
    return fig, ax
