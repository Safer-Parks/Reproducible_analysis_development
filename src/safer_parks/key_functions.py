# import geopandas as gpd
# from shapely.ops import unary_union

### funciton that subsets a greenspace (or similar file) 
# to only include greenspaces within a chosen local authority

def subset_to_LAD(LAD_gdf, LAD_column_name, LAD_name, data_to_subset):
    chosen_LAD =LAD_gdf.loc[LAD_gdf[LAD_column_name]==LAD_name,:]
    chosen_LAD =chosen_LAD.to_crs(data_to_subset.crs)
    data_subset_to_LAD =data_to_subset[data_to_subset.within(chosen_LAD.unary_union)]
    return data_subset_to_LAD

### function that combines greenspace geographies that are intersecting or touching 
# to provide a more simplified boundary for parks more closely aligned to a perceived park
# e.g. combines a park mad-up of woodland-sports fields and open greenspaces into one park 

# written with support fo co-pilot
def merge_touching_or_intersecting_polygons(gdf):
    # Ensure the GeoDataFrame has a valid CRS
    gdf = gdf.to_crs(gdf.estimate_utm_crs())

    # Create a spatial index for efficient spatial queries
    spatial_index = gdf.sindex

    # Track which geometries have been processed
    merged = []
    used = set()

    for idx, geom in enumerate(gdf.geometry):
        if idx in used:
            continue

        # Find all geometries that intersect or touch the current one
        possible_matches_index = list(spatial_index.intersection(geom.bounds))
        candidates = gdf.iloc[possible_matches_index]
        touching_or_intersecting = candidates[candidates.geometry.apply(lambda x: x.intersects(geom) or x.touches(geom))]

        # Combine all geometries
        merged_geom = unary_union(touching_or_intersecting.geometry)

        # Combine attributes by concatenating non-null values
        combined_attributes = {}
        for column in gdf.columns:
            if column != 'geometry':
                combined_attributes[column] = touching_or_intersecting[column].dropna().astype(str).str.cat(sep='; ')

        # Append the merged geometry and attributes
        merged.append({**combined_attributes, 'geometry': merged_geom})

        # Mark these indices as used
        used.update(touching_or_intersecting.index)

    # Create a new GeoDataFrame with the merged results
    merged_gdf = gpd.GeoDataFrame(merged, crs=gdf.crs)

    return merged_gdf

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
            touching_or_intersecting = candidates[candidates.geometry.apply(lambda x: x.intersects(geom) or x.touches(geom))]

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
