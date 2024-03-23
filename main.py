from datetime import datetime
import os
import random


from environment import Grid
from entities import Human, Zombie
from config import W, H, vi, vj, Z, num_humans, num_zombies, days
from logs import Log
from surface_noise import generate_noise
from utils import write_logs_to_dataframes


def setup_environment():
    log_instance = Log()
    elevation_data = generate_noise(W, H, vi, vj, Z)
    grid = Grid(width=W, height=H, elevation_data=elevation_data)

    # Initialize humans and zombies, set their log instance, and add them to the grid
    for _ in range(num_humans + num_zombies):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        z = grid.get_elevation_at(x, y)  # Get z from the grid
        if _ < num_humans:
            entity = Human(x=x, y=y, z=z, grid=grid)
        else:
            entity = Zombie(x=x, y=y, z=z, grid=grid)
        entity.set_log_instance(log_instance)
        grid.add_entity(entity)

    return grid


def run_simulation(grid, num_days):
    for day in range(1, num_days + 1):
        grid.simulate_day()
        # Logging daily metrics or events can be done here


def create_simulation_directory(base_path=r"C:\Users\TR\Desktop\z\GIT\sims"):
    # Create a base directory for simulations if it does not exist
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # Format the directory name with current date and time
    current_time = datetime.now().strftime("__%m%d%Y__%H%M%S")
    directory_name = f"sim{current_time}"
    full_path = os.path.join(base_path, directory_name)

    # Create the specific simulation directory
    os.makedirs(full_path)
    return full_path


def output_to_csv(df, filename, directory):
    path = os.path.join(directory, filename)
    df.to_csv(path, index=False)


def main():
    grid = setup_environment()
    run_simulation(grid, days)

    # Create a directory for this simulation run
    simulation_directory = create_simulation_directory()

    # Assuming your Log class's `write_logs_to_dataframes` method returns these dataframes
    log_instance = next(iter(grid.active_entities.values())).log
    encounter_df, resource_df, movement_df, combined_df = write_logs_to_dataframes(log_instance)

    # Output to CSV in the created directory
    output_to_csv(encounter_df, "encounter_logs.csv", simulation_directory)
    output_to_csv(resource_df, "resource_logs.csv", simulation_directory)
    output_to_csv(movement_df, "movement_logs.csv", simulation_directory)
    # output_to_csv(combined_df, "combined_logs.csv", simulation_directory)


if __name__ == "__main__":
    main()
