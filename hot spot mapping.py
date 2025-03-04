import geopandas as gpd
import folium
import osmnx as ox
import networkx as nx
import pandas as pd
from shapely.geometry import Point

def load_data():
    crime_hotspots = pd.DataFrame({
        'latitude': [28.6500, 28.6350, 28.6200, 28.6100, 28.6400],
        'longitude': [77.2000, 77.2150, 77.2300, 77.2500, 77.1900]
    })
    
    police_stations = pd.DataFrame({
        'latitude': [28.6450, 28.6250, 28.6355, 28.6050, 28.6600],
        'longitude': [77.2050, 77.2250, 77.2400, 77.2600, 77.1950]
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
        
        # Assign random speed limits between 4 km/h to 7 km/h
        speed_limit = 4 + (3 * (hash((u, v)) % 100) / 100)  # Randomized between 4 and 7 km/h
        travel_time = data['length'] / (speed_limit * 1000 / 60)  # time in minutes
        data['weight'] += travel_time  # Incorporate travel time in weight calculation
    
    safe_route = nx.shortest_path(G, orig_node, dest_node, weight='weight')
    
    return G, safe_route

def plot_map(G, safe_route, crime_hotspots, police_stations):
    route_map = folium.Map(location=[28.6300, 77.2200], zoom_start=12)
    
    for _, row in crime_hotspots.iterrows():
        folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=5, color='red', fill=True, fill_color='red', popup='Crime Hotspot').add_to(route_map)
    
    for _, row in police_stations.iterrows():
        folium.Marker(location=[row['latitude'], row['longitude']], icon=folium.Icon(color='blue', icon='shield'), popup='Police Station').add_to(route_map)
    
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in safe_route]
    folium.PolyLine(route_coords, color='green', weight=5, opacity=0.7, popup='Safe Route').add_to(route_map)
    
    return route_map

def main():
    crime_hotspots, police_stations = load_data()
    start = (28.6740, 77.1300)  # Punjabi Bagh
    end = (28.6100, 77.2900)    # Mayur Vihar Phase 1
    
    G, safe_route = create_safe_route(start, end, crime_hotspots, police_stations)
    route_map = plot_map(G, safe_route, crime_hotspots, police_stations)
    
    route_map.save("safe_route_punjabi_bagh_mayur_vihar.html")
    print("Safe route map saved as safe_route_punjabi_bagh_mayur_vihar.html")

if __name__ == "__main__":
    main()
