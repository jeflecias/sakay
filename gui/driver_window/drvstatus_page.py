from tkinter import Frame, Label, Button
# skeleton pa edit nlng if ano gusto nyo layout neto ang importante lang na nilagay ko is yong funcs
def load_driver_status(frame, location, vehicle, back_callback):
    for widget in frame.winfo_children():
        widget.destroy()

    center_frame = Frame(frame)
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    Label(center_frame, text="You are now online").pack(pady=10)
    Label(center_frame, text=f"Location: {location}").pack()
    Label(center_frame, text=f"Vehicle: {vehicle}").pack(pady=(0, 10))
    Label(center_frame, text="Searching for a passenger...").pack(pady=5)
    Button(center_frame, text="Cancel and Go Offline", command=back_callback).pack(pady=20)
