import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt  

from slime.nucleus import Nucleus
from slime.food import Food
from slime.grid import Grid


class MoldSimulation:
    # initialize
    def __init__(self, width=800, height=800, num_nuclei=50, num_cells_to_reach_oats=5, force_constant=10):
        self.width = width
        self.height = height
        self.num_nuclei = num_nuclei
        self.num_cells_to_reach_oats = num_cells_to_reach_oats
        self.force_constant = force_constant

        self.cells = []
        self.oats = []
        self.oats_permanent = []
        self.new_spawn_x = width / 2
        self.new_spawn_y = height / 2
        self.add_spawn = True
        self.trail_count = 0
        self.bool_once = True

    # add food in the grid
    def add_food_sources(self, food_coords):
        for x, y in food_coords:
            self.oats.append(Food(x, y))
            self.oats_permanent.append(Food(x, y))
    
    # run one simulation step
    def step(self):
        # Record trail only every 20 frames (matching original)
        self.trail_count += 1
        record_trail_this_frame = False
        if self.trail_count >= 20:
            record_trail_this_frame = True
            self.trail_count = 0
            
        # spawn nuclei once
        if self.add_spawn:
            for _ in range(self.num_nuclei):
                self.cells.append(Nucleus(self.new_spawn_x, self.new_spawn_y, int(np.random.randint(0, 10000))))
            self.add_spawn = False

        # update nuclei
        for i, cell in enumerate(self.cells):
            if self.oats:
                distances = [np.linalg.norm(cell.location - oat.location) for oat in self.oats]
                closest_idx = int(np.argmin(distances))
                cell.set_closest_oat(closest_idx)

                # force towards closest food
                temp_vector = cell.location - self.oats[closest_idx].location
                norm = np.linalg.norm(temp_vector)
                if norm > 0:
                    mag = sqrt(self.force_constant / norm)
                    temp_vector = temp_vector / norm * mag
                    cell.apply_force(temp_vector)

                # check if nucleus reached food
                for j, oat in enumerate(self.oats):
                    if np.linalg.norm(cell.location - oat.location) < 10 and i not in oat.nuclei_index:
                        oat.add_nucleus(i)
                        self.oats_permanent[j].add_nucleus(i)
                        cell.trail_x.append(oat.location[0])
                        cell.trail_y.append(oat.location[1])

                        if len(oat.nuclei_index) > self.num_cells_to_reach_oats:
                            self.add_spawn = True
                            self.new_spawn_x, self.new_spawn_y = oat.location
                            self.oats.pop(j)
                            break

        # move nuclei
        for cell in self.cells:
            cell.move()
            
        # record trail only every 20 frames
        if record_trail_this_frame:
            for cell in self.cells:
                cell.record_trail()

    def export_force_grid(self, filename="new.csv"):
        """Export force grid to CSV file, matching the original PDE logic"""
        grid_points = []
        grid_objects = []
        magnitudes = []
        
        # create grid objects and find closest oat for each
        for x in range(0, self.width, 10):
            for y in range(0, self.height, 10):
                # find closest oat to this grid point
                closest_idx, min_dist = None, float('inf')
                for i, oat in enumerate(self.oats_permanent):
                    # Use Euclidean distance
                    d = np.sqrt((x - oat.location[0])**2 + (y - oat.location[1])**2)
                    if d < min_dist:
                        closest_idx, min_dist = i, d
                
                # create grid object
                g = Grid(x, y, closest_idx)
                grid_objects.append(g)
                
                # calculate force vector
                vec = g.location - self.oats_permanent[g.closest_oat_index].location
                norm = np.linalg.norm(vec)
                if norm > 0:
                    mag = sqrt(self.force_constant / norm)
                else:
                    mag = 0  
                
                grid_points.append((x, y))
                magnitudes.append(mag)

        # Format 
        rows = self.height // 10
        cols = self.width // 10
        
        # Reshape the magnitudes list into a 2D grid
        grid_data = np.zeros((rows, cols))
        idx = 0
        for x in range(cols):
            for y in range(rows):
                if idx < len(magnitudes):
                    grid_data[y, x] = magnitudes[idx]
                    idx += 1
        
        # convert to df
        df = pd.DataFrame(grid_data)
        df.to_csv(filename, index=False, header=False)

    def plot(self):
        plt.figure(figsize=(8, 8))
        # draw trails
        for cell in self.cells:
            plt.plot(cell.trail_x, cell.trail_y, alpha=0.5)
        # draw food
        for oat in self.oats_permanent:
            plt.scatter(oat.location[0], oat.location[1], c="black", s=30)
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)
        plt.gca().invert_yaxis()
        plt.show()
