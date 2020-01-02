# Diffusion-limited aggregation algorithm

Diffusion-limited aggregation effectively describes a system where diffusion is the primary way of transportation, so that particles moving via Brownian motion cluster together forming aggregates, or Brownian trees ([Wikipedia.](https://en.wikipedia.org/wiki/Diffusion-limited_aggregation)). This program is an attempt to implement this algorithm in a simple 2D case.

The algorithm:
  * Place a seed at the center of the lattice.
  * Release a random walker from the edge.
  * Random walker sticks to the neighbouring sites of the seed/previous points.
  * Repeat N times.

Run of N = 1000 on a 120x120 size lattice:

![Run of N = 1000 on a 120x120 size lattice.](/images/dla_dendrite_growth_N1000.png)
