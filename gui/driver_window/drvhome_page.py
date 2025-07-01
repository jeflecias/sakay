from tkinter import Frame, Label, Button, Entry, messagebox

def load_home(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    # Center content holder
    center_frame = Frame(frame)
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    Label(center_frame, text="Driver Home Page").pack(pady=10)

    # Entry field for location
    Label(center_frame, text="Enter your location:").pack()
    location_entry = Entry(center_frame)
    location_entry.pack(pady=5)

    # Go Online button logic
    def go_online():
        location = location_entry.get().strip()
        if not location:
            messagebox.showerror("Missing Info", "Please enter your location before going online.")
            return
        print(f"Driver is now online at location: {location}")

    Button(center_frame, text="Go Online", command=go_online).pack(pady=5)

    # Vehicle selection
    Label(center_frame, text="Select Vehicle").pack(pady=(20, 5))
    Button(center_frame, text="UFO").pack(pady=2)
    Button(center_frame, text="Tank").pack(pady=2)
    Button(center_frame, text="Space Shuttle").pack(pady=2)
    Button(center_frame, text="Jet Fighter").pack(pady=2)
