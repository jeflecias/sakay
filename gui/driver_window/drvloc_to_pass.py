from tkinter import Frame, Label, Button
import tkintermapview
import googlemaps
import polyline
import requests
import threading
import time
import json

GOOGLE_MAPS_API_KEY = "AIzaSyBQ2_ZV6KF2HQKy8qoewGXBJAcmJf__vSg"
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def load_drvloc_to_pass(frame, match_data):
    for widget in frame.winfo_children():
        widget.destroy()
    
    # extract coords
    driver_lat = float(match_data['driver_start_lat'])
    driver_lng = float(match_data['driver_start_lng'])
    pickup_lat = float(match_data['pickup_lat'])
    pickup_lng = float(match_data['pickup_lng'])
    destination_lat = float(match_data['destination_lat'])
    destination_lng = float(match_data['destination_lng'])
    ride_request_id = match_data['ride_request_id']
    vehicle_type = match_data['vehicle_type']
    driver_id = match_data.get('driver_id')
    
    top_frame = Frame(frame)
    top_frame.pack(pady=10)
    
    Label(top_frame, text="Heading to Pickup Location", font=("Arial", 16, "bold")).pack(pady=5)
    Label(top_frame, text=f"Ride Request ID: {ride_request_id}").pack(pady=2)
    Label(top_frame, text=f"Vehicle Type: {vehicle_type}").pack(pady=2)
    
    # status
    status_label = Label(top_frame, text="Loading route...", font=("Arial", 12))
    status_label.pack(pady=5)
    
    # arrived button
    def on_arrived():
        try:
            # prepare this to send
            data = {
                'driver_id': driver_id,
                'ride_request_id': ride_request_id
            }
            
            # usual post req
            response = requests.post('https://7938-112-200-227-68.ngrok-free.app/sakay/drv_at_pickup.php', data=data)
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print("Driver progress updated to 'arrived' successfully")
                    status_label.config(text="Status: Arrived at pickup location")
                    arrived_button.config(state='disabled', text="Arrived ✓")
                else:
                    print(f"Error: {result['error']}")
            else:
                print(f"HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    arrived_button = Button(top_frame, text="Arrived", command=on_arrived, 
                           bg="green", fg="white", font=("Arial", 12, "bold"),
                           padx=20, pady=10)
    arrived_button.pack(pady=10)
    
    # unpressable done button (will be enabled when passenger is onboard)
    def on_done():
        try:
            # prepare data to send
            data = {
                'driver_id': driver_id,
                'ride_request_id': ride_request_id
            }
            
            # post request to complete ride
            response = requests.post('https://7938-112-200-227-68.ngrok-free.app/sakay/complete_ride.php', data=data)
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print("Ride completed successfully!")
                    status_label.config(text="Status: Ride Completed ✓")
                    done_button.config(state='disabled', text="Completed ✓", bg="gray")
                else:
                    print(f"Error: {result['error']}")
            else:
                print(f"HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"Error completing ride: {e}")
    
    done_button = Button(top_frame, text="Done", command=on_done, state='disabled',
                        bg="gray", fg="white", font=("Arial", 12, "bold"),
                        padx=20, pady=10)
    done_button.pack(pady=5)
    
    # mapwidget
    map_widget = tkintermapview.TkinterMapView(frame, width=800, height=400, corner_radius=0)
    map_widget.pack(pady=10, fill="both", expand=True)
    
    # set map pos and zoom
    center_lat = (driver_lat + pickup_lat) / 2
    center_lng = (driver_lng + pickup_lng) / 2
    map_widget.set_position(center_lat, center_lng)
    map_widget.set_zoom(13)
    
    # add markers
    driver_marker = map_widget.set_marker(driver_lat, driver_lng, text=" Your Location", marker_color_circle="blue")
    pickup_marker = map_widget.set_marker(pickup_lat, pickup_lng, text=" Pickup Location", marker_color_circle="red")
    
    # get coords directions
    route_path = None
    try:
        directions = gmaps.directions(
            origin=(driver_lat, driver_lng),
            destination=(pickup_lat, pickup_lng),
            mode="driving"
        )
        
        if directions:
            route = directions[0]['legs'][0]
            distance = route['distance']['text']
            duration = route['duration']['text']
            
            status_label.config(text=f"Distance: {distance} | ETA: {duration}")
            
            # polyline to match didnot work earlier it was just a STRAIGHTLINE?
            encoded_polyline = directions[0]['overview_polyline']['points']
            decoded_coordinates = polyline.decode(encoded_polyline)
            
            # drawing
            route_path = map_widget.set_path(decoded_coordinates, color="blue", width=3)
        else:
            status_label.config(text="Could not calculate route")
            
    except Exception as e:
        print(f"Error: {e}")
        status_label.config(text="Error loading route")

    def check_passenger_onboard():
        try:
            data = {
                'ride_request_id': ride_request_id,
                'driver_id': driver_id
            }
            response = requests.post(
                'https://7938-112-200-227-68.ngrok-free.app/sakay/check_onboard_status.php',
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                result = response.json()
                if result['success'] and result['passenger_onboard']:
                    print("Passenger is onboard! Updating map...")
                    
                    # clear previous
                    map_widget.delete_all_marker()
                    map_widget.delete_all_path()
                    
                    # add new markers
                    map_widget.set_marker(pickup_lat, pickup_lng, text=" Pickup Location", marker_color_circle="green")
                    map_widget.set_marker(destination_lat, destination_lng, text=" Destination", marker_color_circle="red")
                    
                    # get route from pickup to desti
                    try:
                        dest_directions = gmaps.directions(
                            origin=(pickup_lat, pickup_lng),
                            destination=(destination_lat, destination_lng),
                            mode="driving"
                        ) 
                        if dest_directions:
                            dest_route = dest_directions[0]['legs'][0]
                            dest_distance = dest_route['distance']['text']
                            dest_duration = dest_route['duration']['text']
                            status_label.config(text=f"To Destination - Distance: {dest_distance} | ETA: {dest_duration}")
                            dest_encoded_polyline = dest_directions[0]['overview_polyline']['points']
                            dest_decoded_coordinates = polyline.decode(dest_encoded_polyline)
                            map_widget.set_path(dest_decoded_coordinates, color="red", width=3)
                            center_lat = (pickup_lat + destination_lat) / 2
                            center_lng = (pickup_lng + destination_lng) / 2
                            map_widget.set_position(center_lat, center_lng)
                            map_widget.set_zoom(13)
                            
                    except Exception as e:
                        print(f"Error getting destination route: {e}")
                    
                    done_button.config(state='normal', bg="blue")
                    for widget in top_frame.winfo_children():
                        if isinstance(widget, Label) and "Heading to Pickup Location" in widget.cget("text"):
                            widget.config(text="Passenger Onboard - Heading to Destination")
                            break

                    return True  
            return False  
        
        except Exception as e:
            print(f"Error checking passenger onboard status: {e}")
            return False
    
    #thread run continuously if onboard
    def monitor_driver_progress():
        passenger_onboard = False
        while not passenger_onboard:
            try:
                print(f"Driver Progress: {match_data.get('driver_progress', 'unknown')}")
                passenger_onboard = check_passenger_onboard()
                if not passenger_onboard:
                    time.sleep(5)  
            except Exception as e:
                print(f"[Progress Monitor Error]: {e}")
                time.sleep(5)
    
    # start threads 
    progress_thread = threading.Thread(target=monitor_driver_progress, daemon=True)
    progress_thread.start()