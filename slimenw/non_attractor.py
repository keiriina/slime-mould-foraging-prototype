import numpy as np

# non-attractor class
class NonAttractor:
    # function to initialize non-attractor location and repulsion strength
    def __init__(self, x, y, strength=15):
        self.location = np.array([x, y], dtype=float)
        self.strength = strength  # Higher value means stronger repulsion, lower value is the opposite. this is for non-attractor customization
        self.radius = 30  # Effective radius of repulsion
