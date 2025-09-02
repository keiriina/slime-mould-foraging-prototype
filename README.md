# 🧫 Slime Mould Algorithm - Foraging

This is an experimental project that simulates the foraging behavior of slime mould (Physarum polycephalum). The prototype models how slime mould explores its environment, forms efficient networks between food sources, and adapts its structure through growth and refinement.

## Project Structure

```
slime-mould/
│
├── main.py                 # Main entry point for standard simulation
├── main_non_attractor.py   # Entry point for simulation with obstacles
│
├── slime/                  # Standard slime mold simulation
│   ├── mold.py             # Core simulation engine
│   ├── nucleus.py          # Cell/nucleus implementation
│   ├── food.py             # Food source implementation
│   └── grid.py             # Grid utility
│
├── slimenw/                # Slime mold simulation with non-attractors (obstacles)
│   ├── n_mold.py           # Enhanced simulation with non-attractor avoidance
│   ├── n_nucleus.py        # Enhanced nucleus with non-attractor response
│   └── non_attractor.py    # Non-attractor implementation
│
└── environment.yml         # Conda environment specification
```

## Setup

1. Install conda ([installation guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html))

2. Create environment:
```bash
conda env create -f environment.yml
```

3. Activate environment:
```bash
conda activate slime
```

4. Run simulations:
```bash
# Standard simulation (attraction only)
python main.py

# Simulation with obstacles (attraction and repulsion)
python main_non_attractor.py
```

5. Deactivate environment when done:
```bash
conda deactivate
```

6. If environment.yml gets updated:
```bash
conda env update --name slime --file environment.yml --prune
```

## How It Works

### Basic Foraging Behavior

The simulation models how slime mold cells (nuclei) navigate toward food sources, creating trails between them. When enough nuclei reach a food source, it becomes a new spawn point for more nuclei, simulating how real slime molds create efficient networks between food sources (attractors). On the other hand, the non-attractor adds the ability to model obstacles or undesirable regions that slime mold avoids:



This allows for more complex simulations where slime molds must navigate around obstacles while still finding efficient paths between food sources.

## Reference

[Article: Stepwise Physarum polycephalum inspired algorithm](https://www.nature.com/articles/s41598-022-05439-w)# 🧫 Slime Mould Algorithm - Foraging

This is an experimental project that simulates the foraging behavior of slime mould (Physarum polycephalum). The prototype models how slime mould explores its environment, forms efficient networks between food sources, and adapts its structure through growth and refinement.

## Project Structure

```
slime-mould/
│
├── main.py                 # Main entry point for standard simulation
├── main_non_attractor.py   # Entry point for simulation with obstacles
│
├── slime/                  # Standard slime mold simulation
│   ├── mold.py             # Core simulation engine
│   ├── nucleus.py          # Cell/nucleus implementation
│   ├── food.py             # Food source implementation
│   └── grid.py             # Grid utility
│
├── slimenw/                # Slime mold simulation with non-attractors (obstacles)
│   ├── n_mold.py           # Enhanced simulation with non-attractor avoidance
│   ├── n_nucleus.py        # Enhanced nucleus with non-attractor response
│   └── non_attractor.py    # Non-attractor implementation
│
└── environment.yml         # Conda environment specification
```

## Setup

1. Install conda ([installation guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html))

2. Create environment:
```bash
conda env create -f environment.yml
```

3. Activate environment:
```bash
conda activate slime
```

4. Run simulations:
```bash
# Standard simulation (attraction only)
python main.py

# Simulation with obstacles (attraction and repulsion)
python main_non_attractor.py
```

5. Deactivate environment when done:
```bash
conda deactivate
```

6. If environment.yml gets updated:
```bash
conda env update --name slime --file environment.yml --prune
```

## How It Works

### Basic Foraging Behavior

The simulation models how slime mold cells (nuclei) navigate toward food sources, creating trails between them. When enough nuclei reach a food source, it becomes a new spawn point for more nuclei, simulating how real slime molds create efficient networks between food sources (attractors). On the other hand, the non-attractor adds the ability to model obstacles or undesirable regions that slime mold avoids:



This allows for more complex simulations where slime molds must navigate around obstacles while still finding efficient paths between food sources.

## Reference

[Article: Stepwise Physarum polycephalum inspired algorithm](https://www.nature.com/articles/s41598-022-05439-w)