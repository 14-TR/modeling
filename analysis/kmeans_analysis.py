import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans


def read_encounters_log(filepath):
    return pd.read_csv(filepath)


def filter_inf_events(df, encounter_type='INF'):
    return df[df['encounter_type'] == encounter_type].copy()


def clean_coordinates(df):
    df['X'] = df['X'].str.strip('(),').astype(float)
    df['Y'] = df['Y'].str.strip('(),').astype(float)
    return df[['X', 'Y']]


def run_kmeans_clustering(df, n_clusters=10):
    coords = df[['X', 'Y']]
    kmeans = KMeans(n_clusters=n_clusters, random_state=1).fit(coords)
    df['cluster'] = kmeans.labels_
    return df, kmeans.labels_, kmeans.cluster_centers_


def plot_clusters(df, centers):
    plt.scatter(df['X'], df['Y'], c=df['cluster'], cmap='viridis', alpha=0.7, edgecolors='b')
    plt.scatter(centers[:, 0], centers[:, 1], s=250, marker='*', c='red')
    plt.title('K-Means Clustering of Encounter Locations')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.show()


def main():
    encounters_log_path = r"C:\Users\tingram\Desktop\Captains Log\UWYO\GIT\sims\sim__20240322-160053\encounters.csv"
    encounters_df = read_encounters_log(encounters_log_path)
    inf_df = filter_inf_events(encounters_df)
    coords_df = clean_coordinates(inf_df)
    clustered_df, labels, centers = run_kmeans_clustering(coords_df, n_clusters=5)

    n_clusters_ = len(centers)
    print('Estimated number of clusters:', n_clusters_)

    # Additional metrics or analysis can be added here if needed

    plot_clusters(clustered_df, centers)


if __name__ == "__main__":
    main()

