## The algorithm
The Flood Fill algorithm is a widely used technique in computer graphics and image processing to identify and fill connected regions within a multi-dimensional array or grid, often a 2D grid of pixels or cells.

## How it solves the problem

- Grid (or Map): the data structure is typically a 2D array, where each cell has a value (e.g., a color, a status like 'filled' or 'empty', or a number).

<img src="/docs/images/grid.PNG" width="300">

- Connected region: a set of cells where each cell is adjacent (usually defined as 4-way or 8-way connectivity) to at least one other cell in the set, and all cells in the set share a common characteristic, such as the same color or a specific value.

<img src="/docs/images/connected-region.PNG" width="300">

- Goal: the algorithm starts at a given cell (seed point) and aims to change the color/value of all adjacent cells that belong to the same connected region until the boundary of that region is reached. This is often described as "filling" the region.

<img src="/docs/images/seed-point.PNG" width="300">
