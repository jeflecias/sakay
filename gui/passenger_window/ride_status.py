from tkinter import Frame, Label, Button, messagebox
import requests
import threading
import time
import tkintermapview
import googlemaps
import polyline
import math

API_URL = "https://7938-112-200-227-68.ngrok-free.app" 
GOOGLE_MAPS_API_KEY = "AIzaSyBQ2_ZV6KF2HQKy8qoewGXBJAcmJf__vSg"

try:
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
except:
    gmaps = None

def load_ride_status(frame, uid, rid):
    print(f"Loading ride status for UID: {uid}, RID: {rid}")
    
    for widget in frame.winfo_children():
        widget.destroy()
    
    ping_control = {"should_ping": True}
    driver_found_popup_shown = {"shown": False}
    
    status_label = Label(frame, text="Looking for a driver...", font=("Arial", 14))
    status_label.pack(pady=20)
    
    try:
        map_widget = tkintermapview.TkinterMapView(frame, width=800, height=400, corner_radius=0)
        map_widget.pack(pady=10, fill="both", expand=True)
        map_widget.set_position(11.5, 122.5)  # Philippines center
        map_widget.set_zoom(5)
    except:
        map_widget = None
        error_label = Label(frame, text="Map unavailable", font=("Arial", 12))
        error_label.pack(pady=10)
    
    def ping_passenger():
        while ping_control["should_ping"]:
            try:
                requests.post(f"{API_URL}/sakay/ping_passenger.php", data={
                    "user_id": uid,
                    "ride_id": rid
                }, timeout=10)
            except:
                pass
            time.sleep(10)
    
    def update_map_with_coords(pickup_coords, destination_coords, driver_coords):
        if not map_widget:
            return
            
        try:
            # clear some other markers if any
            map_widget.delete_all_marker()
            map_widget.delete_all_path()
            
            # coords
            pickup_lat = float(pickup_coords.get('lat', 0))
            pickup_lng = float(pickup_coords.get('lng', 0))
            destination_lat = float(destination_coords.get('lat', 0))
            destination_lng = float(destination_coords.get('lng', 0))
            driver_lat = float(driver_coords.get('lat', 0))
            driver_lng = float(driver_coords.get('lng', 0))
            
            # setmap center looked messy backthen
            center_lat = (driver_lat + pickup_lat) / 2
            center_lng = (driver_lng + pickup_lng) / 2
            map_widget.set_position(center_lat, center_lng)
            map_widget.set_zoom(13)
            
            # add markers
            map_widget.set_marker(driver_lat, driver_lng, text="Driver", marker_color_circle="blue")
            map_widget.set_marker(pickup_lat, pickup_lng, text="Pickup", marker_color_circle="red")
            map_widget.set_marker(destination_lat, destination_lng, text="Destination", marker_color_circle="green")
            
            # disatance calculator
            def calculate_distance(lat1, lon1, lat2, lon2):
                R = 6371  
                dlat = math.radians(lat2 - lat1)
                dlon = math.radians(lon2 - lon1)
                a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                return R * c
            
            distance = calculate_distance(driver_lat, driver_lng, pickup_lat, pickup_lng)
            status_label.config(text=f"Driver en route | Distance: {distance:.1f} km")
            
            # drawpath
            path_coords = [(driver_lat, driver_lng), (pickup_lat, pickup_lng)]
            map_widget.set_path(path_coords, color="blue", width=3)
            
        except:
            status_label.config(text="Driver en route - Map update failed")
    
    def check_ride_coords():
        while ping_control["should_ping"]:
            try:
                response = requests.get(f"{API_URL}/sakay/psg_getride.php?user_id={uid}&rid={rid}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        # Show popup only once
                        if not driver_found_popup_shown["shown"]:
                            messagebox.showinfo("Driver Found!", "A driver has been found and is heading to your location!")
                            driver_found_popup_shown["shown"] = True
                        
                        # Update map
                        update_map_with_coords(
                            data.get('pickup_coords', {}),
                            data.get('destination_coords', {}),
                            data.get('driver_current_coords', {})
                        )
            except:
                pass
            time.sleep(5)
    
    def cancel_ride():
        ping_control["should_ping"] = False
        
        try:
            requests.post(f"{API_URL}/sakay/cancel_ride.php", data={
                "user_id": uid,
                "ride_id": rid
            }, timeout=10)
        except:
            pass
        
        try:
            from passenger_window.home_page import load_home
            load_home(frame, uid)
        except:
            for widget in frame.winfo_children():
                widget.destroy()
            Label(frame, text="Ride cancelled", font=("Arial", 14)).pack(pady=20)
    
    # Start background threads
    threading.Thread(target=ping_passenger, daemon=True).start()
    threading.Thread(target=check_ride_coords, daemon=True).start()
    
    # Cancel button
    Button(frame, text="Cancel Ride", command=cancel_ride, bg="red", fg="white").pack(pady=10)