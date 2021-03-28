import osmnx as ox
import pathlib

map_location = "Sydney"

path = pathlib.Path(__file__).parent.absolute()

if map_location == "Cambridge":

    filepath = path / "Cambridge_Graph.xml"

    graph = ox.get_undirected(ox.graph_from_address('Cambridge, United Kingdom', network_type="drive_service"))

    ox.save_graphml(graph, filepath=filepath)

elif map_location == "Sydney":

    filepath = path / "Sydney_Graph.xml"

    graph = ox.get_undirected(ox.graph_from_address('Sydney, Australia', network_type="drive_service"))

    ox.save_graphml(graph, filepath=filepath)