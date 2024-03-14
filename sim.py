from classes import Being, Grid
import random
import pandas as pd


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

    human_lifespans = []
    days_until_all_zombies = None

    # Run the simulation for the specified number of days
    for day in range(1, num_days + 1):
        grid.simulate_day()
        humans, zombies, full_dead = grid.count_humans_and_zombies()
        grid.remove_inactive_beings()
        # Update human lifespans
        for _ in range(humans):
            human_lifespans.append(day)

        if humans == 0 and days_until_all_zombies is None:
            days_until_all_zombies = day
            break  # Stop the simulation if there are no humans left

    # Calculate metrics at the end of the simulation
    # store the counts for humans and zombies at the end of the simulation
    humans, zombies, full_dead = grid.count_humans_and_zombies()

    # Mean human and zombie lifespans and remaining resources held by humans
    mean_human_lifespan = sum(human_lifespans) / num_humans if human_lifespans else 0
    mean_zombie_lifespan = sum(being.lifespan for being in grid.beings if being.is_zombie) / num_zombies if zombies else 0
    mean_resources = sum(being.resources for being in grid.beings) / (num_humans + num_zombies)

    max_human_lifespan = max(human_lifespans) if human_lifespans else 0
    min_human_lifespan = min(human_lifespans) if human_lifespans else 0

    zombie_lifespans = [being.lifespan for being in grid.beings if being.is_zombie]
    max_zombie_lifespan = max(zombie_lifespans) if zombie_lifespans else 0
    min_zombie_lifespan = min(zombie_lifespans) if zombie_lifespans else 0

    # Handle the case where not all humans turned into zombies by the end of the simulation
    if days_until_all_zombies is None:
        days_until_all_zombies = num_days  # or another appropriate value

    mean_days_until_all_zombies = days_until_all_zombies / num_days

    mean_love_xp = sum(being.love_xp for being in grid.beings) / (num_humans + num_zombies)
    mean_war_xp = sum(being.war_xp for being in grid.beings) / (num_humans + num_zombies)
    mean_esc_xp = sum(being.esc_xp for being in grid.beings) / (num_humans + num_zombies)
    mean_win_xp = sum(being.win_xp for being in grid.beings) / (num_humans + num_zombies)
    mean_zh_kills = sum(being.zh_kd for being in grid.beings) / (num_humans + num_zombies)
    mean_hh_kills = sum(being.hh_kd for being in grid.beings) / (num_humans + num_zombies)
    mean_hz_kills = sum(being.hz_kd for being in grid.beings) / (num_humans + num_zombies)

    return (days_until_all_zombies,
            mean_resources,
            mean_human_lifespan,
            mean_zombie_lifespan,
            max_human_lifespan,
            max_zombie_lifespan,
            min_human_lifespan,
            min_zombie_lifespan,
            mean_days_until_all_zombies,
            humans, zombies,
            mean_love_xp,
            mean_war_xp,
            mean_esc_xp,
            mean_win_xp,
            full_dead,
            mean_zh_kills,
            mean_hh_kills,
            mean_hz_kills)


# Run 50 simulations
results = [run_simulation(30, 50, 5) for _ in range(384)]

# Convert results to a DataFrame and save to CSV
df = pd.DataFrame(results, columns=['days_until_all_zombies',
                                    'mean_resources',
                                    'mean_human_lifespan',
                                    'mean_zombie_lifespan',
                                    'max_human_lifespan',
                                    'max_zombie_lifespan',
                                    'min_human_lifespan',
                                    'min_zombie_lifespan',
                                    'mean_days_until_all_zombies',
                                    'mean_love_xp',
                                    'mean_war_xp',
                                    'mean_escape_xp',
                                    'mean_win_xp',
                                    'humans',
                                    'zombies',
                                    'full_dead',
                                    'mean_zh_kills',
                                    'mean_hh_kills',
                                    'mean_hz_kills'])
df.to_csv(r'C:\Users\tingram\Desktop\Captains Log\UWYO\GIT\modeling\metrics_v1\simulation_results.csv', index=False)



