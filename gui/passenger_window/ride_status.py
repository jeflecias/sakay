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

def load_ride_status(frame, uid, rid):
    print(f"Loading ride status for UID: {uid}, RID: {rid}")
    
    for widget in frame.winfo_children():
        widget.destroy()
    
    # constants for later use
    ping_control = {"should_ping": True}
    driver_found_popup_shown = {"shown": False}
    status_label = Label(frame, text="Looking for a driver...", font=("Arial", 14))
    status_label.pack(pady=20)
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    
    # create map widget ui
    def create_map_widget():
        frame.update_idletasks()
        map_widget = tkintermapview.TkinterMapView(
            frame, 
            width=800, 
            height=400, 
            corner_radius=0
        )
        map_widget.pack(pady=10, fill="both", expand=True)
        
        # set initial pos
        frame.after(100, lambda: map_widget.set_position(11.5, 122.5))
        frame.after(200, lambda: map_widget.set_zoom(5))
        
        return map_widget
    
    map_widget = create_map_widget()
    
    def ping_passenger():
        while ping_control["should_ping"]:
            try:
                print(f"Pinging passenger for UID: {uid}, RID: {rid}")
                response = requests.post(f"{API_URL}/sakay/ping_passenger.php", data={
                    "user_id": uid,
                    "ride_id": rid
                }, timeout=10)
            except requests.RequestException as e:
                print(f"Ping error: {e}")
            time.sleep(10)
    
    def get_route_polyline(start_coords, end_coords):
        # Validate coordinate inputs
        start_lat = float(start_coords.get('lat', 0))
        start_lng = float(start_coords.get('lng', 0))
        end_lat = float(end_coords.get('lat', 0))
        end_lng = float(end_coords.get('lng', 0))
        
        # check if coords are valid ran an error previously
        if (start_lat == 0 or start_lng == 0 or end_lat == 0 or end_lng == 0 or
            not (-90 <= start_lat <= 90) or not (-180 <= start_lng <= 180) or
            not (-90 <= end_lat <= 90) or not (-180 <= end_lng <= 180)):
            print("Invalid coordinates")
            return None, None, None
        
        print(f"Getting route from ({start_lat}, {start_lng}) to ({end_lat}, {end_lng})")
        
        try:
            # gmap direcs
            directions_result = gmaps.directions(
                origin=(start_lat, start_lng),
                destination=(end_lat, end_lng),
                mode="driving",
                departure_time="now"
            )
            
            if not directions_result:
                return None, None, None
            
            # extract polyline
            route = directions_result[0]
            if 'overview_polyline' not in route or 'points' not in route['overview_polyline']:
                return None, None, None
                
            encoded_polyline = route['overview_polyline']['points']
            print(f"Encoded polyline: {encoded_polyline[:50]}...")
            
            # polyline to coords
            decoded_coords = polyline.decode(encoded_polyline)
            print(f"Decoded {len(decoded_coords)} coordinate points")
            
            # validate coords
            valid_coords = [(lat, lng) for lat, lng in decoded_coords 
                          if -90 <= lat <= 90 and -180 <= lng <= 180]
            
            if not valid_coords:
                return None, None, None
            
            # get distance
            leg = route['legs'][0]
            distance = leg['distance']['text']
            duration = leg['duration']['text']
            
            return valid_coords, distance, duration
            
        except Exception as e:
            print(f"Google Maps API error: {e}")
            return None, None, None
    
    def calculate_distance(lat1, lon1, lat2, lon2):
        R = 6371  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    marker_refs = {"driver": None, "pickup": None, "destination": None}
    map_initialized = {"status": False}
    
    def update_map_with_coords(pickup_coords, destination_coords, driver_coords):
        """Update map with persistent markers"""
        if not map_widget:
            return
            
        print(f"Updating map with pickup: {pickup_coords}, destination: {destination_coords}, driver: {driver_coords}")
        
        def validate_coords(coords, name):
            if not coords or not isinstance(coords, dict):
                return None
            
            lat = float(coords.get('lat', 0))
            lng = float(coords.get('lng', 0))
            
            if (lat == 0 or lng == 0 or 
                not (-90 <= lat <= 90) or not (-180 <= lng <= 180)):
                return None
                
            return (lat, lng)
        
        pickup_pos = validate_coords(pickup_coords, "pickup")
        destination_pos = validate_coords(destination_coords, "destination")
        driver_pos = validate_coords(driver_coords, "driver")
        
        if not pickup_pos or not destination_pos or not driver_pos:
            frame.after(0, lambda: status_label.config(text="Driver en route - Invalid coordinates"))
            return
        
        pickup_lat, pickup_lng = pickup_pos
        destination_lat, destination_lng = destination_pos
        driver_lat, driver_lng = driver_pos
        
        def initialize_map():

            if not map_initialized["status"]:
                center_lat = (driver_lat + pickup_lat) / 2
                center_lng = (driver_lng + pickup_lng) / 2
                map_widget.set_position(center_lat, center_lng)
                map_widget.set_zoom(13)
                
                marker_refs["driver"] = map_widget.set_marker(driver_lat, driver_lng, text="Driver", marker_color_circle="blue")
                marker_refs["pickup"] = map_widget.set_marker(pickup_lat, pickup_lng, text="Pickup", marker_color_circle="red")
                marker_refs["destination"] = map_widget.set_marker(destination_lat, destination_lng, text="Destination", marker_color_circle="green")
                
                map_initialized["status"] = True
                print("Map initialized with markers")
            else:
                marker_refs["driver"].set_position(driver_lat, driver_lng)
                marker_refs["pickup"].set_position(pickup_lat, pickup_lng)
                marker_refs["destination"].set_position(destination_lat, destination_lng)
        
        map_widget.delete_all_path()
        frame.after(50, initialize_map)
        
        #polyline from driver to pickup
        route_coords, distance, duration = get_route_polyline(driver_coords, pickup_coords)
        
        def update_route():
            if route_coords and len(route_coords) > 1:
                map_widget.set_path(route_coords, color="blue", width=3)
                status_label.config(text=f"Driver en route | Distance: {distance} | ETA: {duration}")
            else:
                straight_distance = calculate_distance(driver_lat, driver_lng, pickup_lat, pickup_lng)
                path_coords = [(driver_lat, driver_lng), (pickup_lat, pickup_lng)]
                map_widget.set_path(path_coords, color="blue", width=3)
                status_label.config(text=f"Driver en route | Distance: {straight_distance:.1f} km")
            
            # route from pickup to desti
            if not map_initialized.get("destination_route_added", False):
                pickup_to_dest_route, _, _ = get_route_polyline(pickup_coords, destination_coords)
                if pickup_to_dest_route and len(pickup_to_dest_route) > 1:
                    map_widget.set_path(pickup_to_dest_route, color="green", width=2)
                    map_initialized["destination_route_added"] = True
        
        frame.after(100, update_route)
    
    # update gui with coords
    def update_gui_with_coords(data):
        if not driver_found_popup_shown["shown"]:
            messagebox.showinfo("Driver Found!", "A driver has been found and is heading to your location!")
            driver_found_popup_shown["shown"] = True
        
        # update map with routes
        update_map_with_coords(
            data.get('pickup_coords', {}),
            data.get('destination_coords', {}),
            data.get('driver_current_coords', {})
        )
    
    def check_ride_coords():
        while ping_control["should_ping"]:
            try:
                print(f"Checking ride coords for UID: {uid}, RID: {rid}")
                response = requests.get(f"{API_URL}/sakay/psg_getride.php?user_id={uid}&rid={rid}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        frame.after(0, lambda: update_gui_with_coords(data))
            except requests.RequestException as e:
                print(f"Ride coords error: {e}")
            time.sleep(5)
    
    def enable_ride_button():
        print("Driver has arrived! Enabling button...")
        ride_button.config(state="normal", bg="green", command=start_ride)
        status_label.config(text="Driver has arrived! You can now start the ride.")
    
    def check_driver_arrival():
        while ping_control["should_ping"]:
            try:
                print(f"Checking driver arrival for RID: {rid}")
                response = requests.get(f"{API_URL}/sakay/check_driver_arrived.php?ride_id={rid}", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('driver_arrived'):
                        frame.after(0, enable_ride_button)
                        break
                        
            except requests.RequestException as e:
                print(f"Driver arrival check error: {e}")
            time.sleep(3)
    
    def start_ride():
        try:
            print(f"Starting ride for UID: {uid}, RID: {rid}")
            response = requests.post(f"{API_URL}/sakay/update_passenger_onboard.php", data={
                "user_id": uid,
                "ride_id": rid
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    status_label.config(text="Ride started! You are now onboard.")
                    ride_button.config(state="disabled", bg="gray", text="Ride In Progress")
                    messagebox.showinfo("Ride Started", "Your ride has started! Enjoy your trip.")
                else:
                    messagebox.showerror("Error", data.get('message', 'Failed to start ride'))
            else:
                messagebox.showerror("Error", "Failed to connect to server")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to start ride: {str(e)}")
    
    def cleanup_and_cancel():
        #stop threads
        ping_control["should_ping"] = False

        if map_widget:
            map_widget.delete_all_marker()
            map_widget.delete_all_path()
            marker_refs["driver"] = None
            marker_refs["pickup"] = None
            marker_refs["destination"] = None
            map_initialized["status"] = False
            map_widget.destroy()
        
        try:
            requests.post(f"{API_URL}/sakay/cancel_ride.php", data={
                "user_id": uid,
                "ride_id": rid
            }, timeout=5)
        except requests.RequestException:
            pass
        
        time.sleep(0.5)
        
        try:
            from passenger_window.home_page import load_home
            load_home(frame, uid)
        except ImportError:
            # Fallback cleanup
            for widget in frame.winfo_children():
                widget.destroy()
            Label(frame, text="Ride cancelled", font=("Arial", 14)).pack(pady=20)
    
    # continuously checks if ride is done if so enable button
    def check_ride_completion(ride_id, user_id):
        try:
            response = requests.get(f"{API_URL}/sakay/check_ride_completion.php?ride_id={ride_id}&user_id={user_id}", timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "message": "Server error"}
                
        except requests.RequestException as e:
            return {"success": False, "message": str(e)}
        
    # button enabler only comes on if check_ride_completion returns success
    def enable_finish_trip_button():
        print("Ride completed! Enabling finish trip button...")
        finish_trip_button.config(state="normal", bg="orange", command=finish_trip)
        status_label.config(text="Ride completed! You can now finish your trip.")

    # checks status completion
    def check_ride_completion_status():
        while ping_control["should_ping"]:
            completion_data = check_ride_completion(rid, uid)
            
            if completion_data.get('success') and completion_data.get('can_finish_trip'):
                frame.after(0, enable_finish_trip_button)
                break
            
            time.sleep(5)

    # finish then save to history then delete
    def finish_trip():
        try:
            print(f"Finishing trip for UID: {uid}, RID: {rid}") 
            response = requests.post(f"{API_URL}/sakay/finalize_trip.php", data={
                "user_id": uid,
                "ride_id": rid
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    status_label.config(text="Trip completed successfully!")
                    finish_trip_button.config(state="disabled", bg="gray", text="Trip Completed")
                    messagebox.showinfo("Trip Completed", "Thank you for using our service!")
                    
                    from passenger_window.home_page import load_home
                    frame.after(3000, lambda: load_home(frame, uid))
                else:
                    messagebox.showerror("Error", data.get('message', 'Failed to complete trip'))
            else:
                messagebox.showerror("Error", "Failed to connect to server")
                
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to complete trip: {str(e)}")

    # finish trip button
    finish_trip_button = Button(frame, text="Finish Trip", state="disabled", bg="gray", fg="white")
    finish_trip_button.pack(pady=5)

    # threads running here
    threading.Thread(target=ping_passenger, daemon=True).start()
    threading.Thread(target=check_ride_coords, daemon=True).start()
    threading.Thread(target=check_driver_arrival, daemon=True).start()
    threading.Thread(target=check_ride_completion_status, daemon=True).start()
    
    # create ride button
    ride_button = Button(frame, text="Ride", state="disabled", bg="gray", fg="white")
    ride_button.pack(pady=5)
    
    Button(frame, text="Cancel Ride", command=cleanup_and_cancel, bg="red", fg="white").pack(pady=10)