from tkinter import Frame, Label, Entry, Button, messagebox
from passenger_window.ride_status import load_ride_status
import googlemaps
import polyline
import re
import tkintermapview
import requests

API_URL = "https://5c23-2001-4451-411d-7e00-a00-27ff-fe01-7f54.ngrok-free.app"
API_KEY = "AIzaSyBQ2_ZV6KF2HQKy8qoewGXBJAcmJf__vSg" 

gmaps = googlemaps.Client(key=API_KEY)

def load_home(frame, uid):
    for widget in frame.winfo_children():
        widget.destroy()

    selected = {"vehicle": None}
    locations = {"pickup": None, "destination": None}

    top_frame = Frame(frame)
    top_frame.pack(pady=10)

    Label(top_frame, text="Pickup Location").pack()
    pickup_entry = Entry(top_frame, width=60)
    pickup_entry.pack(pady=(0, 10))

    Label(top_frame, text="Destination").pack()
    destination_entry = Entry(top_frame, width=60)
    destination_entry.pack(pady=(0, 10))

    Label(top_frame, text="Select Vehicle Type").pack(pady=(10, 5))

    def select_vehicle(vehicle):
        selected["vehicle"] = vehicle
        messagebox.showinfo("Vehicle Selected", f"You selected: {vehicle}")

    # palitan nyo nlng dto
    for vehicle in ["motorcycle", "car4", "car6", "tank"]:
        Button(top_frame, text=vehicle, width=20, command=lambda v=vehicle: select_vehicle(v)).pack(pady=2)

    route_label = Label(top_frame, text="", justify="left", font=("Arial", 10))
    route_label.pack(pady=10)

    map_widget = tkintermapview.TkinterMapView(frame, width=800, height=400, corner_radius=0)
    map_widget.pack(pady=10, fill="both", expand=True)
    map_widget.set_position(11.5, 122.5)
    map_widget.set_zoom(5)

    def confirm_ride():
        #backedn stuff starts
        vehicle = selected["vehicle"]
        if not vehicle:
            messagebox.showerror("Error", "Please select a vehicle before confirming.")
            return

        payload = {
            "user_id": uid,
            "pickup_lat": locations["pickup"]["lat"],
            "pickup_lng": locations["pickup"]["lng"],
            "destination_lat": locations["destination"]["lat"],
            "destination_lng": locations["destination"]["lng"],
            "vehicle": vehicle
        }

        try:
            response = requests.post(f"{API_URL}/sakay/request_ride.php", data=payload)
            data = response.json()

            if data.get("success"):
                rid = data.get("ride_request_id")
                print("RID ISSSSSSSSSSS",rid)
                
                messagebox.showinfo("Success", "Ride requested successfully!")
                load_ride_status(frame, uid, rid)
            else:
                messagebox.showerror("Error", data.get("message", "Request failed"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    confirm_button = Button(top_frame, text="Confirm Ride", state="disabled", command=confirm_ride)
    confirm_button.pack(pady=(5, 0))

    # req route
    def request_ride():
        pickup = pickup_entry.get().strip()
        destination = destination_entry.get().strip()
        vehicle = selected["vehicle"]

        if not pickup or not destination or not vehicle:
            messagebox.showerror("Missing Info", "Please enter pickup, destination, and select a vehicle.")
            return

        try:
            directions_result = gmaps.directions(pickup, destination, mode="driving")
            if not directions_result:
                messagebox.showerror("Error", "No route found.")
                return

            leg = directions_result[0]['legs'][0]
            start_loc = leg['start_location']
            end_loc = leg['end_location']
            polyline_points = directions_result[0]['overview_polyline']['points']
            decoded_points = polyline.decode(polyline_points)

            locations["pickup"] = start_loc
            locations["destination"] = end_loc

            # showmap
            map_widget.set_position(start_loc['lat'], start_loc['lng'])
            map_widget.set_zoom(12)
            map_widget.delete_all_path()
            map_widget.delete_all_marker()
            map_widget.set_marker(start_loc['lat'], start_loc['lng'], text="Pickup")
            map_widget.set_marker(end_loc['lat'], end_loc['lng'], text="Destination")
            map_widget.set_path(decoded_points)

            # update routing and stuff
            distance = leg['distance']['text']
            duration = leg['duration']['text']
            route_label.config(text=f"Route: {distance}, {duration}")
            confirm_button.config(state="normal")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    Button(top_frame, text="Request Ride", command=request_ride).pack(pady=10)
