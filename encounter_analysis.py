import pandas as pd
import matplotlib.pyplot as plt

# Assuming extract_encounter_data function is adapted for EncounterLog
from analysis import extract_encounter_data
from classes import EncounterLog
from config import W, H
from sim import run_simulation
from surface_noise import generate_noise

# Run the simulation
surf = generate_noise(W, H, 0.1, 0.1, 1)  # Example surface noise parameters
simulation_result = run_simulation(365, 100, 5, surf)

# Directly use EncounterLog instance (Singleton pattern ensures it's the same instance used in the simulation)
encounter_log_instance = EncounterLog()
encounter_data = extract_encounter_data(encounter_log_instance)  # Updated to use EncounterLog instance

# Convert the encounter data to a DataFrame for easier analysis
encounter_df = pd.DataFrame(encounter_data)
print(encounter_df.columns)
print(encounter_df.head())


# Count encounters by type
encounter_counts = encounter_df['encounter_type'].value_counts()
print(encounter_counts)

# Calculate daily counts or proportions
daily_encounter_counts = encounter_df.groupby(['day', 'encounter_type']).size().unstack(fill_value=0)

# Assuming 'INF' indicates infections and is part of 'encounter_type' in EncounterRecord
infections_over_time = daily_encounter_counts.get('INF', pd.Series())  # Safe access in case 'INF' is not present

# Bar chart of encounter types
encounter_counts.plot(kind='bar')
plt.xlabel('Encounter Type')
plt.ylabel('Count')
plt.title('Encounter Types Distribution')
plt.show()

# Line plot of infections over time
infections_over_time.plot()
plt.xlabel('Day')
plt.ylabel('Infections')
plt.title('Infections Over Time')
plt.show()