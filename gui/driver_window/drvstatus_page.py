from tkinter import Frame, Label, Button
import requests

connect_url = "url"

# skeleton pa edit nlng den
def load_driver_status(frame, driver_id, location, vehicle, back_callback, uid):
    for widget in frame.winfo_children():
        widget.destroy()

    center_frame = Frame(frame)
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    status_label = Label(center_frame, text="You are now online")
    status_label.pack(pady=10)
    Label(center_frame, text=f"Location: {location}").pack()
    Label(center_frame, text=f"Vehicle: {vehicle}").pack(pady=(0, 10))
    match_label = Label(center_frame, text="Searching for a passenger...")
    match_label.pack(pady=5)

    # backend logic DONOT TOUCH
    def match_passenger():
        try:
            response = requests.post(f"{connect_url}/sakay/match_driver.php", data={"driver_id": driver_id}).json()
            if response.get("matched"):
                match_label.config(text=f"Matched with Passenger {response['passenger_id']}")
            else:
                # added delay to see actual messages/notifs
                frame.after(3000, match_passenger)
        except:
            match_label.config(text="Error checking for match.")

    match_passenger()

    def cancel():
        try:
            requests.post(f"{connect_url}/sakay/go_offline.php", data={"driver_id": driver_id})
        finally:
            back_callback()

    Button(center_frame, text="Cancel and Go Offline", command=cancel).pack(pady=20)
