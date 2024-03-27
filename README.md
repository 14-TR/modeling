
---

### Documentation Overview

This project simulates a zombie outbreak scenario using an agent-based model in a geospatial grid environment. The simulation tracks interactions between humans and zombies, with a focus on resource distribution, movement dynamics, and the transformation of humans into zombies upon encounters. This document provides an overview of the core components, functionalities, and the workflow of the simulation.

#### Core Components

1. **Configuration (`config.py`):** Defines the simulation parameters such as grid dimensions, the number of epochs, simulation days, and parameters for generating the noise map which models the terrain of the simulation environment.

2. **Surface Noise (`surface_noise.py`):** Utilizes Perlin noise to generate a 2D grid representing the terrain. This terrain influences the movement and interactions within the simulation, with parameters defined in the configuration.

3. **Classes (`classes.py`):** Contains the essential classes for the simulation, including:
   - `DayTracker` and `Epoch` for tracking the simulation's temporal aspects.
   - `Being` to represent individual agents (humans and zombies) with specific attributes like position, resources, and experience.
   - `Grid` which sets up the environment where agents interact, including resource points, and facilitates movement and encounters.
   - Logging classes (`EncounterLog`, `ResourceLog`, `MovementLog`) for recording events, movements, and resource changes.

4. **Mapping (`mapping.py`):** Provides functionality to generate heatmaps based on encounter locations and types, visualizing the hotspots of activity within the simulation environment.

5. **Analysis (`analysis.py`):** Tools for extracting and analyzing data from the simulation logs, including temporal data extraction, encounter data processing, and resource data analysis.

6. **Simulation Runner (`sim.py`):** Orchestrates the simulation, initializing the environment, running the simulation for a set number of days, and computing metrics based on agent interactions and movements.

7. **Main CSV (`__main__csv.py`):** Serves as the entry point for running the simulation, exporting results to CSV, generating heatmaps, and performing post-simulation analysis such as logistic regression on encounter types.

#### Workflow

1. **Initialization:**
   - The simulation environment is set up based on the configurations specified in `config.py`.
   - Terrain is generated using Perlin noise in `surface_noise.py`, influencing agent movement and interactions.

2. **Simulation Execution:**
   - Agents (humans and zombies) are placed in the grid environment.
   - Daily simulation activities include agent movements, encounters, and resource consumption, managed by the `Grid` and `Being` classes in `classes.py`.
   - Encounters between agents can result in transformations (humans turning into zombies) and resource exchanges.
   - Events, movements, and resource changes are logged for analysis.

3. **Post-Simulation Analysis:**
   - `analysis.py` and `mapping.py` provide tools for extracting data from logs and generating visual representations such as heatmaps.
   - The main script (`__main__csv.py`) collates results, exports data, and performs additional analyses like logistic regression on encounter outcomes.

4. **Metrics and Visualization:**
   - The simulation tracks various metrics such as the number of active humans and zombies, resource levels, and the distribution of encounters.
   - Visualizations include heatmaps of encounter locations and terrain maps with resource points.

#### Usage

To run the simulation, execute the `__main__csv.py` script. Adjust parameters in `config.py` as needed to explore different scenarios or terrain configurations. Use `analysis.py` and `mapping.py` for detailed data analysis and visualization of simulation outcomes.

---
