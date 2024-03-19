import numpy as np
import matplotlib.pyplot as plt
from classes import Log


def collect_event_locations(event_type):
    log_instance = Log()  # Assuming you have a Log instance
    event_records = log_instance.get_records_by_type(event_type)
    locations = [(record.x, record.y) for record in event_records]  # Collecting locations from records
    return locations


def generate_heatmap(locations):
    grid_size = 100  # Assuming your grid is of a fixed size
    heatmap_matrix = np.zeros((grid_size, grid_size))

    for x, y in locations:
        heatmap_matrix[x, y] += 1  # Increment count for the location

    # Create and return the heatmap image, don't show it yet
    img = plt.imshow(heatmap_matrix, cmap='hot', interpolation='nearest')
    return img



