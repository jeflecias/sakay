from tkinter import Frame, Label, Entry, Button, messagebox
import tkintermapview
import requests
import googlemaps
from driver_window.drvstatus_page import load_driver_status
import threading
import time

connect_url = "https://5c23-2001-4451-411d-7e00-a00-27ff-fe01-7f54.ngrok-free.app" 
GOOGLE_MAPS_API_KEY = "AIzaSyBQ2_ZV6KF2HQKy8qoewGXBJAcmJf__vSg"  
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def load_driver_home(frame, driver_id):
    for widget in frame.winfo_children():
        widget.destroy()

    selected = {"vehicle": None}
    location_data = {"location": None, "lat": None, "lng": None}

    # Create main container with fixed layout
    main_container = Frame(frame)
    main_container.pack(fill="both", expand=True, padx=10, pady=10)

    # Top section for controls (fixed height)
    top_frame = Frame(main_container, bg="#D2B48C")
    top_frame.pack(fill="x", pady=(0, 10))

    Label(top_frame, text="Enter Your Location", bg="#D2B48C").pack()
    location_entry = Entry(top_frame, width=60)
    location_entry.pack(pady=(0, 10))

    Label(top_frame, text="Select Your Vehicle Type", bg="#D2B48C").pack(pady=(10, 5))

    def select_vehicle(vehicle):
        selected["vehicle"] = vehicle
        messagebox.showinfo("Vehicle Selected", f"You selected: {vehicle}")

    # Vehicle buttons in a row
    vehicle_frame = Frame(top_frame, bg="#D2B48C")
    vehicle_frame.pack(pady=5)
    
    for vehicle in ["motorcycle", "car4", "car6", "tank"]:
        Button(vehicle_frame, text=vehicle, width=15, 
               command=lambda v=vehicle: select_vehicle(v)).pack(side="left", padx=5)

    # Button controls
    button_frame = Frame(top_frame, bg="#D2B48C")
    button_frame.pack(pady=10)

    show_location_btn = Button(button_frame, text="Show My Location on Map")
    show_location_btn.pack(side="left", padx=5)

    confirm_button = Button(button_frame, text="Confirm Go Online", state="disabled")
    confirm_button.pack(side="left", padx=5)

    # Map section (fixed size, not expanding)
    map_frame = Frame(main_container, bg="#D2B48C")
    map_frame.pack(fill="both", expand=True)

    map_widget = tkintermapview.TkinterMapView(map_frame, width=800, height=300, corner_radius=0)
    map_widget.pack(pady=5)
    map_widget.set_position(11.5, 122.5)
    map_widget.set_zoom(5)

    def show_location():
        location = location_entry.get().strip()
        vehicle = selected["vehicle"]

        if not location or not vehicle:
            messagebox.showerror("Missing Info", "Please enter your location and select a vehicle.")
            return

        try:
            geocode_result = gmaps.geocode(location)
            if not geocode_result:
                messagebox.showerror("Error", "Location not found.")
                return

            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            location_data.update({"location": location, "lat": lat, "lng": lng})

            map_widget.set_position(lat, lng)
            map_widget.set_zoom(14)
            map_widget.delete_all_marker()
            map_widget.set_marker(lat, lng, text="Your Location")

            confirm_button.config(state="normal")  

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def go_online():
        location = location_data["location"]
        vehicle = selected["vehicle"]

        try:
            response = requests.post(f"{connect_url}/sakay/driver_online.php", data={
                "driver_id": driver_id,
                "current_lat": location_data["lat"],
                "current_lng": location_data["lng"],
                "vehicle": vehicle
            })
            result = response.json()

            if result.get("success"):
                load_driver_status(
                    frame, driver_id, location, vehicle,
                    back_callback=lambda: load_driver_home(frame, driver_id)
                )
            else:
                messagebox.showerror("Error", result.get("message", "Could not go online."))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Connect button commands
    show_location_btn.config(command=show_location)
    confirm_button.config(command=go_online)