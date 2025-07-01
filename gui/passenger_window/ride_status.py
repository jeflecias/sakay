from tkinter import Frame, Label, Button

def load_ride_status(frame):
    # lazy import walang error life hack
    
    from passenger_window.home_page import load_home  
    for widget in frame.winfo_children():
        widget.destroy()

    center_frame = Frame(frame)
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    # ride status info
    Label(center_frame, text="Looking for a driver...").pack(pady=(10, 5))
    Label(center_frame, text="Driver location will appear here").pack(pady=(0, 10))

    # cancel button
    Button(center_frame, text="Cancel Ride", command=lambda: load_home(frame)).pack(pady=10)
