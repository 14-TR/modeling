import numpy as np
import matplotlib.pyplot as plt
from classes import Log
from config import W


def collect_event_locations(event_type):
    log_instance = Log()  # Assuming you have a Log instance
    event_records = log_instance.get_records_by_type(event_type)
    locations = [(record.x, record.y) for record in event_records]  # Collecting locations from records
    return locations


def generate_heatmap(locations):
    grid_size = W  # Assuming your grid is of a fixed size
    heatmap_matrix = np.zeros((grid_size, grid_size))

    for x, y in locations:
        heatmap_matrix[x, y] += 1  # Increment count for the location

    # Create and return the heatmap image, don't show it yet
    img = plt.imshow(heatmap_matrix, cmap='viridis', interpolation='lanczos')
    return img


# select Movement heat map cells by corresponding elevation cells of a particular value
def select_cells(elevation, movement, value):
    cells = []
    for i in range(W):
        for j in range(W):
            if elevation[i][j] == value:
                cells.append((i, j))
    return cells


