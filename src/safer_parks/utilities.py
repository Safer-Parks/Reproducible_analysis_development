# Functions migrated from safer_parks_functions.ipynb
from shapely import Point, LineString, remove_repeated_points, unary_union
import numpy as np
import matplotlib.pyplot as plt
import osmnx as ox
import geopandas as gpd

def clean_and_deduplicate(values, separator=';'):
    """
    Cleans a list of separator-separated strings by removing duplicates,
    stripping whitespace, and avoiding repeated separators.
    """
    items = [item.strip() for item in str(values).split(separator) if item.strip()]
    seen = set()
    cleaned = [x for x in items if not (x in seen or seen.add(x))]
    return separator.join(cleaned)

def merge_touching_or_intersecting_polygons_condense(gdf):
    gdf = gdf.to_crs(gdf.estimate_utm_crs())

    while True:
        spatial_index = gdf.sindex
        merged = []
        used = set()

        for idx, geom in enumerate(gdf.geometry):
            if idx in used:
                continue

            possible_matches_index = list(spatial_index.intersection(geom.bounds))
            candidates = gdf.iloc[possible_matches_index]
            touching_or_intersecting = candidates[candidates.geometry.apply(lambda x: x.intersects(geom) or x.touches(geom) or x.overlaps(geom))]

            merged_geom = unary_union(touching_or_intersecting.geometry)

            combined_attributes = {}
            for column in gdf.columns:
                if column != 'geometry':
                    raw_values = touching_or_intersecting[column].dropna().astype(str).str.cat(sep=', ')
                    combined_attributes[column] = clean_and_deduplicate(raw_values)

            merged.append({**combined_attributes, 'geometry': merged_geom})
            used.update(touching_or_intersecting.index)

        new_gdf = gpd.GeoDataFrame(merged, crs=gdf.crs)

        if len(new_gdf) == len(gdf):
            break

        gdf = new_gdf

    return gdf