import numpy as np

# grid class
class Grid:
    # function to initialize grid location and closest food index
    def __init__(self, x, y, closest_food_index):
        self.location = np.array([x, y], dtype=float)
        self.closest_food_index = closest_food_index
