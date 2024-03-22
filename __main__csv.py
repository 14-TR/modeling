import datetime
import os

import pandas as pd

from analysis import extract_encounter_data
from classes import Epoch, DayTracker, Grid, MovementLog, EncounterLog, ResourceLog
from config import W, H, vi, vj, z, eps, days, num_humans, num_zombies
from sim import run_simulation, encounters_to_dataframe, movements_to_dataframe, resources_to_dataframe
from surface_noise import generate_noise


def main():
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_folder = f"./sims/sim__{timestamp}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Configuration for your simulation
    # W, H, eps, vi, vj, z, num_humans, num_zombies, days = 100, 100, 10, 0.1, 0.1, 1, 100, 50, 30

    results = []
    Epoch.epoch = 0
    surf = generate_noise(W, H, vi, vj, z)

    for _ in range(eps):
        Epoch.increment_sim()
        DayTracker.reset()

        grid = Grid(width=W, height=H)
        grid.append_surface(surf)

        resource_points = grid.generate_resource_points(num_points=4)
        simulation_result = run_simulation(days, num_humans, num_zombies, surf, resource_points)
        results.append(simulation_result)

    results_df = pd.DataFrame(results)
    results_csv_path = os.path.join(output_folder, 'simulation_results.csv')
    results_df.to_csv(results_csv_path, index=False)
    print(f"Simulation results saved to {results_csv_path}")

    # Export encounter logs to CSV
    enc_log_instance = EncounterLog()

    # Directly use the records from the encounter log instance if encounters_to_dataframe expects a list of dictionaries
    enc_df = encounters_to_dataframe(enc_log_instance)  # Assuming encounters_to_dataframe can handle this format

    enc_csv_path = os.path.join(output_folder, 'encounters.csv')
    enc_df.to_csv(enc_csv_path, index=False)
    print(f"Encounter logs saved to {enc_csv_path}")

    # Export movement logs to CSV
    mov_df = movements_to_dataframe(MovementLog())
    mov_csv_path = os.path.join(output_folder, 'movements.csv')
    mov_df.to_csv(mov_csv_path, index=False)
    print(f"Movement logs saved to {mov_csv_path}")

    # Export resource logs to CSV
    res_df = resources_to_dataframe(ResourceLog())
    res_csv_path = os.path.join(output_folder, 'resources.csv')
    res_df.to_csv(res_csv_path, index=False)
    print(f"Resource logs saved to {res_csv_path}")

if __name__ == "__main__":
    main()
