from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import mainthread
import time
import os
import pygame
import numpy as np
import sounddevice as sd
import requests
import speech_recognition as sr
import folium
import osmnx as ox
import networkx as nx
import pandas as pd
from shapely.geometry import Point
from kivy.utils import platform
from plyer import gps, notification

class SOSApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        self.sos_button = Button(text='SOS', font_size=24, background_color=(1, 0, 0, 1))
        self.sos_button.bind(on_press=self.on_sos_button_click)
        layout.add_widget(self.sos_button)
        
        self.tracker_button = Button(text='Tracker', font_size=24, background_color=(0, 0, 1, 1))
        self.tracker_button.bind(on_press=self.on_tracker_button_click)
        layout.add_widget(self.tracker_button)
        
        self.map_button = Button(text='Safe Route Map', font_size=24, background_color=(0, 1, 0, 1))
        self.map_button.bind(on_press=self.on_map_button_click)
        layout.add_widget(self.map_button)
        
        return layout
    
    def send_emergency_alert(self):
        try:
            gps.configure(on_location=self.on_gps_location, on_status=self.on_gps_status)
            gps.start()
        except NotImplementedError:
            print("GPS not supported on this platform")
    
    @mainthread
    def on_gps_location(self, **kwargs):
        location = f"Lat: {kwargs['lat']}, Lon: {kwargs['lon']}"
        emergency_message = f"EMERGENCY! I am in danger. My location: {location}"
        print(emergency_message)
        notification.notify(title="Emergency Alert", message=emergency_message)
    
    def play_sos(self, instance):
        pygame.mixer.init()
        if os.path.exists("sos.wav"):
            beep = pygame.mixer.Sound("sos.wav")
            beep.play()
        else:
            samplerate = 44100
            duration = 0.3
            t = np.linspace(0, duration, int(samplerate * duration), False)
            wave = 0.5 * np.sin(2 * np.pi * 1000 * t)
            sd.play(wave, samplerate)
            sd.wait()
    
    def on_sos_button_click(self, instance):
        self.send_emergency_alert()
        self.play_sos(instance)
    
    def on_tracker_button_click(self, instance):
        self.send_emergency_alert()
    
    def on_map_button_click(self, instance):
        crime_hotspots = pd.DataFrame({
            'latitude': [28.6500, 28.6350, 28.6200, 28.6100, 28.6400],
            'longitude': [77.2000, 77.2150, 77.2300, 77.2500, 77.1900]
        })
        
        police_stations = pd.DataFrame({
            'latitude': [28.6450, 28.6250, 28.6355, 28.6050, 28.6600],
            'longitude': [77.2050, 77.2250, 77.2400, 77.2600, 77.1950]
        })
        
        start = (28.6740, 77.1300)
        end = (28.6100, 77.2900)
        
        G = ox.graph_from_place("Delhi, India", network_type='walk')
        orig_node = ox.distance.nearest_nodes(G, X=start[1], Y=start[0])
        dest_node = ox.distance.nearest_nodes(G, X=end[1], Y=end[0])
        safe_route = nx.shortest_path(G, orig_node, dest_node, weight='length')
        
        route_map = folium.Map(location=[28.6300, 77.2200], zoom_start=12)
        
        for _, row in crime_hotspots.iterrows():
            folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=5, color='red', fill=True, fill_color='red', popup='Crime Hotspot').add_to(route_map)
        
        for _, row in police_stations.iterrows():
            folium.Marker(location=[row['latitude'], row['longitude']], icon=folium.Icon(color='blue', icon='shield'), popup='Police Station').add_to(route_map)
        
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in safe_route]
        folium.PolyLine(route_coords, color='green', weight=5, opacity=0.7, popup='Safe Route').add_to(route_map)
        
        route_map.save("safe_route_map.html")
        notification.notify(title="Map Generated", message="Safe route map saved as safe_route_map.html")

if __name__ == "__main__":
    SOSApp().run()