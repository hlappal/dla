# Diffusion-limited aggregation
#
# The algorithm:
#  Place a seed at the center of the lattice.
#  Release a random walker from the edge.
#  Random walker sticks to the neighboring sites of the seed.
#  Repeat N times, leads into dendrite growth.
#
# Code by Heikki Lappalainen
# email: heikki.lappalainen@protonmail.com
# Date: 30 Dec 2019

import numpy as np
import matplotlib.pyplot as plt

latt = [h, w] = [120, 120]  # height and width of the lattice
N = 1000                    # number of random walkers
lattice = np.zeros((h, w)).astype(int)  # initialize empty lattice
lattice[h//2, w//2] = 1                 # initial seedd point
neighbors = []                          # the list of neighboring sites
# add the initial neighboring sites
neighbors.append([h//2 + 1, w//2])
neighbors.append([h//2 - 1, w//2])
neighbors.append([h//2, w//2 + 1])
neighbors.append([h//2, w//2 - 1])

def randomWalk(pos, lattice):
    """Perform a random walk from given point until contact"""
    
    while True:
        i = np.random.randint(2)  # choose vertical or horizontal movement
        pos[i] += np.random.randint(-1,2)  # choose direction and move
        # prevent walker going out of the lattice
        if pos[i] < 0:
            pos[i] = 0
            continue
        if pos[i] >= latt[i]:
            pos[i] -= 1
            continue
        # check for contact
        if pos in neighbors:
            # add the neighboring sites to the list
            for site in [[pos[0] + 1, pos[1]],
                         [pos[0] - 1, pos[1]],
                         [pos[0], pos[1] + 1],
                         [pos[0], pos[1] - 1]]:
                if site not in neighbors:  # prevent double counting
                    neighbors.append(site)
            lattice[pos[0], pos[1]] = 1
            return lattice

for i in range(N):
    print('Running random walker #{}'.format(i+1))
    # choose the starting position of the random walker
    pos = [x, y] = [np.random.randint(w), np.random.randint(h)]
    i = np.random.randint(2)  # choose either the x or y axis
    # the chosen axis assigned a value of either min or max to put it on
    # the lattice edge
    if np.random.rand() < 0.5:
        pos[i] = 0
    else:
        pos[i] = latt[i]-1
    # run random walk from the chosen site
    lattice = randomWalk(pos, lattice)

# simple plot
plt.matshow(lattice)
plt.xticks(ticks=[], labels=None)
plt.yticks(ticks=[], labels=None)
plt.show()
