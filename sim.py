from classes import Being, Grid
import numpy as np

# Initialize the grid
grid = Grid(width=10, height=10)

# Create and add beings to the grid
being1 = Being(id=1, resources=np.random.uniform(3, 10), x=0, y=0)
being2 = Being(id=2, resources=np.random.uniform(3, 10), x=9, y=9)
grid.add_being(being1)
grid.add_being(being2)

# Simulate movements and encounters
days = 10
for day in range(days):
    grid.simulate_day()
    # Print beings' positions and states here
