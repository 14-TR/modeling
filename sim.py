#########################################################
"""

Title: sim.py
Author: TR Ingram
Description:

This script sets up a zombie apocalypse simulation using agent-based modeling. It defines classes for tracking
simulation days (`DayTracker`), running multiple simulations (`Epoch`), characterizing agents (`Being`), and managing
the simulation grid (`Grid`). The `run_simulation` function populates the grid with humans and zombies, simulates their
interactions over specified days, and calculates key metrics such as resource levels and encounter outcomes.

The `calculate_metrics` function extracts and analyzes specific attributes from the agents. Finally,
`write_log_to_dataframe` compiles all event logs into a structured pandas DataFrame for analysis,
capturing detailed records of the simulation's events.

"""
#########################################################

import random
import pandas as pd

from classes import Being, Grid, DayTracker, EncounterLog, MovementLog, ResourceLog
from config import W, H


def calculate_metrics(grid, attribute_name):
    values = [getattr(being, attribute_name, None) for being in grid.beings]
    # Filter out None values which represent missing attributes
    values = [value for value in values if value is not None]

    if not values:  # If the list is empty, return None for all metrics
        return None, None, None

    max_value = max(values)
    min_value = min(values)
    avg_value = sum(values) / len(values)
    n_value = sum(values)

    return max_value, min_value, avg_value, n_value


def run_simulation(num_days, num_humans, num_zombies, surf, resource_points):
    # resource_points = Grid.generate_resource_points(W, H, num_points=4)  # Define this function to generate points

    grid = Grid(width=W, height=H, resource_points=resource_points)
    grid.append_surface(surf)
    # Add humans
    for _ in range(num_humans):
        x, y = random.randint(0, grid.width - 1), random.randint(0, grid.height - 1)
        z = grid.get_elev_at(x, y)
        human = Being(resources=random.randint(10, 20), x=x, y=y, z=z)
        grid.add_being(human)

    # Add zombies
    for _ in range(num_zombies):
        x, y = random.randint(0, grid.width - 1), random.randint(0, grid.height - 1)
        z = grid.get_elev_at(x, y)
        zombie = Being(resources=random.randint(1, 10), x=x, y=y, z=z, is_zombie=True)
        grid.add_being(zombie)

    days_until_all_zombies = None

    # Runs sim for spec # of days
    for day in range(1, num_days + 1):
        grid.simulate_day()
        grid.remove_inactive_beings()
        humans, zombies = grid.count_humans_and_zombies()
        DayTracker.increment_day()

        if humans == 0 and days_until_all_zombies is None:
            days_until_all_zombies = day
            break

    # get the number of humans and zombies that are not active
    humans, zombies = grid.count_humans_and_zombies()
    full_dead = (num_humans + num_zombies) - (humans + zombies)

    # Calculate metrics for the simulation

    metrics = {}
    attr_list = [
        # "lifespan_h",
        # "lifespan_z",
        "resources",
        "esc_xp",
        "win_xp",
        "love_xp",
        "war_xp",
        "theft",
        "zh_kd",
        "hh_kd",
        # "hz_kd",
        "z_enc",
        "h_enc"
    ]

    for item in attr_list:
        max_value, min_value, avg_value, n_value = calculate_metrics(grid, item)
        metrics[f'max_{item}'] = max_value
        metrics[f'min_{item}'] = min_value
        metrics[f'mean_{item}'] = avg_value
        metrics[f'count_{item}'] = n_value

    metrics['days_until_all_zombies'] = days_until_all_zombies if days_until_all_zombies is not None else num_days
    metrics['humans'] = humans
    metrics['zombies'] = zombies
    metrics['full_dead'] = full_dead

    return metrics


def encounters_to_dataframe(encounter_log):
    data = [{
        'Epoch': record.epoch,
        'Day': record.day,
        'Being ID': record.being_id,
        'Other Being ID': record.other_being_id,
        'Encounter Type': record.encounter_type,  # Ensure this line correctly references the attribute
        'X': record.x,
        'Y': record.y,
        'Z': record.z
    } for record in encounter_log.records]
    df = pd.DataFrame(data)
    # If you're renaming columns, ensure it's done correctly
    df.rename(columns={'Encounter Type': 'encounter_type'}, inplace=True)
    return df



def resources_to_dataframe(resource_log):
    data = [{
        'Epoch': record.epoch,
        'Day': record.day,
        'Being ID': record.being_id,
        'Resource Change': record.resource_change,
        'Current Resources': record.current_resources,
        'Reason': record.reason
    } for record in resource_log.records]
    return pd.DataFrame(data)


def movements_to_dataframe(movement_log):
    data = [{
        'Epoch': record.epoch,
        'Day': record.day,
        'Being ID': record.being_id,
        'Start X': record.start_x,
        'Start Y': record.start_y,
        'End X': record.end_x,
        'End Y': record.end_y
    } for record in movement_log.records]
    return pd.DataFrame(data)


def write_logs_to_dataframes():
    encounter_df = encounters_to_dataframe(EncounterLog())
    resource_df = resources_to_dataframe(ResourceLog())
    movement_df = movements_to_dataframe(MovementLog())

    # Optionally, you can merge these DataFrames into one for unified analysis This step depends on how you plan to
    # analyze the data and whether you need them combined or separate Example of a simple concatenation (make sure
    # your records have a way to be distinguished, e.g., by adding a 'Log Type' column to each DataFrame before
    # concatenation)

    # Add 'Log Type' columns to distinguish between logs
    encounter_df['Log Type'] = 'Encounter'
    resource_df['Log Type'] = 'Resource'
    movement_df['Log Type'] = 'Movement'

    combined_df = pd.concat([encounter_df, resource_df, movement_df], ignore_index=True)

    return encounter_df, resource_df, movement_df, combined_df  # Return individual and combined DataFrames


# selct movements of huumans reference the being id and the is zombie attribute
def extract_movement_human(logs):
    movement_data = []
    for record in logs.records:
        #use the get_is_zombie method to check if the being is a zombie
        if not record.being_id.get_is_zombie():
            movement_data.append((record.x, record.y))
    return movement_data


def extract_movement_zombie(logs):
    movement_data = []
    for record in logs.records:
        if record.being_id.get_is_zombie():
            movement_data.append((record.x, record.y))
    return movement_data


def extract_movement_data(logs):
    movement_data = []
    for record in logs.records:
        if record.event_type == "MOV":
            movement_data.append((record.x, record.y))
    return movement_data
