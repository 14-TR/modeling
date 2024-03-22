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
import datetime
import os

import matplotlib.pyplot as plt
import pandas as pd

from classes import Epoch, DayTracker, EncounterLog, ResourceLog, MovementLog, Grid
from config import W, H, eps, vi, vj, z, num_humans, num_zombies, days
from mapping import generate_heatmap
#########################################################
# imports
from sim import run_simulation, encounters_to_dataframe, movements_to_dataframe, resources_to_dataframe, \
    extract_movement_human
from surface_noise import generate_noise

timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
output_folder = f"C:\\Users\\TR\\Desktop\\z\\GIT\\modeling\\sims\\sim__{timestamp}__N{eps}"
# output_folder = f"C:\\Users\\tingram\\Desktop\\Captains Log\\UWYO\\GIT\\sims\\sim__{timestamp}__N{eps}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def main():
    results = []
    Epoch.epoch = 0
    surf = generate_noise(W, H, vi, vj, z)

    for _ in range(eps):  # For each simulation epoch
        Epoch.increment_sim()
        DayTracker.reset()  # Reset the day tracker

        grid = Grid(width=W, height=H)
        grid.append_surface(surf)

        # Generate resource points for this simulation run
        # Using the instance of Grid to call the method
        resource_points = grid.generate_resource_points(num_points=4)

        # Run the simulation with the generated surface and resource points
        simulation_result = run_simulation(days, num_humans, num_zombies, surf, resource_points)
        results.append(simulation_result)

        results_csv_path = os.path.join(output_folder, 'simulation_results.csv')
        enc_csv_path = os.path.join(output_folder, 'enc_log.csv')
        mov_csv_path = os.path.join(output_folder, 'mov_log.csv')
        res_csv_path = os.path.join(output_folder, 'res_log.csv')

        met_df = pd.DataFrame(results)
        met_df.to_csv(results_csv_path, index=False)

        # logs
        enc_log_instance = EncounterLog()
        mov_log_instance = MovementLog()
        res_log_instance = ResourceLog()

        # logs to dfs
        enc_df = encounters_to_dataframe(enc_log_instance)
        if 'Encounter Type' in enc_df.columns:
            # Filter rows where 'Encounter Type' is 'INF'
            inf_encounters = enc_df[enc_df['Encounter Type'] == 'INF']

            # Count the number of 'INF' encounters
            num_inf_encounters = inf_encounters.shape[0]

            # If you want to visualize the count as a bar chart
            encounter_counts = enc_df['Encounter Type'].value_counts()
            encounter_counts.plot(kind='bar')
            plt.xlabel('Encounter Type')
            plt.ylabel('Count')
            plt.title('Encounter Types Distribution')
            plt.show()
        else:
            print("Encounter Type column not found in the DataFrame.")
        mov_df = movements_to_dataframe(mov_log_instance)
        res_df = resources_to_dataframe(res_log_instance)

        # log dfs to csv
        enc_df.to_csv(enc_csv_path, index=False)
        mov_df.to_csv(mov_csv_path, index=False)
        res_df.to_csv(res_csv_path, index=False)

        # Plotting the elevation surface (2D Perlin Noise)
        plt.imshow(surf, cmap='terrain')
        plt.colorbar()
        plt.title('2D Perlin Noise')

        # Save the elevation surface plot to the new folder
        elevation_surface_filename = "elevation_surface.png"
        plt.savefig(os.path.join(output_folder, elevation_surface_filename))

        # map clustering encounters by type
        encounter_counts = enc_df['INF'].value_counts()
        encounter_counts.plot(kind='bar')
        plt.xlabel('Encounter Type')
        plt.ylabel('Count')
        plt.title('Encounter Types Distribution')
        encounter_counts_filename = "encounter_counts.png"
        plt.savefig(os.path.join(output_folder, encounter_counts_filename))

        # #--------------------------------------------
        # #--------------------------------------------
        # #heatmap clustering encounters by type "INF",   "ESC",   "WIN",   "WAR",   "LUV", "STL
        # inf_encounters = extract_encounter_data(enc_log_instance, 'INF')
        # inf_heatmap = generate_heatmap(inf_encounters, x_attr='x', y_attr='y')
        # inf_heatmap_filename = "inf_heatmap.png"
        # plt.savefig(os.path.join(output_folder, inf_heatmap_filename))
        #
        # esc_encounters = extract_encounter_data(enc_log_instance, 'ESC')
        # esc_heatmap = generate_heatmap(esc_encounters, x_attr='x', y_attr='y')
        # esc_heatmap_filename = "esc_heatmap.png"
        # plt.savefig(os.path.join(output_folder, esc_heatmap_filename))
        #
        # win_encounters = extract_encounter_data(enc_log_instance, 'WIN')
        # win_heatmap = generate_heatmap(win_encounters, x_attr='x', y_attr='y')
        # win_heatmap_filename = "win_heatmap.png"
        # plt.savefig(os.path.join(output_folder, win_heatmap_filename))
        #
        # war_encounters = extract_encounter_data(enc_log_instance, 'WAR')
        # war_heatmap = generate_heatmap(war_encounters, x_attr='x', y_attr='y')
        # war_heatmap_filename = "war_heatmap.png"
        # plt.savefig(os.path.join(output_folder, war_heatmap_filename))
        #
        # luv_encounters = extract_encounter_data(enc_log_instance, 'LUV')
        # luv_heatmap = generate_heatmap(luv_encounters, x_attr='x', y_attr='y')
        # luv_heatmap_filename = "luv_heatmap.png"
        # plt.savefig(os.path.join(output_folder, luv_heatmap_filename))
        #
        # stl_encounters = extract_encounter_data(enc_log_instance, 'STL')
        # stl_heatmap = generate_heatmap(stl_encounters, x_attr='x', y_attr='y')
        # stl_heatmap_filename = "stl_heatmap.png"
        # plt.savefig(os.path.join(output_folder, stl_heatmap_filename))
        # #--------------------------------------------
        # #--------------------------------------------
        #
        #
        # #make a map of all human movements
        # human_movements = extract_movement_human(mov_log_instance)
        # human_movement_heatmap = generate_heatmap(human_movements)
        # human_movement_heatmap_filename = "human_movement_heatmap.png"
        # plt.savefig(os.path.join(output_folder, human_movement_heatmap_filename))

        # make a map of all zombie movements
        zombie_movements = extract_movement_human(mov_log_instance)
        zombie_movement_heatmap = generate_heatmap(zombie_movements)
        zombie_movement_heatmap_filename = "zombie_movement_heatmap.png"
        plt.savefig(os.path.join(output_folder, zombie_movement_heatmap_filename))


if __name__ == "__main__":
    main()
