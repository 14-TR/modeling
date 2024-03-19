#########################################################
"""

Title: surface_noise.py
Author: TR Ingram
Description:


"""
#########################################################

import perlin as p
import matplotlib.pyplot as plt
import numpy as np
#generate a 2d grid of perlin noise that is 20 by 20
def generate_noise(w, h, vi, vj, z):
    noise = p.Perlin(14)
    grid = np.zeros((w, h))
    for i in range(w):
        for j in range(h):
            grid[i, j] = noise.noise(i*vi, j*vj, z)
    return grid

# noise = p.Perlin(14)
# w=100
# h=100
# grid = np.zeros((w, h))
# for i in range(w):
#     for j in range(h):
#         grid[i,j] = noise.noise(i*0.1, j*0.2, 0)

# grid = generate_noise(100, 100, 0.1, 0.2, 0)

# # plot grid
# plt.imshow(grid, cmap='terrain')
# plt.colorbar()
# plt.title('2D Perlin Noise')
# plt.show()

