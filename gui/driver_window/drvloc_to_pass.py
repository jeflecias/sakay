from tkinter import Frame, Label, Button, Toplevel
import tkintermapview
import googlemaps
import polyline
import requests
import threading
import time
from driver_window.pricingrules import PricingRules
import json
import os
from datetime import datetime

connect_url = "https://5c23-2001-4451-411d-7e00-a00-27ff-fe01-7f54.ngrok-free.app"
GOOGLE_MAPS_API_KEY = "AIzaSyBQ2_ZV6KF2HQKy8qoewGXBJAcmJf__vSg"
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def reverse_geocode(lat, lng):
    result = gmaps.reverse_geocode((lat, lng))
    if result:
        return result[0]['formatted_address']
    return "Unknown location"

def save_transaction_history(transaction_data):
    """Save transaction to JSON file"""
    try:
        history_file = "transaction_history.json"
        
        # Load existing history if file exists
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = {"transactions": []}
        
        # Add new transaction
        history["transactions"].append(transaction_data)
        
        # Save updated history
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        print(f"Transaction saved to {history_file}")
        return True
        
    except Exception as e:
        print(f"Error saving transaction history: {e}")
        return False

def load_drvloc_to_pass(frame, match_data, back_callback):
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
    
    # Initialize pricing rules
    pricing = PricingRules()
    
    # Variables to store route information for fare calculation
    total_distance_km = 0
    total_duration_min = 0
    ride_start_time = None
    
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
            response = requests.post(f'{connect_url}/sakay/drv_at_pickup.php', data=data)
            
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
        nonlocal ride_start_time
        try:
            # prepare data to send
            data = {
                'driver_id': driver_id,
                'ride_request_id': ride_request_id
            }
            
            # post request to complete ride
            response = requests.post(f'{connect_url}/sakay/complete_ride.php', data=data)
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print("Ride completed successfully!")
                    status_label.config(text="Status: Ride Completed ✓")
                    done_button.config(state='disabled', text="Completed ✓", bg="gray")
                    
                    # Calculate fare based on vehicle type
                    fare = 0
                    if vehicle_type == 'motorcycle':
                        fare = pricing.motorcycle_fare(total_distance_km)
                        fare_type = "Motorcycle"
                    elif vehicle_type == 'car4':
                        fare = pricing.car4_fare(total_distance_km, total_duration_min)
                        fare_type = "Car (4-seater)"
                    elif vehicle_type == 'car6':
                        fare = pricing.car6_fare(total_distance_km, total_duration_min)
                        fare_type = "Car (6-seater)"
                    elif vehicle_type == 'tank':
                        fare = pricing.tank_fare(total_distance_km)
                        fare_type = "Tank"
                    else:
                        fare_type = "Unknown"
                    
                    # Prepare transaction data
                    ride_end_time = datetime.now()
                    transaction_data = {
                        "ride_request_id": ride_request_id,
                        "driver_id": driver_id,
                        "vehicle_type": vehicle_type,
                        "fare_type": fare_type,
                        "distance_km": round(total_distance_km, 2),
                        "duration_minutes": round(total_duration_min, 1),
                        "fare_amount": round(fare, 2),
                        "ride_start_time": ride_start_time.isoformat() if ride_start_time else None,
                        "ride_end_time": ride_end_time.isoformat(),
                        "pickup_location": reverse_geocode(pickup_lat, pickup_lng),
                        "destination_location": reverse_geocode(destination_lat, destination_lng),
                        "driver_start_location": reverse_geocode(driver_lat, driver_lng)
                    }
                    
                    # Show fare in tkinter window
                    show_fare_window(fare, fare_type, total_distance_km, total_duration_min, transaction_data)
                    
                else:
                    print(f"Error: {result['error']}")
            else:
                print(f"HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"Error completing ride: {e}")
    
    def show_fare_window(fare, fare_type, distance_km, duration_min, transaction_data):
        """Display fare information in a new tkinter window"""
        
        fare_window = Toplevel()
        fare_window.title("Ride Completed - Fare Summary")
        fare_window.geometry("400x350")
        fare_window.configure(bg="white")
        
        # Center the window
        fare_window.transient(frame)
        fare_window.grab_set()
        
        # Title
        title_label = Label(fare_window, text="🎉 Ride Completed!", 
                           font=("Arial", 18, "bold"), bg="white", fg="green")
        title_label.pack(pady=20)
        
        # Fare details frame
        details_frame = Frame(fare_window, bg="white")
        details_frame.pack(pady=10, padx=20, fill="x")
        
        # Vehicle type
        Label(details_frame, text=f"Vehicle Type: {fare_type}", 
              font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
        
        # Distance
        Label(details_frame, text=f"Distance: {distance_km:.2f} km", 
              font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
        
        # Duration
        Label(details_frame, text=f"Duration: {duration_min:.1f} minutes", 
              font=("Arial", 12), bg="white").pack(anchor="w", pady=2)
        
        # Separator
        separator = Frame(details_frame, height=2, bg="gray")
        separator.pack(fill="x", pady=10)
        
        # Total fare (highlighted)
        fare_label = Label(details_frame, text=f"Total Fare Earned: ₱{fare:.2f}", 
                          font=("Arial", 16, "bold"), bg="white", fg="blue")
        fare_label.pack(anchor="w", pady=5)
        
        # Status label for save confirmation
        save_status_label = Label(details_frame, text="", 
                                 font=("Arial", 10), bg="white", fg="green")
        save_status_label.pack(anchor="w", pady=5)
        
        # Button frame
        button_frame = Frame(fare_window, bg="white")
        button_frame.pack(pady=20)
        
        # Done button (saves transaction and closes window)
        def on_done_fare_window():
            if save_transaction_history(transaction_data):
                save_status_label.config(text="✓ Transaction saved successfully!")
                fare_window.after(1500, lambda: [fare_window.destroy(), back_callback()])
            else:
                save_status_label.config(text="✗ Error saving transaction", fg="red")
        
        done_button = Button(button_frame, text="Done", 
                            command=on_done_fare_window,
                            bg="blue", fg="white", font=("Arial", 12, "bold"),
                            padx=30, pady=10)
        done_button.pack(side="left", padx=10)
        
        # Close button (closes without saving)
        close_button = Button(button_frame, text="Close", 
                             command=fare_window.destroy,
                             bg="gray", fg="white", font=("Arial", 12, "bold"),
                             padx=30, pady=10)
        close_button.pack(side="left", padx=10)
    
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
        nonlocal total_distance_km, total_duration_min, ride_start_time
        
        try:
            data = {
                'ride_request_id': ride_request_id,
                'driver_id': driver_id
            }
            response = requests.post(
                f'{connect_url}/sakay/check_onboard_status.php',
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                result = response.json()
                if result['success'] and result['passenger_onboard']:
                    print("Passenger is onboard! Updating map...")
                    
                    # Record ride start time
                    ride_start_time = datetime.now()
                    
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
                            
                            # store distance and duration for fare calculation
                            total_distance_km = dest_route['distance']['value'] / 1000  
                            total_duration_min = dest_route['duration']['value'] / 60   

                            # then it continues
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