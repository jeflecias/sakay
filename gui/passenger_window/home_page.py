from tkinter import Frame, Label, Entry, Button, StringVar

def load_home(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    center_frame = Frame(frame)
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    Label(center_frame, text="Passenger Home").pack(pady=10)

    # Pickup location
    Label(center_frame, text="Pickup Location:").pack()
    pickup_var = StringVar()
    Entry(center_frame, textvariable=pickup_var).pack(pady=5)

    # Destination
    Label(center_frame, text="Destination:").pack()
    destination_var = StringVar()
    Entry(center_frame, textvariable=destination_var).pack(pady=5)

    # Ride Status
    ride_status = StringVar(value="Ride status will appear here.")

    def request_ride():
        pickup = pickup_var.get().strip()
        destination = destination_var.get().strip()
        if not pickup or not destination:
            ride_status.set("Please enter both pickup and destination.")
        else:
            # Simulate searching
            ride_status.set("Searching for a driver...")

    Button(center_frame, text="Request Ride", command=request_ride).pack(pady=10)

    Label(center_frame, textvariable=ride_status).pack(pady=(20, 5))
