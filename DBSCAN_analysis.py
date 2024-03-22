import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt


def read_encounters_log(filepath):
    """
    Read the encounters log into a DataFrame.
    """
    df = pd.read_csv(filepath)
    return df


def filter_inf_events(df, encounter_type='INF'):
    """
    Filter the DataFrame for INF encounter types.
    """
    inf_df = df[df['encounter_type'] == encounter_type].copy()
    return inf_df


def clean_coordinates(df):
    """
    Clean and convert the 'X' and 'Y' columns from string tuples to integers.
    """
    df['X'] = df['X'].str.strip('(),').astype(float)
    df['Y'] = df['Y'].str.strip('(),').astype(float)
    return df


def perform_dbscan_clustering(df, eps=50, min_samples=5):
    """
    Perform DBSCAN clustering on XY grid data.
    """
    coords = df[['X', 'Y']].to_numpy()
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    df['cluster'] = dbscan.fit_predict(coords)
    return df


def plot_clusters(df):
    """
    Plotting the DBSCAN clustering results on an XY grid.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    scatter = ax.scatter(df['X'], df['Y'], c=df['cluster'], cmap='viridis', s=50)
    legend1 = ax.legend(*scatter.legend_elements(),
                        loc="upper left", title="Clusters")
    ax.add_artist(legend1)
    plt.title('DBSCAN Clustering Results on XY Grid')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.show()


def main():
    """
    Main function to orchestrate the DBSCAN analysis for INF events on an XY grid.
    """
    # Path to your encounters log CSV file
    encounters_log_path = r"C:\Users\tingram\Desktop\Captains Log\UWYO\GIT\sims\sim__20240322-122005\encounters.csv"

    # Read the encounters log
    encounters_df = read_encounters_log(encounters_log_path)

    # Filter for INF events
    inf_df = filter_inf_events(encounters_df)

    # Clean and prepare the coordinates
    cleaned_df = clean_coordinates(inf_df)

    # Perform DBSCAN clustering
    clustered_df = perform_dbscan_clustering(cleaned_df, eps=50, min_samples=5)

    # Plot the clustering results
    plot_clusters(clustered_df)


if __name__ == "__main__":
    main()
