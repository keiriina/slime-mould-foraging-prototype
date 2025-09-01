# 🧫 Slime Mould Algorithm - Foraging

This is an experimental project that simulates the foraging behavior of slime mould (Physarum polycephalum). The prototype models how slime mould explores its environment, forms efficient networks between food sources, and adapts its structure through growth and refinement.

## Set up
1. Install conda [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

2. Create environment.
```
conda env create -f environment.yml
```
3. Activate/Deactivate environment.
```
conda activate slime
conda deactivate
```
4. If environment.yml gets updated.
```
conda env update --name slime --file environment.yml --prune
```
5. Run code
```
python main.py
```