from tkinter import Frame, Label, Button, messagebox
import requests
import threading
import time
import tkintermapview
API_URL = "https://1ff5-2001-4451-411d-7e00-a00-27ff-fe01-7f54.ngrok-free.app" 

# wag nyo pakailaman backend logic

def load_ride_status(frame, uid):
    from passenger_window.home_page import load_home
    for widget in frame.winfo_children():
        widget.destroy()
    import threading
    import time
    
    # ping to check if user is still there if not remove his req
    ping_control = {"should_ping": True}
    
    def ping_passenger(user_id, control):
        def ping_loop():
            while control["should_ping"]:
                try:
                    requests.post("https://1ff5-2001-4451-411d-7e00-a00-27ff-fe01-7f54.ngrok-free.app/sakay/ping_passenger.php", data={"user_id": user_id})
                except:
                    pass
                time.sleep(10)  
        threading.Thread(target=ping_loop, daemon=True).start()

    ping_passenger(uid, ping_control)

    # frontend stuff
    status_label = Label(frame, text="Looking for a driver...", font=("Arial", 14))
    status_label.pack(pady=20)
    map_widget = tkintermapview.TkinterMapView(frame, width=800, height=400, corner_radius=0)
    map_widget.pack(pady=10, fill="both", expand=True)
    map_widget.set_zoom(12)
    def poll_match():
        while True:
            try:
                response = requests.get(f"{API_URL}/sakay/check_match.php?uid={uid}")
                data = response.json()
                if data.get("matched"):
                    driver = data["driver"]
                    driver_lat = driver["lat"]
                    driver_lng = driver["lng"]
                    status_label.config(text=f"Driver matched: {driver['name']}")
                    map_widget.set_position(driver_lat, driver_lng)
                    map_widget.set_marker(driver_lat, driver_lng, text="Driver Location")
                    break
            except Exception as e:
                print("Error polling match:", e)
            time.sleep(3)
    threading.Thread(target=poll_match, daemon=True).start()
    def cancel_ride():
        # stop ping when cancelled
        ping_control["should_ping"] = False

        #backend stuff again
        try:
            response = requests.post(f"{API_URL}/sakay/cancel_ride.php", data={"uid": uid})
            result = response.json()
            if result.get("success"):
                messagebox.showinfo("Ride Cancelled", "Your ride has been cancelled.")
                load_home(frame, uid)  # Return to home page
            else:
                messagebox.showerror("Error", result.get("message", "Could not cancel the ride."))
        except Exception as e:
            messagebox.showerror("Error", f"Could not cancel the ride.\n{str(e)}")
    Button(frame, text="Cancel Ride", command=cancel_ride).pack(pady=10)