import csv
from sim import run_simulation, write_log_to_dataframe
from classes import Epoch, DayTracker, Log # Make sure to import the Log class
import pandas as pd

results = []
Epoch.epoch = 0
for _ in range(384): # 384 based on infinite sample
    Epoch.increment_sim()
    DayTracker.reset()  # Reset the day tracker at the start of each simulation
    simulation_result = run_simulation(365, 50, 5)  # Run the simulation
    results.append(simulation_result)  # Collect the results

# Convert the results to a DataFrame and save to CSV
results_csv_path = r'C:\Users\TR\Desktop\z\GIT\modeling\metrics_v1\simulation_results.csv'
met_df = pd.DataFrame(results)
met_df.to_csv(results_csv_path, index=False)

# Access the singleton instance of Log to get all recorded events
log_instance = Log()

# Define the path for the simulation log CSV, ensuring it's in the same folder as the results CSV
log_csv_path = r'C:\Users\TR\Desktop\z\GIT\modeling\metrics_v1\simulation_log.csv'
log_df = write_log_to_dataframe()
log_df.to_csv(log_csv_path, index=False)

# Write all recorded events to the simulation log CSV file
# with open(log_csv_path, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     # Write the header
#     writer.writerow(['Epoch', 'Day', 'Being ID', 'Event Type', 'Description'])
#
#     # Write each log record
#     for record in log_instance.records:
#         writer.writerow([record.day, record.event_type, record.description])
