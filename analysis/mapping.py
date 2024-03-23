import numpy as np
import matplotlib.pyplot as plt
from archive.classes import EncounterLog
from config import W, H


def collect_enc_locations(event_type):
    enc_log_instance = EncounterLog()  # Assuming you have a Log instance
    event_records = enc_log_instance.get_records_by_type(event_type)
    locations = [(record.x, record.y) for record in event_records]  # Collecting locations from records
    return locations


def generate_heatmap(locations, x_attr='x', y_attr='y'):
    # Initialize an empty grid for the heatmap
    heatmap_grid = np.zeros((H, W))  # Assuming H and W are the height and width of your grid

    # Iterate over the locations and increment the heatmap grid
    for location in locations:
        x = getattr(location, x_attr)
        y = getattr(location, y_attr)
        heatmap_grid[y, x] += 1  # Increment the count at the (x, y) location

    # Now, you can proceed to generate the heatmap visualization with heatmap_grid
    # For example, using matplotlib to display the heatmap
    plt.imshow(heatmap_grid, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.show()

    return heatmap_grid


def generate_heatmap_by_enc_type(locations, x_attr, y_attr):
    heatmap_grid = np.zeros((H, W))
    # Iterate over the locations and increment the heatmap grid
    for location in locations:
        x = getattr(location, x_attr)
        y = getattr(location, y_attr)
        heatmap_grid[y, x] += 1  # Increment the count at the (x, y) location

    return heatmap_grid


def generate_heatmap_from_df(enc_df, dx='X', dy='Y'):
    heatmap_grid = np.zeros((H, W))
    # Iterate over the locations and increment the heatmap grid
    for index, row in enc_df.iterrows():
        x = row[dx]
        y = row[dy]
        heatmap_grid[y, x] += 1  # Increment the count at the (x, y) location

    return heatmap_grid
