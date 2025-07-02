import requests
from tkinter import Frame, Label, Button, Entry, messagebox
from driver_window.drvstatus_page import load_driver_status

# skeleton edit nyo nalang binura ko mga pics and stuff

selected = {"vehicle": None}
connect_url = "urlhere"

def load_home(frame, driver_id):
    for widget in frame.winfo_children():
        widget.destroy()

    center_frame = Frame(frame)
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    Label(center_frame, text="Driver Home Page").pack(pady=10)

    Label(center_frame, text="Enter your location:").pack()
    location_entry = Entry(center_frame)
    location_entry.pack(pady=5)

    Label(center_frame, text="Select Vehicle").pack(pady=(20, 5))

    def select_vehicle(vehicle_name):
        selected["vehicle"] = vehicle_name

    for vehicle in ["UFO", "Tank", "Space Shuttle", "Jet Fighter"]:
        Button(center_frame, text=vehicle, command=lambda v=vehicle: select_vehicle(v)).pack(pady=2)

    def go_online():
        location = location_entry.get().strip()
        vehicle = selected["vehicle"]

        if not location or not vehicle:
            messagebox.showerror("Missing Info", "Enter location and vehicle.")
            return

        # send to backend WAG NYONG PAPAKAILAMAN TO
        try:
            response = requests.post(f"{connect_url}/sakay/go_online.php", data={
                "driver_id": driver_id,
                "location": location,
                "vehicle": vehicle
            })
            res = response.json()
            if res.get("success"):
                load_driver_status(frame, driver_id, location, vehicle, lambda: load_home(frame, driver_id))
            else:
                messagebox.showerror("Error", res.get("message", "Unknown error"))
        except Exception as e:
            messagebox.showerror("Error", f"Server error: {e}")

    Button(center_frame, text="Go Online", command=go_online).pack(pady=20)
