# Visibility analysis incorporating treeline

See [Visibility analysis notebook](../visability_analysis.ipynb) for work through.

The notebook above works through using a DEM for visibility analysis, however we also want to incorporate tree coverage as this will hugely alter the actual effective visibility when it comes to using the park.

- There's not a huge body of literature on this with regards women and girl's safety in parks, and what the best approach is, so we will have to choose an approach.

## Different applications of visibility analysis

Brief overview of the different techniques and what they can show us.

### Point to point analysis: gathering spaces, signage, park furniture

- Apply a grid across park area, and calculate visibility of each grid to each grid.
- Not just along networks, but should see how the network of paths intersects with this: are there "gathering areas" along path networks? A.k.a are they accessible to people using wheelchairs, pushchairs, mobility aids, or in the winter when grassy areas are difficult to cross?
- Is there street furniture, signage, lighting in these areas?

### Point to entrances analysis: openness, escape

- Where in the park feels remote/without an escape route?
- How does this correlate with signage and lighting?
- How does this correlate with networks/paths (see above for all the users of paths, e.g. mobility-aid users) - do paths take you on more poorly lit/remote routes?


## Point to entrances workflow in more depth

The notes in this section are about developing a workflow for point-to-entrance visibility (so for openness and escape), but some is also relevant for point-to-point.

### General approach for the park

- Line of sight analysis: this works in both directions, is reversible/reciprocal - simplifies things a lot!
    - This means visibility *from* an entrance to a point is equal to visbility *from* a point *to* the entrance.
- Each analysis outputs a raster DEM from one viewpoint/origin across area.
    - Repeat analysis with each entrance as the origin, producing multiple viewsheds.
    - Each resulting output rater is a binary black/white visible/not visible result.
- Combine these layers:
    - A number of different methods of combining, depending on the desired output.
    - "Does this point have line to sight to *at least one entrance*?"
        - Simple summing: if result > 1, the point is visible from at least one entrance. If result is zero, the area is not visible from an entrance.
    - "What areas of the park are most visible?"
        - Summing heatmap
    - "Least visible and most remote?"
        - Overlay result where visibility is zero, add to heatmap of remoteness

### Overview of workflow

1.  Individual Entrance Viewsheds
    - Calculate a viewshed from each entrance point
    - Each resulting raster shows areas that can see that specific entrance
    - Store these as separate layers (e.g., "viewshed_entrance_1", "viewshed_entrance_2", etc.)
2. Binary "Can See Any Entrance" Map
    - Formula: (viewshed_1 OR viewshed_2 OR viewshed_3 OR ...)
    - In most GIS software: Con(viewshed_1 == 1 OR viewshed_2 == 1 OR viewshed_3 == 1, 1, 0)
    - Result: Binary map where 1 = can see at least one entrance, 0 = cannot see any entrance
3. Visibility Heatmap
    - Sum all entrance viewsheds: viewshed_1 + viewshed_2 + viewshed_3 + ...
    - Result: Each pixel value represents the number of entrances visible from that location
    - Style as a heatmap with color ramp

## Point to point workflow in more depth

> TO DO: Add more notes here!

## Decisions with trees/shrubs

- Do we assume no permeability/solid?

For partially permeable, there is this study:

> [A new GIS-compatible methodology for visibility analysis in digital surface models of earth sites](https://www.sciencedirect.com/science/article/pii/S1674987120302498#s0010)

This is a much simpler approach assuming the layer is totally solid: [Viewshed Analysis incorporating tree height](https://gis.stackexchange.com/questions/215320/viewshed-analysis-incorporating-tree-height)

In general for the trees layer - count it as just the trunk, not the foliage, 60/70 cm, opaque for shrubs, how we frame it for the dashboard - "worst case scenario" for visibility.

## General points

- Ways you can improve visability, maintain tree branches etc., 50 % permeable, etc.
- Also took into account: tennis courts, fences, football courts don't, for visibility?
- Playgrounds, often have bushes and fences.
- 1 m height wheelchair user, also for girls. Very explicitly make a point that this is being used for visibility analysis.

