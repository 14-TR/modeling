
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
### `config.py` - Configuration Script

#### Overview
The `config.py` script sets the foundational parameters for the zombie outbreak simulation. It defines the dimensions of the grid environment, the number of simulation epochs, the duration in days for each epoch, and the initial number of humans and zombies. Additionally, it configures the parameters for generating the terrain's noise map, which influences agent movement and interactions.

#### Key Parameters
- `W`, `H`: Width and height of the grid environment, defining its size.
- `EPS`: Number of epochs or simulation runs to be executed.
- `days`: Duration of each simulation run, in days.
- `num_humans`, `num_zombies`: Initial count of human and zombie agents in the simulation.
- `vi`, `vj`, `z`: Parameters for the Perlin noise function, controlling the variability and scale of the terrain's elevation.

#### Usage
Adjust the parameters in this script to modify the simulation's scale, duration, and the complexity of the terrain. These settings directly impact the dynamics of agent interactions and the overall progression of the simulated zombie outbreak.

---
### `surface_noise.py` - Terrain Generation Script

#### Overview
The `surface_noise.py` script is responsible for generating a 2D grid that represents the terrain of the simulation environment using Perlin noise. This noise map introduces variability in elevation across the grid, which influences agent movements and interactions. Higher terrain can represent obstacles or strategic advantages, impacting the dynamics between humans and zombies.

#### Key Functions
- `generate_noise(w, h, vi, vj, z)`: Generates a grid of size `w` by `h` filled with Perlin noise values. The `vi`, `vj`, and `z` parameters control the scale and intensity of the noise, affecting the terrain's elevation and variability. The function returns a 2D NumPy array representing the noise map.

#### Dependencies
- `perlin`: A Python module that generates Perlin noise. It is used to create the elevation variations across the grid.
- `numpy`: Utilized for creating and manipulating the 2D grid array.
- `matplotlib.pyplot`: Though commented out in the provided code, it can be used for visualizing the generated terrain as a 2D plot for analysis and debugging purposes.

#### Usage
This script is typically called by other components of the simulation (e.g., during the initialization phase) to create the terrain on which the agents will interact. The `generate_noise` function can be customized or extended to introduce different types of terrain or to simulate environmental changes over time.

---
### `classes.py` - Core Simulation Entities and Logic

#### Overview
The `classes.py` script defines the essential classes and structures used in the simulation, including the representation of time (`DayTracker` and `Epoch`), agents (`Being`), the simulation grid (`Grid`), and various logging classes for recording simulation events.

#### Key Classes and Their Functions

- **DayTracker**: Manages the simulation's current day, providing methods to increment the day, get the current day, and reset the day count for a new simulation run.

- **Epoch**: Tracks the current epoch (simulation run) and offers methods to increment the epoch count, retrieve the current epoch, and reset for subsequent runs.

- **Being**: Represents an individual agent in the simulation, either a human or a zombie. It includes attributes for position, resources, experience in different skills, lifespan, and status (human or zombie). Key methods include movement logic (`move` and `move_towards_resource_point`), encounter handling (`encounter`, `encounter_as_zombie`, `encounter_zombie`, `encounter_human`), and status updates (`update_status`).

- **Grid**: Defines the simulation environment as a grid where agents are placed and interact. It includes methods for adding beings, moving beings, simulating daily activities (`simulate_day`), removing inactive beings, and counting the number of humans and zombies. The grid also handles the generation and management of resource points and the integration of terrain elevation data.

- **EncounterRecord & EncounterLog**: Used for logging encounter events between beings, capturing details like the epoch, day, involved agents, encounter type, and location. `EncounterLog` provides functionality to add records and retrieve records based on day or type.

- **ResourceRecord & ResourceLog**: Focus on logging resource-related events, such as consumption or gains due to encounters. These classes capture and allow retrieval of resource change events, detailing the involved agent, the change in resources, and the reason for the change.

- **MovementRecord & MovementLog**: Log the movement of agents within the grid, documenting the start and end positions of movements, and allowing the retrieval of movement records by day.

