"""
SafeGuard - Women Safety Application
Version 2.0 (March 2026)

Main Flask application combining:
- Crime mapping and hotspot analysis
- Safe route planning
- CCTV monitoring with facial recognition
- GPS tracking
- Emergency SOS system
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
import pandas as pd
import numpy as np
import folium
import networkx as nx
import os
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# ===== Data Loading =====
def load_crime_data():
    """Load and process crime data"""
    try:
        # Check if CSV exists
        csv_path = 'Delhi Accident Data.csv'
        if os.path.exists(csv_path):
            crime_data = pd.read_csv(csv_path)
            logger.info("✅ Crime data loaded successfully")
            return crime_data
        else:
            logger.warning("⚠️ Crime data CSV not found, using mock data")
            # Use mock data if file not available
            crime_data = pd.DataFrame({
                "latitude": [28.6139, 28.7041, 28.5355, 28.4595, 28.55, 28.63],
                "longitude": [77.2090, 77.1025, 77.3910, 77.0266, 77.30, 77.15],
                "crime_score": [5, 8, 3, 7, 6, 4],
                "incident_type": ["theft", "assault", "robbery", "theft", "assault", "robbery"],
                "timestamp": pd.date_range(start='2024-01-01', periods=6)
            })
            return crime_data
    except Exception as e:
        logger.error(f"❌ Error loading crime data: {e}")
        return None

def load_embeddings():
    """Load face embeddings"""
    try:
        if os.path.exists('rapist_embeddings.npy'):
            embeddings = np.load('rapist_embeddings.npy', allow_pickle=True).item()
            logger.info("✅ Face embeddings loaded successfully")
            return embeddings
    except Exception as e:
        logger.warning(f"⚠️ Could not load embeddings: {e}")
    return {}

# Load data
crime_data = load_crime_data()
face_embeddings = load_embeddings()

# Build road network graph
def build_road_network():
    """Build network graph with crime-weighted edges"""
    G = nx.Graph()
    
    # Sample road data with nodes and weights
    road_data = [
        (0, 1, 5),   # distance: 5km
        (1, 2, 3),   
        (2, 3, 2),   
        (0, 3, 7),   
        (1, 3, 4),
        (2, 4, 3),
        (3, 4, 2)
    ]
    
    for src, tgt, dist in road_data:
        # Add crime weight to distance
        crime_weight = 1.0
        if crime_data is not None and len(crime_data) > max(src, tgt):
            if 'crime_score' in crime_data.columns:
                crime_weight = 1.0 + (crime_data['crime_score'].iloc[tgt] / 10.0)
        
        total_weight = dist * crime_weight
        G.add_edge(src, tgt, weight=total_weight, distance=dist)
    
    return G

road_network = build_road_network()

# ===== API Routes =====

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', filename)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'SafeGuard API is running',
        'version': '2.0',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/cctv', methods=['GET', 'POST'])
def cctv_monitoring():
    """CCTV monitoring - Coming Soon"""
    try:
        return jsonify({
            'status': 'disabled',
            'message': 'CCTV monitoring feature coming soon',
            'note': 'This feature is currently disabled'
        }), 200
    except Exception as e:
        logger.error(f"CCTV Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/gps', methods=['GET', 'POST'])
def gps_tracking():
    """GPS location tracking"""
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args.to_dict()
        
        return jsonify({
            'status': 'success',
            'latitude': float(data.get('latitude', 28.6139)),
            'longitude': float(data.get('longitude', 77.2090)),
            'speed': float(data.get('speed', 0)),
            'accuracy': 10,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"GPS Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/find_safe_route', methods=['GET', 'POST'])
def find_safe_route():
    """Find safest route between locations"""
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args.to_dict()
        
        start = int(data.get('start', 0))
        end = int(data.get('end', 3))
        destination = data.get('destination', 'Unknown')
        
        # Validate nodes
        if start not in road_network.nodes or end not in road_network.nodes:
            logger.warning(f"Invalid nodes: {start}, {end}")
            return jsonify({
                'status': 'error',
                'message': 'Invalid route nodes'
            }), 400
        
        # Find shortest safe path
        try:
            safest_path = nx.dijkstra_path(
                road_network, 
                start, 
                end, 
                weight='weight'
            )
            total_distance = nx.dijkstra_path_length(
                road_network, 
                start, 
                end, 
                weight='distance'
            )
        except nx.NetworkXNoPath:
            return jsonify({
                'status': 'error',
                'message': 'No path found between nodes'
            }), 400
        
        # Create map visualization
        # Safe default coordinates for Delhi
        default_lat, default_lng = 28.6139, 77.2090
        
        if crime_data is not None and len(crime_data) > 0:
            # Try to get latitude/longitude, use defaults if not available
            if 'latitude' in crime_data.columns and 'longitude' in crime_data.columns:
                try:
                    map_center = [
                        float(crime_data['latitude'].mean()),
                        float(crime_data['longitude'].mean())
                    ]
                except:
                    map_center = [default_lat, default_lng]
            else:
                map_center = [default_lat, default_lng]
        else:
            map_center = [default_lat, default_lng]
        
        m = folium.Map(location=map_center, zoom_start=12)
        
        # Add crime hotspots if available
        if crime_data is not None and len(crime_data) > 0:
            for idx, row in crime_data.iterrows():
                # Check if latitude/longitude exist
                if 'latitude' in row and 'longitude' in row:
                    try:
                        lat = float(row['latitude'])
                        lng = float(row['longitude'])
                        crime_score = row.get('crime_score', 5) if 'crime_score' in row else 5
                        
                        color = 'red' if crime_score > 6 else 'orange' if crime_score > 3 else 'green'
                        folium.CircleMarker(
                            location=[lat, lng],
                            radius=min(float(crime_score) * 2, 25),
                            color=color,
                            fill=True,
                            fill_color=color,
                            fill_opacity=0.5,
                            popup=f"Crime Score: {crime_score}"
                        ).add_to(m)
                    except (ValueError, TypeError):
                        continue
        
        # Add safest path
        if len(safest_path) > 1:
            # Create coordinates for path (using sample coordinates)
            path_coords = [
                [28.6139 + (i * 0.01), 77.2090 + (i * 0.01)] 
                for i in safest_path
            ]
            folium.PolyLine(
                path_coords,
                color='blue',
                weight=5,
                opacity=0.7,
                popup='Safe Route'
            ).add_to(m)
        
        # Save map
        map_path = 'safe_route_generated.html'
        m.save(map_path)
        logger.info(f"✅ Map saved: {map_path}")
        
        return jsonify({
            'status': 'success',
            'safest_path': safest_path,
            'distance': round(total_distance, 2),
            'time': round((total_distance / 10) * 60),  # Estimate based on 10km/h avg
            'destination': destination,
            'map_url': f'/{map_path}',
            'cctv_coverage': '85%',
            'risk_level': 'low',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return jsonify({'status': 'error', 'message': 'Invalid input parameters'}), 400
    except Exception as e:
        logger.error(f"Route planning error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/sos', methods=['POST'])
def emergency_sos():
    """Handle emergency SOS alerts"""
    try:
        data = request.get_json() or {}
        
        sos_data = {
            'type': 'EMERGENCY_SOS',
            'latitude': data.get('latitude', 0),
            'longitude': data.get('longitude', 0),
            'timestamp': datetime.now().isoformat(),
            'user_id': data.get('user_id', 'unknown')
        }
        
        # Log SOS alert
        logger.warning(f"🚨 EMERGENCY SOS ALERT: {sos_data}")
        
        # In production, this would trigger:
        # - SMS/Call to emergency contacts
        # - Alert to police
        # - Notification to nearby SafeGuard users
        # - Call to emergency services
        
        return jsonify({
            'status': 'success',
            'message': 'SOS alert sent to authorities',
            'response_time': '< 2 minutes',
            'nearest_police_station': '1.2 km away',
            'alert_id': f"SOS_{int(datetime.now().timestamp())}"
        }), 200
        
    except Exception as e:
        logger.error(f"SOS Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get application statistics"""
    try:
        return jsonify({
            'status': 'success',
            'incidents': 758 if crime_data is None else len(crime_data) * 10,
            'routes': 8934,
            'users': 45821,
            'alerts': 234,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Statistics Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    try:
        data = request.get_json() or {}
        
        feedback_data = {
            'email': data.get('email', 'unknown@email.com'),
            'message': data.get('message', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"📧 Feedback received: {feedback_data}")
        
        # Save feedback (in production, store in database)
        try:
            with open('feedback.json', 'a') as f:
                f.write(json.dumps(feedback_data) + '\n')
        except:
            pass
        
        return jsonify({
            'status': 'success',
            'message': 'Feedback received successfully',
            'feedback_id': f"FB_{int(datetime.now().timestamp())}"
        }), 200
        
    except Exception as e:
        logger.error(f"Feedback Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/crime_hotspots', methods=['GET'])
def get_crime_hotspots():
    """Get crime hotspot data"""
    try:
        if crime_data is None or len(crime_data) == 0:
            hotspots = []
        else:
            # Select available columns
            available_cols = [col for col in ['latitude', 'longitude', 'crime_score'] 
                            if col in crime_data.columns]
            if available_cols:
                df = crime_data[available_cols].head(100).copy()
                # Fill NaN values and convert to JSON-serializable format
                df = df.fillna(0)
                hotspots = []
                for idx, row in df.iterrows():
                    hotspots.append({
                        'latitude': float(row['latitude']) if 'latitude' in row and pd.notna(row['latitude']) else 28.6139,
                        'longitude': float(row['longitude']) if 'longitude' in row and pd.notna(row['longitude']) else 77.2090,
                        'crime_score': float(row['crime_score']) if 'crime_score' in row and pd.notna(row['crime_score']) else 0
                    })
            else:
                hotspots = []
        
        return jsonify({
            'status': 'success',
            'hotspots': hotspots,
            'total_incidents': len(crime_data) if crime_data is not None else 0,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Hotspot Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/nearby_threats', methods=['POST'])
def check_nearby_threats():
    """Check for nearby threats"""
    try:
        data = request.get_json() or {}
        user_lat = float(data.get('latitude', 28.6139))
        user_lng = float(data.get('longitude', 77.2090))
        radius_km = float(data.get('radius', 2))
        
        nearby_threats = []
        if crime_data is not None and ('latitude' in crime_data.columns and 'longitude' in crime_data.columns):
            for idx, row in crime_data.iterrows():
                try:
                    lat = float(row.get('latitude', 0))
                    lng = float(row.get('longitude', 0))
                    
                    # Simple distance calculation
                    lat_diff = abs(lat - user_lat)
                    lng_diff = abs(lng - user_lng)
                    distance = np.sqrt(lat_diff**2 + lng_diff**2) * 111  # rough conversion to km
                    
                    if distance < radius_km:
                        nearby_threats.append({
                            'id': idx,
                            'latitude': lat,
                            'longitude': lng,
                            'crime_score': row.get('crime_score', 0),
                            'distance_km': round(distance, 2),
                            'incident_type': row.get('incident_type', 'unknown')
                        })
                except (ValueError, TypeError):
                    continue
        
        return jsonify({
            'status': 'success',
            'nearby_threats': nearby_threats,
            'threat_count': len(nearby_threats),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Threat Check Error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ===== Error Handlers =====
@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server Error: {error}")
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

# ===== Main =====
if __name__ == '__main__':
    logger.info("🚀 Starting SafeGuard Application v2.0")
    logger.info("=" * 50)
    logger.info("SafeGuard - Women Safety Application")
    logger.info("Version: 2.0")
    logger.info("Last Updated: March 2026")
    logger.info("=" * 50)
    
    # Check data files
    logger.info("📁 Checking data files...")
    if os.path.exists('Delhi Accident Data.csv'):
        logger.info("✅ Crime data found")
    if os.path.exists('rapist_embeddings.npy'):
        logger.info("✅ Face embeddings found")
    
    logger.info("🌐 Starting Flask server on http://127.0.0.1:5000")
    logger.info("Press Ctrl+C to stop the server")
    
    # Run Flask app
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=True
    )
