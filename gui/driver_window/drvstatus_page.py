from tkinter import Frame, Label, Button, Toplevel, messagebox
import requests
import time
import threading

API_URL = "https://873b-2001-4451-411d-7e00-a00-27ff-fe01-7f54.ngrok-free.app"

def load_driver_status(frame, driver_id, location, vehicle, back_callback):
    import driver_window.drvloc_to_pass
    for widget in frame.winfo_children():
        widget.destroy()

    # ping to check if user is still there if not remove from queue
    ping_control = {"should_ping": True}
    popup_active = {"active": False}  # Add this flag

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

    # Backend logic: Check for matches every 5 seconds
    def check_matches():
        while ping_control["should_ping"]:
            try:
                # Only check if no popup is currently active
                if not popup_active["active"]:
                    response = requests.get(f"{API_URL}/sakay/driver_checkreq.php?driver_id={driver_id}")
                    data = response.json()
                    
                    if 'pending_matches' in data and data['pending_matches']:
                        # Show match popup
                        match = data['pending_matches'][0]  # Get first pending match
                        popup_active["active"] = True  # Set flag before showing popup
                        show_match_popup(match, driver_id, ping_control, popup_active)
                        
            except Exception as e:
                print(f"Error checking matches: {e}")
            time.sleep(5)

    def show_match_popup(match, driver_id, ping_control, popup_active):
        popup = Toplevel()
        popup.title("New Ride Request")
        popup.geometry("400x300")
        popup.grab_set()  # Make popup modal
        
        # Reset flag when popup is closed
        def on_popup_close():
            popup_active["active"] = False
            popup.destroy()
        
        popup.protocol("WM_DELETE_WINDOW", on_popup_close)
        
        Label(popup, text="🚗 New Ride Request!", font=("Arial", 16, "bold")).pack(pady=10)
        Label(popup, text=f"Passenger ID: {match['passenger_id']}").pack(pady=5)
        Label(popup, text=f"Vehicle Type: {match['vehicle_type']}").pack(pady=5)
        Label(popup, text=f"Pickup: {match['pickup_lat']}, {match['pickup_lng']}").pack(pady=5)
        Label(popup, text=f"Destination: {match['destination_lat']}, {match['destination_lng']}").pack(pady=5)
        
        def accept_match():
            try:
                response = requests.post(f"{API_URL}/sakay/driver_checkreq.php", data={
                    "driver_id": driver_id,
                    "match_id": match['id'],
                    "action": "accept"
                })
                result = response.json()
                if result.get('success'):
                    # Update driver progress to en_route
                    requests.post(f"{API_URL}/sakay/update_driver_progress.php", data={
                        "driver_id": driver_id, 
                        "match_id": match['id']
                    })
                    
                    messagebox.showinfo("Success", "Match accepted!")
                    popup_active["active"] = False
                    popup.destroy()
                    
                    # Stop the ping control since we're moving to a new page
                    ping_control["should_ping"] = False
                    
                    # Load the driver-to-passenger page with match data
                    driver_window.drvloc_to_pass.load_drvloc_to_pass(
                        frame=frame,
                        match_data=match
                    )
                else:
                    messagebox.showerror("Error", result.get('error', 'Unknown error'))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to accept match: {e}")
        
        def reject_match():
            try:
                response = requests.post(f"{API_URL}/sakay/driver_checkreq.php", data={
                    "driver_id": driver_id,
                    "match_id": match['id'],
                    "action": "reject"
                })
                result = response.json()
                if result.get('success'):
                    messagebox.showinfo("Success", "Match rejected!")
                    popup_active["active"] = False  # Reset flag so new matches can be shown
                    popup.destroy()
                    # The original check_matches loop will continue automatically
                else:
                    messagebox.showerror("Error", result.get('error', 'Unknown error'))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reject match: {e}")
        
        Button(popup, text="✓ Accept Ride", command=accept_match, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)
        Button(popup, text="✗ Reject Ride", command=reject_match, bg="red", fg="white", font=("Arial", 12)).pack(pady=5)

    # Start checking for matches
    threading.Thread(target=check_matches, daemon=True).start()

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
        back_callback()

    Button(center_frame, text="Cancel and Go Offline", command=cancel).pack(pady=20)