from tkinter import Frame, Label, Entry, Button, messagebox
import tkintermapview
import requests
import googlemaps
from driver_window.drvstatus_page import load_driver_status
import threading
import time

API_URL = "https://873b-2001-4451-411d-7e00-a00-27ff-fe01-7f54.ngrok-free.app" 
GOOGLE_MAPS_API_KEY = "AIzaSyBQ2_ZV6KF2HQKy8qoewGXBJAcmJf__vSg"  
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def load_driver_home(frame, driver_id):
    for widget in frame.winfo_children():
        widget.destroy()

    selected = {"vehicle": None}
    location_data = {"location": None, "lat": None, "lng": None}

    top_frame = Frame(frame)
    top_frame.pack(pady=10)

    Label(top_frame, text="Enter Your Location").pack()
    location_entry = Entry(top_frame, width=60)
    location_entry.pack(pady=(0, 10))

    Label(top_frame, text="Select Your Vehicle Type").pack(pady=(10, 5))

    def select_vehicle(vehicle):
        selected["vehicle"] = vehicle
        messagebox.showinfo("Vehicle Selected", f"You selected: {vehicle}")

    for vehicle in ["UFO", "Tank", "Space Shuttle", "Jet Fighter"]:
        Button(top_frame, text=vehicle, width=20, command=lambda v=vehicle: select_vehicle(v)).pack(pady=2)

    # Map Widget
    map_widget = tkintermapview.TkinterMapView(frame, width=800, height=400, corner_radius=0)
    map_widget.pack(pady=10, fill="both", expand=True)
    map_widget.set_position(11.5, 122.5)
    map_widget.set_zoom(5)

    # Confirm button (disabled at first)
    confirm_button = Button(top_frame, text="Confirm Go Online", state="disabled")
    confirm_button.pack(pady=10)

    # Load location and show on map
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

            confirm_button.config(state="normal")  # Enable confirmation

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Confirm go online
    def go_online():
        location = location_data["location"]
        vehicle = selected["vehicle"]

        try:
            response = requests.post(f"{API_URL}/sakay/driver_online.php", data={
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

    confirm_button.config(command=go_online)

    # Search/Preview location button
    Button(top_frame, text="Show My Location on Map", command=show_location).pack(pady=5)