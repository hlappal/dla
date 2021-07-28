#!/usr/bin/env python3

"""
Diffusion limited aggregation on central seed and on surface.

Author: Heikki Lappalainen
Email:  heikki.lappalainen@protonmail.com
"""

import sys
import argparse
import time
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


class CentralDLA():
    """
    DLA simulation on central seed. Random walkers spawn on random points at
    the lattice edges and perform Brownian walk until they hit a neighboring
    site of previous fixed sites.
    """
    def __init__(self, n_walkers: int, L: int, p: float) -> None:
        self.n_walkers = n_walkers                  # Number of random walkers
        self.L = L                                  # Lattice side length
        self.p = p                                  # Sticky factor in [0..1]
        self.lattice = np.zeros((L, L), dtype=int)  # Simulation lattice
        self.lattice[L//2, L//2] = 1                # Central seed
        self.pos = np.zeros(2, dtype=int)           # Current walker position
        # List the possible moves for random walkers: up, down, left, right
        self.moves = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])

    def init_walker(self) -> None:
        """
        Generate a new random walker on one of the four edges.
        """
        self.pos = np.array([np.random.randint(self.L),
                             np.random.choice([0, self.L-1])])

    def pos_valid(self, pos: np.array) -> bool:
        """
        Check if the given position is free and inside the lattice.

        Params:
          pos (np.array):  The position coordinates.
        Returns:
          (boolean):       True if the position is valid, False otherwise.
        """
        if (pos[0] >= 0 and pos[1] >= 0 and pos[0] < self.L and pos[1] < self.L
                and self.lattice[pos[0], pos[1]] == 0):
            return True
        return False

    def move_walker(self) -> None:
        """
        Move walker into one of the allowed neighboring sites.
        """
        while True:
            ind = np.random.randint(4)
            move = self.moves[ind]     # Random move direction
            new_pos = self.pos + move  # Trial move
            if self.pos_valid(new_pos):
                self.pos = new_pos     # Accept move
                break

    def on_sticky_site(self) -> None:
        """
        Determine if the walker is on a sticky site. For each adjacent
        direction in the lattice, check if the adjacent cell value is
        greater than zero (i.e. is occupied).

        Returns:
          (boolean):  True if on a sticky site, False otherwise.
        """
        inds = self.pos + self.moves
        inds = inds[(inds[:, 0] > 0) & (inds[:, 0] < self.L)
                    & (inds[:, 1] > 0) & (inds[:, 1] < self.L)]
        if (self.lattice[inds[:, 0], inds[:, 1]].sum() > 0):
            return True
        return False

    def run(self) -> None:
        """
        Run the simulation main loop.
        """
        start = time.time()

        for i in tqdm(range(self.n_walkers)):
            # Generate new walker
            self.init_walker()

            # Perform random walk until the walker hits a sticky site
            while True:
                # Check if the walker is on a sticky site
                if self.on_sticky_site():
                    # Fix the walker into the site with a running integer value
                    self.lattice[self.pos[0], self.pos[1]] = i+1
                    break

                # Take a random step
                self.move_walker()


        print(f"Simulated {self.n_walkers} random walks on a {self.L}x{self.L}"
              + f" lattice in {time.time() - start:.4f} seconds.")

    def plot(self) -> None:
        """
        Plot the simulation results.
        """
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(self.lattice, cmap='magma')
        plt.show()


class SurfaceDLA(CentralDLA):
    """
    DLA growth on a surface. The random walkers spawn on the top edge.
    The class inherits the CentralDLA class, but re-defines
    """
    def __init__(self, n_walkers: int, L: int, p=1.0) -> None:
        CentralDLA.__init__(self, n_walkers, L, p)
        self.lattice = np.zeros((L, L), dtype=int)  # Re-initialize the lattice
        self.lattice[L-1, :] = 1  # Surface at the bottom of lattice

    def init_walker(self) -> None:
        """
        Generate a new random walker on a random point at the top of the
        lattice. The growth might reach the lattice top, so the site must be
        checked.
        """
        self.pos[0] = 0
        while True:
            self.pos[1] = np.random.randint(self.L)
            if self.pos_valid(self.pos):
                break  # Accept valid position


def main(argv: list) -> None:
    """
    Simulation main loop.
    """
    print(argv[0])
    parser = argparse.ArgumentParser()
    parser.add_argument("model", metavar="model",
                        help="DLA growth type: [c]entral, [s]urface")
    parser.add_argument("walkers", metavar="num-walkers",
                        help="Number of random walkers", type=int)
    parser.add_argument("lattice", metavar="lattice",
                        help="Lattice side length", type=int)
    parser.add_argument("-p",
                        help="Sticky factor (default 1.0)", type=float)

    args = parser.parse_args()
    n_walkers = args.walkers
    L = args.lattice
    if args.p:
        p = args.p
    else:
        p = 1.0

    if args.model in ["c", "central"]:
        dla = CentralDLA(n_walkers, L, p)
    elif args.model in ["s", "surface"]:
        dla = SurfaceDLA(n_walkers, L, p)
    else:
        parser.print_help()
        sys.exit(1)

    dla.run()
    dla.plot()


if __name__ == "__main__":
    main(sys.argv[1:])
