from tkinter import Frame, Label, Button
import tkintermapview
import googlemaps
import polyline
import requests
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
                'driver_id': match_data.get('driver_id'),
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
    
    # mapwidget
    map_widget = tkintermapview.TkinterMapView(frame, width=800, height=400, corner_radius=0)
    map_widget.pack(pady=10, fill="both", expand=True)
    
    # set map pos and zoom
    center_lat = (driver_lat + pickup_lat) / 2
    center_lng = (driver_lng + pickup_lng) / 2
    map_widget.set_position(center_lat, center_lng)
    map_widget.set_zoom(13)
    
    # add markers
    map_widget.set_marker(driver_lat, driver_lng, text=" Your Location", marker_color_circle="blue")
    map_widget.set_marker(pickup_lat, pickup_lng, text=" Pickup Location", marker_color_circle="red")
    
    # get coords directions
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
            map_widget.set_path(decoded_coordinates, color="blue", width=3)
        else:
            status_label.config(text="Could not calculate route")
            
    except Exception as e:
        print(f"Error: {e}")
        status_label.config(text="Error loading route")