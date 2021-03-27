import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class World:
    """
    A general class representing a world.

    Attributes
    ----------
    graph: nx.Graph
        the graph of the whole world
    positions: list
        the list of all the positions of the nodes as tuples (x, y)
    """
    def __init__(self, number_of_nodes=7, number_of_warehouses=1, radius=0.5, seed=3):
        """
        Initializer of the function.

        Parameters
        ----------
        number_of_nodes: int
            the number of nodes in the world where each node represents either a hospital (type 0) or a
            warehouse (type 1)
        number_of_warehouses: int
            the number of warehouses to be considered for a given world. Needs to be smaller than number_of_nodes
        radius: float
            the radius used in random graph generation. Should be between 0 and 1 and decides whether two nodes are
            connected or not.
        seed: int
            the random seed used to generate the world
        """
        # Get graph and positions
        self.graph = nx.random_geometric_graph(number_of_nodes, radius, seed=seed)
        # Dictionary
        self.positions = nx.get_node_attributes(self.graph, "pos")

        # Generate random warehouses
        np.random.seed(seed)
        random_warehouse_locations = np.random.choice(self.graph.nodes, number_of_warehouses, replace=False)

        # Label all the nodes
        for node in self.graph.nodes:
            pointer = self.graph.nodes[node]
            if node != random_warehouse_locations:
                pointer['type'] = 0
                pointer['demand1'] = np.random.randint(5)
                pointer['demand2'] = np.random.randint(5)
                pointer['priority'] = np.random.randint(3)
            else:
                pointer['type'] = 1

        # Label all the edges
        for edge in self.graph.edges:
            node1 = np.array(self.graph.nodes[edge[0]]['pos'])
            node2 = np.array(self.graph.nodes[edge[1]]['pos'])
            pointer = self.graph.edges[edge[0], edge[1]]
            pointer['length'] = float(f"{np.linalg.norm(node1 - node2):.2f}")
            pointer['traffic'] = 1
            pointer['capacity'] = np.inf

    def plot(self):
        """
        Plots a simple representation of the world. The hospitals are marked in blue, the warehouses in green.
        """
        # Obtain the edge labels
        edge_labels = {}
        for edge in self.graph.edges:
            edge_labels[edge] = self.graph.edges[edge[0], edge[1]]['length']

        # Obtain the node colors
        node_colors = []
        node_labels = {}
        for node in self.graph.nodes:
            if self.graph.nodes[node]['type'] == 0:
                node_colors.append("lightblue")
                node_labels[node] = f"{node}/{self.graph.nodes[node]['demand1']}/{self.graph.nodes[node]['demand2']}/" \
                                    f"{self.graph.nodes[node]['priority']}"
            else:
                node_labels[node] = f"{node}"
                node_colors.append("lightgreen")

        # Plot the nodes, edges and labels
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_edges(self.graph, self.positions, alpha=0.4)
        nx.draw_networkx_nodes(self.graph, self.positions, node_color=node_colors)
        nx.draw_networkx_labels(self.graph, self.positions, node_labels)
        nx.draw_networkx_edge_labels(self.graph, self.positions, edge_labels)
        plt.show()


if __name__ == "__main__":
    # Run a test
    world = World()
    world.plot()
    print(list(nx.all_pairs_dijkstra(world.graph)))
