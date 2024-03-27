import datetime
import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from analysis import extract_enc_data_from_df
from classes import Epoch, DayTracker, Grid, MovementLog, EncounterLog, ResourceLog
from config import W, H, vi, vj, z, EPS, days, num_humans, num_zombies
from mapping import generate_heatmap_from_df
from modeling.group import GroupLog
from sim import run_simulation, encounters_to_dataframe, movements_to_dataframe, resources_to_dataframe, \
    groups_to_dataframe
from surface_noise import generate_noise


def main():
    global resource_points, grid
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_folder = f"C:/Users/tingram/Desktop/Captains Log/UWYO/GIT/sims/sim__{timestamp}"
    # output_folder = f"C:/Users/TR/Desktop/z/GIT/sims/sim__{timestamp}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Configure sim
    # W, H, EPS, vi, vj, z, num_humans, num_zombies, days = 100, 100, 10, 0.1, 0.1, 1, 100, 50, 30

    results = []
    Epoch.epoch = 0
    surf = generate_noise(W, H, vi, vj, z)

    for _ in range(EPS):
        Epoch.increment_sim()
        DayTracker.reset()

        grid = Grid(width=W, height=H)
        grid.append_surface(surf)

        resource_points = grid.generate_resource_points(num_points=4)
        simulation_result = run_simulation(days, num_humans, num_zombies, surf, resource_points)
        results.append(simulation_result)

    results_df = pd.DataFrame(results)
    results_csv_path = os.path.join(output_folder, 'simulation_results.csv')
    results_df.to_csv(results_csv_path, index=False)
    print(f"Simulation results saved to {results_csv_path}")

    # Export encounter logs to CSV
    enc_log_instance = EncounterLog()
    move_log_instance = MovementLog()
    res_log_instance = ResourceLog()
    grp_log_instance = GroupLog()

    # Directly use the records from the encounter log instance if encounters_to_dataframe expects a list of dictionaries
    enc_df = encounters_to_dataframe(enc_log_instance)  # Assuming encounters_to_dataframe can handle this format
    mov_df = movements_to_dataframe(move_log_instance)
    res_df = resources_to_dataframe(res_log_instance)
    grp_df = groups_to_dataframe(grp_log_instance)

    # print df header
    # print(enc_df.head())
    enc_csv_path = os.path.join(output_folder, 'encounters.csv')
    enc_df.to_csv(enc_csv_path, index=False)
    print(f"Encounter logs saved to {enc_csv_path}")

    mov_csv_path = os.path.join(output_folder, 'movements.csv')
    mov_df.to_csv(mov_csv_path, index=False)
    print(f"Movement logs saved to {mov_csv_path}")

    # Export resource logs to CSV
    res_csv_path = os.path.join(output_folder, 'resources.csv')
    res_df.to_csv(res_csv_path, index=False)
    print(f"Resource logs saved to {res_csv_path}")

    grp_csv_path = os.path.join(output_folder, 'groups.csv')
    grp_df.to_csv(grp_csv_path, index=False)
    print(f"Group logs saved to {grp_csv_path}")

    # plot heatmap of INF encounters

    inf_enc = extract_enc_data_from_df(enc_df, 'INF')
    inf_enc_df = pd.DataFrame(inf_enc)
    # print(inf_enc_df.head())

    # generate heatmap from dataframe and plot and save
    heatmap_grid = generate_heatmap_from_df(inf_enc_df, 'x', 'y')
    plt.imshow(heatmap_grid, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.savefig(os.path.join(output_folder, 'heatmap.png'))
    plt.show()

    resource_point_list = grid.get_xy_resource_points()
    resource_points_array = np.array(resource_point_list)

    # Plotting the elevation surface
    plt.imshow(surf, cmap='terrain', extent=[0.00, float(W), 0.00, float(H)], origin='lower')
    plt.colorbar(label='Elevation')

    # Plot resource points on the surface
    # Note: The 'extent' argument in plt.imshow() aligns the axes, making sure resource points are correctly placed
    plt.scatter(resource_points_array[:, 0], resource_points_array[:, 1], c='red', marker='x', label='Resource Points')

    plt.title('Elevation Surface with Resource Points')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()


    # Save the elevation surface plot to the new folder
    elevation_surface_filename = "elevation_surface.png"
    plt.savefig(os.path.join(output_folder, elevation_surface_filename))
    plt.show()



    # Load your data into a pandas DataFrame
    # enc_df = pd.read_csv('path_to_csv')

    # Encode the categorical 'Encounter Type' variable
    # Initialize the LabelEncoder
    label_encoder = LabelEncoder()

    # Fit the encoder to the 'Encounter Type' data and transform it to numerical
    enc_df['Encounter Type Encoded'] = label_encoder.fit_transform(enc_df['encounter_type'])

    # Now your 'Encounter Type' has been encoded to 'Encounter Type Encoded' as numbers
    # Features (Resource Distance) and Target Variable (Encoded Encounter Types)
    X = enc_df[['Resource Distance']]  # Predictor
    y = enc_df['Encounter Type Encoded']  # Response

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a logistic regression model
    # For multinomial, 'lbfgs' solver is recommended
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=200)

    # Fit the model with the training data
    model.fit(X_train, y_train)

    # Predict the test set results
    y_pred = model.predict(X_test)

    # Print the classification report
    print(classification_report(y_test, y_pred))

    # inverse transform encoded labels back to the original labels
    y_pred_labels = label_encoder.inverse_transform(y_pred)


if __name__ == "__main__":
    main()
