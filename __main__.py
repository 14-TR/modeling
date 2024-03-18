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
from sim import run_simulation, write_log_to_dataframe
from classes import Epoch, DayTracker, Log
import pandas as pd

results = []
Epoch.epoch = 0
for _ in range(384): # 384 based on infinite sample
    Epoch.increment_sim()
    DayTracker.reset()  # Reset the day tracker at the start of each simulation
    simulation_result = run_simulation(365, 50, 5)  # Run
    results.append(simulation_result)


#outputs
results_csv_path = r'C:\Users\TR\Desktop\z\GIT\modeling\metrics_v1\simulation_results.csv'
met_df = pd.DataFrame(results)
met_df.to_csv(results_csv_path, index=False)

log_instance = Log()

log_csv_path = r'C:\Users\TR\Desktop\z\GIT\modeling\metrics_v1\simulation_log.csv'
log_df = write_log_to_dataframe()
log_df.to_csv(log_csv_path, index=False)


