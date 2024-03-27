from classes import Log  # Assuming Log class is in classes.py
# Import other necessary classes or functions
from classes import Log, Being, DayTracker, Epoch
from analysis import extract_temporal_data
from sim import run_simulation, write_log_to_dataframe
from config import W,H
from surface_noise import generate_noise
import pandas as pd
import matplotlib.pyplot as plt


# Example simulation run
surf = generate_noise(W, H, 0.1, 0.1, 1)  # Example surface noise parameters
simulation_result = run_simulation(30, 100, 50, surf)  # 30 days, 100 humans, 50 zombies
log_df = write_log_to_dataframe()


# Assuming log_df contains columns 'Day', 'Event Type', and 'Being ID' among others
daily_counts = log_df.groupby(['Day', 'Event Type']).size().unstack(fill_value=0)

# Example: Plotting the number of move events per day for humans and zombies
# This assumes 'MOV_HUMAN' and 'MOV_ZOMBIE' are event types logged for human and zombie movements
plt.figure(figsize=(12, 6))
plt.plot(daily_counts.index, daily_counts['MOV_HUMAN'], label='Human Movements')
plt.plot(daily_counts.index, daily_counts['MOV_ZOMBIE'], label='Zombie Movements')
plt.xlabel('Day')
plt.ylabel('Number of Movements')
plt.title('Daily Movements of Humans and Zombies')
plt.legend()
plt.show()

