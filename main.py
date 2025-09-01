from slime.mold import MoldSimulation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def main():
    # Initialize simulation
    sim = MoldSimulation()
    
    # Add food at the same positions as the original PDE
    food_positions = [
        (210, 431), (255, 592), (399, 596), (657, 476),
        (641, 117), (287, 173), (492, 206), (478, 428),
        (398, 264), (509, 606), (357, 395), (428, 464)
    ]
    sim.add_food_sources(food_positions)

    # Matplotlib setup
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, sim.width)
    ax.set_ylim(0, sim.height)
    ax.set_title("Slime Mold Simulation")
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
        color="black",  # Original used black ellipses
        s=60,  # Smaller size as requested
        zorder=3,
        marker="o"  # Circular shape like the original
    )

    # Create line objects for nuclei trails outside of init/update functions
    # Initially create empty lines, we'll use them in both init and update
    lines = []
    
    # Create a scatter object for the nucleus positions (end of trails)
    nucleus_scatter = ax.scatter([], [], color='#c0c0c0', s=25, alpha=0.8, zorder=4)
    
    def init():
        # Clear existing lines and create new ones
        nonlocal lines
        lines = []
        for _ in range(sim.num_nuclei):  # Use num_nuclei to create the correct number of lines
            # Set all lines to light gray (#c0c0c0) and thinner as requested
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
        # Ensure we have the right number of lines
        while len(lines) < len(sim.cells):
            # Make sure any new lines also use light gray (#c0c0c0) and thinner width
            line, = ax.plot([], [], color='#c0c0c0', alpha=0.7, linewidth=0.8)
            lines.append(line)
        
        # Update each line with cell trail data
        for idx, cell in enumerate(sim.cells):
            if idx < len(lines):  # Safety check
                lines[idx].set_data(cell.trail_x, cell.trail_y)
        
        # Get the current positions of all nuclei to update the circles at end of trails
        current_positions = np.array([[cell.location[0], cell.location[1]] 
                                     for cell in sim.cells if len(cell.trail_x) > 0])
        
        # Update the nucleus scatter with current positions
        if len(current_positions) > 0:  # Only update if we have positions
            nucleus_scatter.set_offsets(current_positions)

        return lines + [oat_scatter, nucleus_scatter]

    # Animate
    ani = FuncAnimation(fig, update, frames=200, init_func=init, blit=True, interval=50)

    plt.show()

    # Export CSV after simulation
    sim.export_force_grid("new.csv")
    print("Simulation complete. CSV exported.")


if __name__ == "__main__":
    main()