#### Usage
The `classes.py` script forms the backbone of the simulation, with other components relying on these definitions to simulate agent interactions and the progression of the zombie outbreak. Customization can be done to these classes to introduce new behaviors, modify agent interactions, or change how the environment influences the agents.

---
### `mapping.py` - Visualization and Analysis Tools

#### Overview
The `mapping.py` script provides utilities for visualizing simulation data, particularly the spatial aspects such as the locations of encounters. It facilitates the generation of heatmaps to identify hotspots of activity within the simulation grid, helping to analyze patterns and outcomes of agent interactions.

#### Key Functions

- **collect_enc_locations(event_type)**: Collects the locations of specific encounter types (e.g., human-zombie encounters) from the simulation's encounter log. It returns a list of coordinates representing the locations where the specified encounters occurred.

- **generate_heatmap(locations, x_attr='x', y_attr='y')**: Generates a heatmap based on a list of locations. This function initializes a grid based on the simulation's dimensions and increments grid cells' values based on the occurrences of events at those locations. The resulting heatmap is displayed using `matplotlib`, highlighting areas of high activity.

- **generate_heatmap_by_enc_type(locations, x_attr, y_attr)**: Similar to `generate_heatmap`, but tailored for processing encounter locations and visualizing them as a heatmap, focusing on specific encounter types if needed.

- **generate_heatmap_from_df(enc_df, dx='X', dy='Y')**: Generates a heatmap directly from a DataFrame that contains encounter data, utilizing specified columns for the x and y coordinates. This function is useful for creating visualizations from data that has been processed and stored in pandas DataFrames.

#### Dependencies
- `numpy`: Used for creating and manipulating the grid that serves as the basis for the heatmap.
- `matplotlib.pyplot`: Utilized for visualizing the heatmap, allowing for the analysis of spatial patterns in the simulation data.

#### Usage
This script is instrumental in the post-simulation analysis phase, where visual insights into the simulation's dynamics are required. By generating heatmaps of encounters or other events, researchers and analysts can visually assess patterns, such as preferred habitats, conflict zones, or resource-rich areas within the simulation environment.

---

### `mapping.py` - Visualization and Analysis Tools

#### Overview
The `mapping.py` script provides utilities for visualizing simulation data, particularly the spatial aspects such as the locations of encounters. It facilitates the generation of heatmaps to identify hotspots of activity within the simulation grid, helping to analyze patterns and outcomes of agent interactions.

#### Key Functions

- **collect_enc_locations(event_type)**: Collects the locations of specific encounter types (e.g., human-zombie encounters) from the simulation's encounter log. It returns a list of coordinates representing the locations where the specified encounters occurred.

- **generate_heatmap(locations, x_attr='x', y_attr='y')**: Generates a heatmap based on a list of locations. This function initializes a grid based on the simulation's dimensions and increments grid cells' values based on the occurrences of events at those locations. The resulting heatmap is displayed using `matplotlib`, highlighting areas of high activity.

- **generate_heatmap_by_enc_type(locations, x_attr, y_attr)**: Similar to `generate_heatmap`, but tailored for processing encounter locations and visualizing them as a heatmap, focusing on specific encounter types if needed.

- **generate_heatmap_from_df(enc_df, dx='X', dy='Y')**: Generates a heatmap directly from a DataFrame that contains encounter data, utilizing specified columns for the x and y coordinates. This function is useful for creating visualizations from data that has been processed and stored in pandas DataFrames.

#### Dependencies
- `numpy`: Used for creating and manipulating the grid that serves as the basis for the heatmap.
- `matplotlib.pyplot`: Utilized for visualizing the heatmap, allowing for the analysis of spatial patterns in the simulation data.

#### Usage
This script is instrumental in the post-simulation analysis phase, where visual insights into the simulation's dynamics are required. By generating heatmaps of encounters or other events, researchers and analysts can visually assess patterns, such as preferred habitats, conflict zones, or resource-rich areas within the simulation environment.

---

### `analysis.py` - Data Extraction and Analysis

