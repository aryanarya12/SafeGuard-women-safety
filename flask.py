import pandas as pd
import folium
import networkx as nx
from flask import Flask, request, jsonify

# Load Crime Hotspot Data
crime_data = pd.DataFrame({
    "latitude": [28.6139, 28.7041, 28.5355, 28.4595],
    "longitude": [77.2090, 77.1025, 77.3910, 77.0266],
    "crime_score": [5, 8, 3, 7]
})

# Load Road Network
road_data = [(0, 1, 5), (1, 2, 3), (2, 3, 2), (0, 3, 7)]

# Build Graph
G = nx.Graph()
for src, tgt, dist in road_data:
    G.add_edge(src, tgt, weight=dist + (crime_data["crime_score"][tgt] / 2))

# Initialize Flask App
app = Flask(__name__)

@app.route('/find_safe_route', methods=['GET'])
def find_safe_route():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))

    if start not in G.nodes or end not in G.nodes:
        return jsonify({"error": "Invalid nodes"}), 400

    safest_path = nx.dijkstra_path(G, start, end, weight='weight')

    m = folium.Map(location=[crime_data["latitude"].mean(), crime_data["longitude"].mean()], zoom_start=12)

    for idx, row in crime_data.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=row["crime_score"],
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.5,
        ).add_to(m)

    path_coords = [(crime_data["latitude"][i], crime_data["longitude"][i]) for i in safest_path]
    folium.PolyLine(path_coords, color="blue", weight=5, opacity=0.7).add_to(m)

    m.save("safe_route_map.html")

    return jsonify({"safest_path": safest_path, "map_url": "safe_route_map.html"})

if __name__ == '__main__':
    app.run(debug=True)
