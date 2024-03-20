#########################################################
"""
Title: __main__.py
Author: TR Ingram
Description:

This script conducts an agent-based simulation to explore the interactions between humans and zombies in a grid-based
environment. It leverages classes such as `Being` for actors, `Grid` for the environment, `DayTracker` for time
progression, and `Log` for event recording.

The `calculate_metrics` function extracts and computes statistics (max, min, average, total) for specific attributes
from all beings in the grid. The `run_simulation` function initializes the grid with humans and zombies,
then simulates their interactions over a set number of days, tracking outcomes like encounters and resource changes.
It concludes by compiling key metrics from the simulation.

The `write_log_to_dataframe` function transforms the logged events into a pandas DataFrame for analysis, detailing
each event with attributes like epoch, day, being ID, and event type. This concise setup allows for a detailed
examination of the simulated pandemic dynamics and actor behaviors.

"""
#########################################################
# imports
from sim import run_simulation, write_log_to_dataframe
from classes import Epoch, DayTracker, Log
from mapping import collect_event_locations, generate_heatmap, select_cells
from surface_noise import generate_noise
import pandas as pd
import matplotlib.pyplot as plt
import os, datetime
from config import W, H, eps, vi, vj, z, num_humans, num_zombies, days


timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# output_folder = f"C:\\Users\\TR\\Desktop\\z\\GIT\\modeling\\sims\\sim__{timestamp}__N{eps}"
output_folder = f"C:\\Users\\tingram\\Desktop\\Captains Log\\UWYO\\GIT\\sims\\sim__{timestamp}__N{eps}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

results = []
Epoch.epoch = 0
surf = generate_noise(W, H, vi, vj, z)
for _ in range(eps): # 384 based on infinite sample
    Epoch.increment_sim()
    DayTracker.reset()  # Reset the day tracker at the start of each simulation
    simulation_result = run_simulation(days, num_humans, num_zombies, surf)  # Run
    results.append(simulation_result)

results_csv_path = os.path.join(output_folder, 'simulation_results.csv')
log_csv_path = os.path.join(output_folder, 'simulation_log.csv')

# results_csv_path = r'C:\Users\TR\Desktop\z\GIT\modeling\metrics_v1\simulation_results.csv'
# results_csv_path = r"C:\Users\tingram\Desktop\Captains Log\UWYO\GIT\modeling\metrics_v1\simulation_results.csv"
met_df = pd.DataFrame(results)
met_df.to_csv(results_csv_path, index=False)

log_instance = Log()

# log_csv_path = r'C:\Users\TR\Desktop\z\GIT\modeling\metrics_v1\simulation_log.csv'
# log_csv_path = r"C:\Users\tingram\Desktop\Captains Log\UWYO\GIT\modeling\metrics_v1\simulation_log.csv"
log_df = write_log_to_dataframe()
log_df.to_csv(log_csv_path, index=False)

# Plotting the elevation surface (2D Perlin Noise)
plt.imshow(surf, cmap='terrain')
plt.colorbar()
plt.title('2D Perlin Noise')

# Save the elevation surface plot to the new folder
elevation_surface_filename = "elevation_surface.png"
plt.savefig(os.path.join(output_folder, elevation_surface_filename))

plt.clf()

for event_type in ['LUV', 'STL', 'WIN', 'INF', 'WAR', 'MOV']:
    locations = collect_event_locations(event_type)
    plt.figure(figsize=(10, 8))
    img = generate_heatmap(locations)
    plt.title(f"Cumulative Heatmap for {event_type} Events")
    plt.colorbar(img)

    # Save each heatmap to the new folder
    heatmap_filename = f"{event_type}_heatmap.png"
    plt.savefig(os.path.join(output_folder, heatmap_filename))
    plt.clf()  # Clear the current figure after saving each heatmap

# print the movement heatmaps for each elvation breaking the range of all elevations into 5 classes
# and plotting the movement heatmaps for each class
#take the max elevation and min elevation and segment into 5 classes
elevations = surf
max_elev = elevations.max()
min_elev = elevations.min()
elev_range = max_elev - min_elev
elev_class = elev_range / 5
elevations = elevations.tolist()
elevation_classes = []
for i in range(W):
    elevation_classes.append([])
    for j in range(W):
        elevation_classes[i].append(int(elevations[i][j] / elev_class))

for i in range(5):
    cells = select_cells(elevation_classes, elevation_classes, i)
    plt.figure(figsize=(10, 8))
    img = generate_heatmap(cells)
    plt.title(f"Cumulative Heatmap for Movement in Elevation Class {i}")
    plt.colorbar(img)

    # Save each heatmap to the new folder
    heatmap_filename = f"elevation_class_{i}_heatmap.png"
    plt.savefig(os.path.join(output_folder, heatmap_filename))
    plt.clf()  # Clear the current figure after saving each heatmap

#print class values
print(min_elev, max_elev, elev_range, elev_class)