from tkinter import Frame, Label, Button

def load_home(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    # Center content holder
    center_frame = Frame(frame)
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Static labels (optional for structure)
    Label(center_frame, text="Driver Home Page").pack(pady=10)

    # Basic buttons
    Button(center_frame, text="Enter Location").pack(pady=5)
    Button(center_frame, text="Go Online").pack(pady=5)

    Label(center_frame, text="Select Vehicle").pack(pady=(20, 5))
    Button(center_frame, text="UFO").pack(pady=2)
    Button(center_frame, text="Tank").pack(pady=2)
    Button(center_frame, text="Space Shuttle").pack(pady=2)
    Button(center_frame, text="Jet Fighter").pack(pady=2)
