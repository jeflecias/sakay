from tkinter import Frame, Label, Entry, Button
from passenger_window.ride_status import load_ride_status

def load_home(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    center_frame = Frame(frame)
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    # pickup loc
    Label(center_frame, text="Pickup Location").pack(pady=(10, 0))
    pickup_entry = Entry(center_frame)
    pickup_entry.pack(pady=(0, 10))

    # to where
    Label(center_frame, text="Destination").pack()
    destination_entry = Entry(center_frame)
    destination_entry.pack(pady=(0, 10))

    # request ride button goes to ridestatus
    Button(center_frame, text="Request Ride", command=lambda: load_ride_status(frame)).pack(pady=10)
