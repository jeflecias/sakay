from tkinter import Frame, Label, Button
import requests
import time
import threading

API_URL = "https://1ff5-2001-4451-411d-7e00-a00-27ff-fe01-7f54.ngrok-free.app"

def load_driver_status(frame, driver_id, location, vehicle, back_callback):
    for widget in frame.winfo_children():
        widget.destroy()

    # ping to check if user is still there if not remove from queue
    ping_control = {"should_ping": True}

    def start_driver_ping(driver_id, control):
        def ping_loop():
            while control["should_ping"]:
                try:
                    requests.post(f"{API_URL}/sakay/ping_driver.php", data={"driver_id": driver_id})
                except:
                    pass
                time.sleep(10)

        threading.Thread(target=ping_loop, daemon=True).start()

    start_driver_ping(driver_id, ping_control)

    center_frame = Frame(frame)
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    status_label = Label(center_frame, text="You are now online")
    status_label.pack(pady=10)
    Label(center_frame, text=f"Location: {location}").pack()
    Label(center_frame, text=f"Vehicle: {vehicle}").pack(pady=(0, 10))
    match_label = Label(center_frame, text="Searching for a passenger...")
    match_label.pack(pady=5)

    def cancel():
        # stop pinging when cancelled
        ping_control["should_ping"] = False
        
        try:
            requests.post(f"{API_URL}/sakay/driver_offline.php", data={"driver_id": driver_id})
        except:
            pass
        
        back_callback()

    Button(center_frame, text="Cancel and Go Offline", command=cancel).pack(pady=20)