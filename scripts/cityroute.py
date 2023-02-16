# -*- coding: utf-8 -*-
"""
@author: Sander van der Plas
"""

from geopy.geocoders import Nominatim
import osmnx as ox

class cityroute:
    def __init__(self, city, origin_location, dest_location, network_type='bike', weight='length'):
        self.city = city
        self.origin_location = origin_location
        self.dest_location = dest_location
        self.network_type = network_type
        self.weight = weight
    
    def geocode_location(self, location):
        locator = Nominatim(user_agent = "myapp")
        geocoded_location = locator.geocode(location)
        if geocoded_location:
            return geocoded_location.longitude, geocoded_location.latitude
        else:
            raise ValueError(f"The location '{location}' could not be found.")

    def get_shortest_path(self):
        # Geocode origin and destination locations
        origin_coordinates = self.geocode_location(self.origin_location)
        dest_coordinates = self.geocode_location(self.dest_location)
        
        
        # Print the origin and destination coordinates
        print("Origin Coordinates:", origin_coordinates)
        print("Destination Coordinates:", dest_coordinates)

        # Get bike network
        roads_graph = ox.graph.graph_from_place(self.city, network_type=self.network_type)

        # get nodes and edges
        nodes, edges = ox.graph_to_gdfs(roads_graph, nodes=True, edges=True)

        # Origin
        source = ox.distance.nearest_nodes(roads_graph, origin_coordinates[0], origin_coordinates[1])

        # Destination
        target = ox.distance.nearest_nodes(roads_graph, dest_coordinates[0], dest_coordinates[1])

        # Compute shortest path 
        shortest_route = ox.distance.shortest_path(G=roads_graph, orig=source, dest=target, weight=self.weight)
    
        return shortest_route, roads_graph, nodes, edges

if __name__ == "__main__":
        city = 'Utrecht, Netherlands'
        origin_location = "Utrecht station"
        dest_location = "Parijsboulevard 143 Utrecht"
        network_type = 'bike'
        weight = 'length'
        shortest_path, roads_graph, nodes, edges = cityroute(city, origin_location, dest_location, network_type, weight).get_shortest_path()