#### Overview
The `analysis.py` script is designed to extract meaningful insights from the simulation's logs, converting raw event data into structured, analyzable formats. It supports a range of functions for processing different types of data, such as encounters, resource changes, and movements, facilitating comprehensive analysis of the simulation outcomes.

#### Key Functions

- **extract_temporal_data(logs)**: Aggregates data from the logs on a day-to-day basis, summarizing the number of humans and zombies, their resources, and other attributes over time. This function helps in understanding the dynamics of the simulation across its duration.

- **extract_enc_data_from_df(df, encounter_type=None)**: Processes a pandas DataFrame containing encounter data, filtering by specific encounter types if needed. It's useful for analyzing specific interactions within the simulation, such as human-zombie encounters.

- **extract_encounter_data(logs, encounter_type=None)**: Similar to `extract_enc_data_from_df`, but operates directly on log objects. It extracts detailed information about encounters, including participants, types, and locations.

- **extract_resource_data(logs)**: Gathers data on resource changes from the resource logs, capturing information about consumption, acquisition, and the reasons behind these changes. This function is crucial for analyzing survival strategies and resource utilization within the simulation.

- **extract_movement_data(logs)**: Compiles data on agent movements from movement logs, detailing the start and end points of movements. This can reveal patterns in agent behavior, such as migration, avoidance, or clustering.

- **perform_dbscan_clustering(gdf, eps=50, min_samples=5)**: Applies DBSCAN clustering to geospatial data, identifying dense clusters of events or agents. This method can uncover areas of high activity or congregation, providing insights into the spatial dynamics of the simulation.

#### Dependencies
- `pandas`: Essential for data manipulation and analysis, enabling the transformation of log data into structured DataFrames.
- `geopandas`: Used for handling geospatial data, particularly useful when applying clustering algorithms to spatial event data.
- `sklearn`: Provides clustering algorithms like DBSCAN, aiding in the spatial analysis of simulation data.

#### Usage
This script is a powerful tool for post-simulation analysis, enabling researchers to dissect and understand the complex interactions and behaviors observed in the simulation. By converting logs into structured data and applying statistical and spatial analysis techniques, it's possible to derive insights into the factors influencing survival, resource distribution, and the spread of the zombie outbreak.

---

### `sim.py` - Simulation Execution Logic

#### Overview
The `sim.py` script orchestrates the running of the zombie outbreak simulation. It integrates the core components of the simulation, such as the grid environment, agents (humans and zombies), and the temporal tracking of days and epochs. This script is responsible for initializing the simulation, running it for a specified number of days, and calculating various metrics to assess the outcomes.

#### Key Functions

- **calculate_metrics(grid, attribute_name)**: Computes statistics for a specified attribute (e.g., resources, experience points) across all agents in the grid. This function helps in evaluating the overall state of the simulation, such as the average resources of humans or the total experience gained in encounters.

- **run_simulation(num_days, num_humans, num_zombies, surf, resource_points)**: The main function that sets up and runs the simulation for a given number of days. It initializes the grid with humans and zombies, simulates daily activities including movements and encounters, and tracks the progression of the outbreak. The function returns a dictionary of key metrics summarizing the simulation results.

- **encounters_to_dataframe(encounter_log)**: Converts encounter logs into a pandas DataFrame for easier analysis and visualization. This is useful for post-simulation analysis, allowing for detailed examination of encounter types, locations, and outcomes.

- **resources_to_dataframe(resource_log)**, **movements_to_dataframe(movement_log)**: Similar to `encounters_to_dataframe`, these functions transform resource and movement logs into DataFrames, facilitating the analysis of resource dynamics and agent movements throughout the simulation.

#### Usage
The `sim.py` script is typically invoked to run the simulation with specific parameters such as the number of agents, the duration of the simulation, and the terrain configuration. After the simulation concludes, the collected data can be analyzed using the provided functions to extract insights into the dynamics of the simulated zombie outbreak, including survival strategies, resource scarcity impacts, and hotspots of activity.

This script serves as the backbone of the simulation, integrating various components and managing the execution flow from initialization to the final analysis of results.

---
