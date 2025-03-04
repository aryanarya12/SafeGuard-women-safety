import geopandas as gpd
import folium
import osmnx as ox
import networkx as nx
import pandas as pd
from shapely.geometry import Point

def load_data():
    crime_hotspots = pd.DataFrame({
        'latitude': [28.7041, 28.6129, 28.5355],
        'longitude': [77.1025, 77.2295, 77.3910]
    })
    
    police_stations = pd.DataFrame({
        'latitude': [28.7075, 28.6139, 28.5425],
        'longitude': [77.1500, 77.2089, 77.4120]
    })
    
    return crime_hotspots, police_stations

def create_safe_route(start, end, crime_hotspots, police_stations):
    G = ox.graph_from_place("Delhi, India", network_type='walk')
    
    orig_node = ox.distance.nearest_nodes(G, X=start[1], Y=start[0])
    dest_node = ox.distance.nearest_nodes(G, X=end[1], Y=end[0])
    
    for u, v, data in G.edges(data=True):
        edge_center = ((G.nodes[u]['y'] + G.nodes[v]['y']) / 2, (G.nodes[u]['x'] + G.nodes[v]['x']) / 2)
        
        if any(Point(edge_center).distance(Point(hotspot)) < 0.005 for hotspot in zip(crime_hotspots['latitude'], crime_hotspots['longitude'])):
            data['weight'] = data.get('length', 1) * 10  
        
        elif any(Point(edge_center).distance(Point(police)) < 0.005 for police in zip(police_stations['latitude'], police_stations['longitude'])):
            data['weight'] = data.get('length', 1) * 0.5  
        else:
            data['weight'] = data.get('length', 1)
    
    safe_route = nx.shortest_path(G, orig_node, dest_node, weight='weight')
    
    return G, safe_route

def plot_map(G, safe_route, crime_hotspots, police_stations):
    route_map = folium.Map(location=[28.6139, 77.2090], zoom_start=12)
    
    for _, row in crime_hotspots.iterrows():
        folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=5, color='red', fill=True, fill_color='red', popup='Crime Hotspot').add_to(route_map)
    
    for _, row in police_stations.iterrows():
        folium.Marker(location=[row['latitude'], row['longitude']], icon=folium.Icon(color='blue', icon='shield'), popup='Police Station').add_to(route_map)
    
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in safe_route]
    folium.PolyLine(route_coords, color='green', weight=5, opacity=0.7, popup='Safe Route').add_to(route_map)
    
    return route_map

def main():
    crime_hotspots, police_stations = load_data()
    start = (28.7041, 77.1025)
    end = (28.5355, 77.3910)
    
    G, safe_route = create_safe_route(start, end, crime_hotspots, police_stations)
    route_map = plot_map(G, safe_route, crime_hotspots, police_stations)
    
    route_map.save("safe_route_delhi.html")
    print("Safe route map saved as safe_route_delhi.html")

if __name__ == "__main__":
    main()
