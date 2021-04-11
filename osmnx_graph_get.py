import osmnx as ox
import pathlib

map_location = "Sydney"

path = pathlib.Path(__file__).parent.absolute()

if map_location == "Cambridge":

    filepath = path / "Cambridge_Graph.xml"

    graph = ox.get_undirected(ox.project_graph(ox.graph_from_point((52.206000250695205, 0.1218685443020611),dist=2000, network_type="drive_service"), to_crs="EPSG:27700"))

    ox.save_graphml(graph, filepath=filepath)

elif map_location == "Sydney":

    filepath = path / "Sydney_Graph.xml"

    graph = ox.get_undirected(ox.project_graph(ox.graph_from_address('Sydney, Australia',dist=1500, network_type="drive_service"), to_crs="EPSG:27700"))

    ox.save_graphml(graph, filepath=filepath)