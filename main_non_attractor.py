import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import sys
import os

# Import the non-attractor mold simulation
from slimenw.n_mold import MoldSimulation as NonAttractorMoldSimulation


def main():
    # Initialize simulation
    sim = NonAttractorMoldSimulation()
    
    # Add food at the same positions as the original PDE
    food_positions = [
        (210, 431), (255, 592), (399, 596), (657, 476),
        (641, 117), (287, 173), (492, 206), (478, 428),
        (398, 264), (509, 606), (357, 395), (428, 464)
    ]
    sim.add_food_sources(food_positions)

    # Add non-attractors (obstacles) to the simulation
    # Each non-attractor is defined by (x, y) or (x, y, strength) where strength controls repulsion power
    non_attractors = [
        (350, 350, 20),  # Strong obstacle in center
        (450, 250, 15),  # Medium obstacle
        (250, 450, 15),  # Medium obstacle
        (150, 150),      # Default strength obstacle
        (600, 600)       # Default strength obstacle
    ]
    sim.add_non_attractors(non_attractors)

    # Matplotlib setup
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, sim.width)
    ax.set_ylim(0, sim.height)
    ax.set_title("Slime Mold Simulation with Non-Attractors")
    ax.set_aspect("equal")
    
    # Add grid with more prominent lines
    ax.grid(True, linestyle='-', linewidth=1.0, alpha=0.8)
    
    # Add major grid lines at fixed intervals
    major_ticks = np.arange(0, sim.width + 1, 100)
    ax.set_xticks(major_ticks)
    ax.set_yticks(major_ticks)
    ax.grid(which='major', linestyle='-', linewidth=2.0, color='gray', alpha=0.8)
    
    # Add minor grid lines for more detail
    minor_ticks = np.arange(0, sim.width + 1, 50)
    ax.set_xticks(minor_ticks, minor=True)
    ax.set_yticks(minor_ticks, minor=True)
    ax.grid(which='minor', linestyle=':', linewidth=0.5, color='gray', alpha=0.5)
    
    # Scatter for oats (food) - smaller black circles
    oat_scatter = ax.scatter(
        [o.location[0] for o in sim.oats_permanent],
        [o.location[1] for o in sim.oats_permanent],
        color="black",  
        s=60,  
        zorder=3,
        marker="o"  
    )
    
    # Scatter for non-attractors - red circles with radius
    for na in sim.non_attractors:
        ax.scatter(
            na.location[0], 
            na.location[1],
            color="red", 
            s=80, 
            alpha=0.7, 
            zorder=2, 
            marker="o"
        )
        # Draw radius of influence
        circle = plt.Circle(
            (na.location[0], na.location[1]), 
            na.radius, 
            fill=False, 
            color='red', 
            linestyle='--', 
            alpha=0.3
        )
        ax.add_patch(circle)

    # Create line objects for nuclei trails outside of init/update functions
    # Initially create empty lines
    lines = []
    
    # Create a scatter object for the nucleus positions (end of trails)
    nucleus_scatter = ax.scatter([], [], color='#c0c0c0', s=25, alpha=0.8, zorder=4)
    
    def init():
        # Clear existing lines and create new ones
        nonlocal lines
        lines = []
        for _ in range(sim.num_nuclei):  
            line, = ax.plot([], [], color='#c0c0c0', alpha=0.7, linewidth=0.8)
            lines.append(line)
        
        for line in lines:
            line.set_data([], [])
        
        # Initialize with empty data
        nucleus_scatter.set_offsets(np.empty((0, 2)))
        
        return lines + [oat_scatter, nucleus_scatter]

    def update(frame):
        sim.step()  # advance simulation one step
        
        nonlocal lines
        while len(lines) < len(sim.cells):
            line, = ax.plot([], [], color='#c0c0c0', alpha=0.7, linewidth=0.8)
            lines.append(line)
        
        for idx, cell in enumerate(sim.cells):
            if idx < len(lines):  # Safety check
                lines[idx].set_data(cell.trail_x, cell.trail_y)
        
        # Get the current positions of all nuclei to update the circles at end of trails
        current_positions = np.array([[cell.location[0], cell.location[1]] 
                                     for cell in sim.cells if len(cell.trail_x) > 0])
        
        # Update the nucleus scatter with current positions
        if len(current_positions) > 0: 
            nucleus_scatter.set_offsets(current_positions)

        return lines + [oat_scatter, nucleus_scatter]

    # Animate
    ani = FuncAnimation(fig, update, frames=200, init_func=init, blit=True, interval=50)

    plt.show()

    # Export CSV 
    sim.export_force_grid("new_with_obstacles.csv")
    print("Simulation complete. CSV exported.")


if __name__ == "__main__":
    main()
