import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import numpy as np
import pathlib


class World:
    """
    A general class representing a world.

    Attributes
    ----------
    graph: nx.Graph
        the graph of the whole world
    """

    def __init__(self, number_of_warehouses=1, number_of_hospitals=5, seed=3):
        """
        Initializer of the function. There are three types of nodes. (0) is a hospital, (1) a warehouse and (2) anything
        else, like cross roads.

        Parameters
        ----------
        number_of_warehouses: int
            the number of warehouses to be considered for a given world. Needs to be smaller than number_of_nodes
        seed: int
            the random seed used to generate the world
        """
        # Get graph and positions
        filepath = pathlib.Path(__file__).parent.absolute() / "Cambridge_Graph.xml"
        #project graph to metres
        self.graph = ox.project_graph(ox.io.load_graphml(filepath), to_crs="EPSG:3395")
        ox.add_edge_speeds(self.graph)
        ox.add_edge_travel_times(self.graph)

        # Generate random warehouses
        np.random.seed(seed)
        random_locations = np.random.choice(self.graph.nodes, number_of_warehouses + number_of_hospitals, replace=False)
        random_warehouse_locations = random_locations[:number_of_warehouses]
        random_hospital_locations = random_locations[number_of_warehouses:]

        # Set them to be readable by the object
        self.warehouses = list(random_warehouse_locations)
        self.hospitals = list(random_hospital_locations)

        # Label all the nodes
        for node in self.graph.nodes:
            pointer = self.graph.nodes[node]
            if node in random_hospital_locations:
                # Hospitals
                pointer['type'] = 0
                pointer['demand1'] = np.random.randint(2)       # Going to change this to between 0 and 1 for now
                pointer['demand2'] = np.random.randint(2)
                pointer['priority'] = np.random.randint(3)
            elif node in random_warehouse_locations:
                # Warehouses
                pointer['type'] = 1
            else:
                # Corners
                pointer['type'] = 2

        # Label all the edges with traffic - to get higher values change the multiplier
        for edge in self.graph.edges:
            pointer = self.graph.edges[edge]
            pointer['travel_time'] *= 1.0


    def plot(self, ax, show=True):
        """
        Plots a simple representation of the world. The hospitals are marked in blue, the warehouses in green.
        """
        # Obtain the edge labels
        # edge_labels = {}
        # for edge in self.graph.edges:
        #     edge_labels[edge] = self.graph.edges[edge[0], edge[1]]['length']

        # Obtain the node colors
        node_colors = []
        for node in self.graph.nodes:
            if self.graph.nodes[node]['type'] == 0:
                node_colors.append("#ff0000ff")
            elif self.graph.nodes[node]['type'] == 1:
                node_colors.append("#00ff00ff")
            else:
                node_colors.append("#00000000")

        # Plot the graph
        ox.plot_graph(self.graph, ax=ax, node_color=node_colors, node_size=80, show=False)

        # Plot the text for the hospitals
        for node in self.hospitals:
            pointer = self.graph.nodes[node]
            plt.text(pointer['x'], pointer['y'], f"  {pointer['demand1']}/{pointer['demand2']}"
                                                 f"/{pointer['priority']}", color="white")

        # Show the plot if required
        if show:
            plt.show()


if __name__ == "__main__":
    # Run a test
    world = World()
    print(world.warehouses, world.hospitals)
    world.plot()
