import time
import geocoder
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from geopy.distance import geodesic

class Speedometer(App):
    def build(self):
        self.label = Label(text="Fetching Location...", font_size=24)
        self.prev_location = None
        self.prev_time = None
        Clock.schedule_interval(self.update_location, 5)  # Update every 5 seconds
        return self.label

    def update_location(self, dt):
        g = geocoder.ip("me")  # Get approximate location from IP
        if g.latlng:
            lat, lon = g.latlng
            curr_time = time.time()
            curr_location = (lat, lon)

            if self.prev_location and self.prev_time:
                distance = geodesic(self.prev_location, curr_location).meters
                time_diff = curr_time - self.prev_time
                speed = distance / time_diff if time_diff > 0 else 0  # m/s
                self.label.text = f"Speed: {speed:.2f} m/s ({speed * 3.6:.2f} km/h)"

            self.prev_location = curr_location
            self.prev_time = curr_time
        else:
            self.label.text = "Unable to fetch location."

if __name__ == "__main__":
    Speedometer().run()
