import networkx as nx

class SocialNetwork:
    def __init__(self):
        self.graph = nx.Graph()

    def add_being(self, being_id):
        """Add a new being to the social network graph."""
        self.graph.add_node(being_id)

    def remove_being(self, being_id):
        """Remove a being from the social network graph."""
        self.graph.remove_node(being_id)

    def add_connection(self, being_id1, being_id2):
        """Add a connection between two beings."""
        self.graph.add_edge(being_id1, being_id2)

    def remove_connection(self, being_id1, being_id2):
        """Remove the connection between two beings."""
        self.graph.remove_edge(being_id1, being_id2)

    def get_connections(self, being_id):
        """Get all connections for a given being."""
        return list(self.graph.neighbors(being_id))

    def get_common_connections(self, being_id1, being_id2):
        """Get common connections between two beings."""
        return list(nx.common_neighbors(self.graph, being_id1, being_id2))

    def are_connected(self, being_id1, being_id2):
        """Check if two beings are directly connected."""
        return self.graph.has_edge(being_id1, being_id2)

    # Additional methods for analyzing the social network can be added here, such as finding groups or communities.
