import numpy as np

# food class
class Food:
    # function to initialize food location
    def __init__(self, x, y):
        self.location = np.array([x, y], dtype=float)
        self.nuclei_index = [] # list to store indices of nuclei that have consumed this food

    # add a nucleus index to the list of connected nuclei
    def add_nucleus(self, index):
        # avoid duplicates
        if index not in self.nuclei_index:
            self.nuclei_index.append(index)
