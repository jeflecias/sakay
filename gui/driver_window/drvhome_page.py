from tkinter import Frame, Label, Button, Entry, messagebox
from driver_window.drvstatus_page import load_driver_status

selected = {"vehicle": None}

def load_home(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    center_frame = Frame(frame)
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    Label(center_frame, text="Driver Home Page").pack(pady=10)

    # Location input
    Label(center_frame, text="Enter your location:").pack()
    location_entry = Entry(center_frame)
    location_entry.pack(pady=5)

    # Vehicle selection
    Label(center_frame, text="Select Vehicle").pack(pady=(20, 5))

    def select_vehicle(vehicle_name):
        selected["vehicle"] = vehicle_name
        print(f"Selected vehicle: {vehicle_name}")

    Button(center_frame, text="UFO", command=lambda: select_vehicle("UFO")).pack(pady=2)
    Button(center_frame, text="Tank", command=lambda: select_vehicle("Tank")).pack(pady=2)
    Button(center_frame, text="Space Shuttle", command=lambda: select_vehicle("Space Shuttle")).pack(pady=2)
    Button(center_frame, text="Jet Fighter", command=lambda: select_vehicle("Jet Fighter")).pack(pady=2)

    # Go Online logic
    def go_online():
        location = location_entry.get().strip()
        vehicle = selected["vehicle"]

        if not location:
            messagebox.showerror("Missing Info", "Please enter your location.")
            return
        if not vehicle:
            messagebox.showerror("Missing Info", "Please select a vehicle.")
            return

        # Load status page
        def back_to_home():
            load_home(frame)

        load_driver_status(frame, location, vehicle, back_to_home)

    Button(center_frame, text="Go Online", command=go_online).pack(pady=20)
