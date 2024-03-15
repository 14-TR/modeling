from sim import run_simulation
import pandas as pd

results = [run_simulation(365, 50, 5) for _ in range(384)]
df = pd.DataFrame(results)

df.to_csv(r'C:\Users\tingram\Desktop\Captains Log\UWYO\GIT\modeling\metrics_v1\simulation_results.csv', index=False)
# df.to_csv(r'C:\Users\TR\Desktop\z\GIT\modeling\metrics_v1\simulation_results.csv', index=False)

# add number of humans with a h_kd and z_kd, add number of z with kd