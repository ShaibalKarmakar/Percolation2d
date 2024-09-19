import os

import numpy as np

import corr_length


p_mesh = [0.45, 0.46, 0.47, 0.48, 0.49]
p_fine_mesh = [0.491, 0.492, 0.493, 0.494, 0.495, 0.496, 0.497, 0.498, 0.499]

for p in p_fine_mesh:
    corr_length.main(p, n = 100, multiplier = 1.2, num_trials = 10000, num_processes = 5)
