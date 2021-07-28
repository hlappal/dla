# Diffusion-limited aggregation

Diffusion-limited aggregation effectively describes a system where diffusion
is the primary way of transportation, so that particles moving via Brownian
motion cluster together forming aggregates, or Brownian trees
([Wikipedia.](https://en.wikipedia.org/wiki/Diffusion-limited_aggregation)).
This program implements the algorithm in simple 2D cases where the aggregate
grows around a central seed or up from a surface.

The algorithm:
  * Place a seed at the center of the lattice.
  * Release a random walker from the edge (or from the top in the surface
  case).
  * Random walker sticks to the neighbouring sites of the seed/previous points.
  * Repeat N times.

Example of central DLA with 1000 random walkers on a 100x100 lattice:

![Central DLA with N = 1000 on a 100x100 size lattice.](/images/dla_dendrite_growth_N1000.png)

## Usage

Run the program from the command line with

```
dla.py [-h] [-p P] model num-walkers lattice

positional arguments:
  model        DLA growth type: [c]entral, [s]urface
  num-walkers  Number of random walkers
  lattice      Lattice side length
  
optional arguments:
  -h, --help   Show this help message and exit
  -p sticky    Sticky factor (default 1.0)
```

## To do

The algorithm is not very optimized, as the walkers are released one at a time,
and there are no limiting conditions (birth/death distance, etc.).

The performance could be improved by:
 * Implementing the main loop as a Numpy operation
 * Introducing limiting conditions for the random walkers
