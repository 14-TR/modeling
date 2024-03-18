import csv
from sim import run_simulation
from classes import DayTracker
from logger import Log  # Make sure to import the Log class
import pandas as pd

results = []
for _ in range(384):
    DayTracker.reset()  # Reset the day tracker at the start of each simulation
    simulation_result = run_simulation(365, 50, 5)  # Run the simulation
    results.append(simulation_result)  # Collect the results

# Convert the results to a DataFrame and save to CSV
results_csv_path = r'C:\Users\TR\Desktop\z\GIT\modeling\metrics_v1\simulation_results.csv'
df = pd.DataFrame(results)
df.to_csv(results_csv_path, index=False)

# Access the singleton instance of Log to get all recorded events
log_instance = Log()

# Define the path for the simulation log CSV, ensuring it's in the same folder as the results CSV
log_csv_path = r'C:\Users\TR\Desktop\z\GIT\modeling\metrics_v1\simulation_log.csv'

# Write all recorded events to the simulation log CSV file
with open(log_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Day','Being ID', 'Event Type', 'Description'])

    # Write each log record
    for record in log_instance.records:
        writer.writerow([record.day, record.event_type, record.description])
