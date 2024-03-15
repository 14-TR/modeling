from classes import Being, Grid
import random


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

def run_simulation(num_days, num_humans, num_zombies):

    grid = Grid(width=20, height=20)  # Adjust grid size as needed

    # Add humans
    for _ in range(num_humans):
        x, y = random.randint(0, grid.width - 1), random.randint(0, grid.height - 1)
        human = Being(resources=random.randint(1, 10), x=x, y=y)
        grid.add_being(human)

    # Add zombies
    for _ in range(num_zombies):
        x, y = random.randint(0, grid.width - 1), random.randint(0, grid.height - 1)
        zombie = Being(resources=random.randint(1, 10), x=x, y=y, is_zombie=True)
        grid.add_being(zombie)

    days_until_all_zombies = None

    # Run the simulation for the specified number of days
    for day in range(1, num_days + 1):
        grid.simulate_day()
        grid.remove_inactive_beings()
        humans, zombies = grid.count_humans_and_zombies()

        if humans == 0 and days_until_all_zombies is None:
            days_until_all_zombies = day
            break


    #get the number of humans and zombies that are not active
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

    # Add other metrics like 'days_until_all_zombies', 'humans', 'zombies', 'full_dead' to the metrics dictionary
    metrics['days_until_all_zombies'] = days_until_all_zombies if days_until_all_zombies is not None else num_days
    metrics['humans'] = humans
    metrics['zombies'] = zombies
    metrics['full_dead'] = full_dead

    return metrics



