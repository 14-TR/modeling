import pandas as pd
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from sklearn import metrics
import numpy as np


def read_encounters_log(filepath):
    df = pd.read_csv(filepath)
    return df


def filter_inf_events(df, encounter_type='INF'):
    inf_df = df[df['encounter_type'] == encounter_type].copy()
    return inf_df


def clean_coordinates(df):
    df['X'] = df['X'].str.strip('(),').astype(float)
    df['Y'] = df['Y'].str.strip('(),').astype(float)
    return df[['X', 'Y']]  # Return only the cleaned coordinates


def run_affinity_propagation(df):
    coords = df[['X', 'Y']]
    clustering = AffinityPropagation(random_state=5).fit(coords)
    df['cluster'] = clustering.labels_
    return df, clustering.labels_, clustering.cluster_centers_


def plot_clusters(df, centers):
    plt.scatter(df['X'], df['Y'], c=df['cluster'], cmap='rainbow', alpha=0.7, edgecolors='b')
    # plt.scatter(centers[:, 0], centers[:, 1], s=250, marker='*', c='black')
    plt.title('Affinity Propagation Clustering')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.show()


def main():
    encounters_log_path = r"C:\Users\tingram\Desktop\Captains Log\UWYO\GIT\sims\sim__20240322-144047\encounters.csv"
    encounters_df = read_encounters_log(encounters_log_path)
    inf_df = filter_inf_events(encounters_df)
    coords_df = clean_coordinates(inf_df)
    clustered_df, labels, centers = run_affinity_propagation(coords_df)

    n_clusters_ = len(centers)
    print('Estimated number of clusters: %d' % n_clusters_)

    # Silhouette Coefficient
    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(coords_df, labels, metric='sqeuclidean'))

    plot_clusters(clustered_df, centers)


if __name__ == "__main__":
    main()
