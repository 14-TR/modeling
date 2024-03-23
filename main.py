import random
import pandas as pd
from environment import Grid
from entities import Human, Zombie
from config import W, H, vi, vj, Z, num_humans, num_zombies, days
from logs import Log
from surface_noise import generate_noise


def setup_environment():
    log_instance = Log()
    elevation_data = generate_noise(W, H, vi, vj, Z)
    grid = Grid(width=W, height=H, elevation_data=elevation_data)

    humans = []
    for _ in range(num_humans):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        z = grid.get_elevation_at(x, y)  # Get z from the grid
        human = Human(x=x, y=y, z=z, grid=grid)
        humans.append(human)
        grid.add_entity(human)

    zombies = []
    for _ in range(num_zombies):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        z = grid.get_elevation_at(x, y)
        zombie = Zombie(x=x, y=y, z=z, grid=grid)
        zombies.append(zombie)
        grid.add_entity(zombie)

    for human in humans:
        grid.add_entity(human)
        human.set_log_instance(log_instance)
    for zombie in zombies:
        grid.add_entity(zombie)
        zombie.set_log_instance(log_instance)

    return grid


def run_simulation(grid, num_days):
    for day in range(1, num_days + 1):
        grid.simulate_day()
        # You can log daily metrics or events here if needed


def output_to_csv(df, filename):
    df.to_csv(filename, index=False)


def main():
    grid = setup_environment()
    run_simulation(grid, days)

    # Assuming your logs are stored in grid.log
    encounter_df, resource_df, movement_df, combined_df = grid.log.write_logs_to_dataframes()

    # Output to CSV
    output_to_csv(encounter_df, "encounter_logs.csv")
    output_to_csv(resource_df, "resource_logs.csv")
    output_to_csv(movement_df, "movement_logs.csv")
    output_to_csv(combined_df, "combined_logs.csv")


if __name__ == "__main__":
    main()
