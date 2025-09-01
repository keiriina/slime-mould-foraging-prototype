import numpy as np
import pandas as pd

class Nucleus:
    def __init__(self, x, y, seed):
        # initialize with position and seed 
        self.location = np.array([x, y], dtype=float)
        self.acceleration = np.array([0.0, 1.0], dtype=float)  
        self.velocity = np.array([0.0, 0.0], dtype=float) 
        self.seed = seed
        
        # initialize trail tracking (like the original FloatList x, y)
        self.trail_x = [x] 
        self.trail_y = [y]
        
        # initialize closest oat tracking
        self.closest_oat_index = None
        
        # initialize noise state variables
        self.u, self.v = 0.0, 0.0       # current noise values (taken from somewhere)
        self.nU, self.nV = 0.0, 0.0     # noise position
        self.mapU, self.mapV = 0.0, 0.0 # mapped noise

    def apply_force(self, force):
        self.acceleration += force

    def set_closest_oat(self, idx):
        self.closest_oat_index = idx

    def move(self):
        # Perlin noise implementation 
        # Set random seed based on nucleus seed for consistent noise
        np.random.seed(self.seed)
        u = np.random.uniform(0, 1)  
        np.random.seed(self.seed + 1)
        v = np.random.uniform(0, 1)
        
        # Map from [0,1] to [-1,1] 
        map_u = (u * 2) - 1
        map_v = (v * 2) - 1
        
        # create velocity vector and apply acceleration 
        velocity = np.array([map_u, map_v], dtype=float)
        velocity += self.acceleration
        
        # Set magnitude to 0.5 
        if np.linalg.norm(velocity) > 0:
            velocity = velocity / np.linalg.norm(velocity) * 0.5
        
        # subtract from location (move in opposite direction as in original)
        self.location -= velocity
        
        # reset acceleration and increment noise values
        self.acceleration *= 0
        self.nU += 0.01
        self.nV += 0.01
    
    # record the trail
    def record_trail(self):
        # record the current location in the trail arrays
        self.trail_x.append(self.location[0])
        self.trail_y.append(self.location[1])

    # save to csv
    def save_trail(self, id_number):
        filename = f"{id_number}_Stem_Trail.csv"
        df = pd.DataFrame({"x": self.trail_x, "y": self.trail_y})
        df.to_csv(filename, index=False)
