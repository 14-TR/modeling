import pandas as pd
import matplotlib.pyplot as plt

from analysis import extract_resource_data, extract_encounter_data
from classes import ResourceLog  # Assuming ResourceLog is properly implemented
from config import W, H
from sim import run_simulation
from surface_noise import generate_noise

# Run the simulation
surf = generate_noise(W, H, 0.1, 0.1, 1)  # Example surface noise parameters
simulation_result = run_simulation(365, 100, 5, surf)


def calculate_daily_average_resources(resource_df):
    # Grouping by day and calculating the average of 'Current Resources'
    avg_res_daily = resource_df.groupby('Day')['Current Resources'].mean().reset_index()
    return avg_res_daily


def plot_daily_average_resources(daily_avg_resources):
    plt.figure(figsize=(10, 6))
    plt.plot(daily_avg_resources['Day'], daily_avg_resources['Current Resources'], marker='o')
    plt.title('Average Resource Levels Over Time')
    plt.xlabel('Day')
    plt.ylabel('Average Resources')
    plt.grid(True)
    plt.show()


res_log_instance = ResourceLog()

res_data_df = extract_resource_data(res_log_instance)

print(res_data_df.columns)

avg_res = calculate_daily_average_resources(res_data_df)
plot_daily_average_resources(avg_res)
