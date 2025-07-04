from tkinter import Frame, Label, Button, Toplevel, messagebox
import requests
import time
import threading

connect_url = "https://5c23-2001-4451-411d-7e00-a00-27ff-fe01-7f54.ngrok-free.app"

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
                    requests.post(f"{connect_url}/sakay/ping_driver.php", data={"driver_id": driver_id})
                except:
                    pass
                time.sleep(10)

        threading.Thread(target=ping_loop, daemon=True).start()

    start_driver_ping(driver_id, ping_control)

    # backend stuff check for match in the match queue must match driver id
    def check_matches():
        while ping_control["should_ping"]:
            try:
                # check if no popup is active
                if not popup_active["active"]:
                    response = requests.get(f"{connect_url}/sakay/driver_checkreq.php?driver_id={driver_id}")
                    data = response.json()
                    
                    if 'pending_matches' in data and data['pending_matches']:
                        match = data['pending_matches'][0]  
                        popup_active["active"] = True  
                        show_match_popup(match, driver_id, ping_control, popup_active)
                        
            except Exception as e:
                print(f"Error checking matches: {e}")
            time.sleep(5)

    def show_match_popup(match, driver_id, ping_control, popup_active):
        popup = Toplevel()
        popup.title("New Ride Request")
        popup.geometry("400x300")
        popup.grab_set() 
        
        def on_popup_close():
            popup_active["active"] = False
            popup.destroy()
        
        popup.protocol("WM_DELETE_WINDOW", on_popup_close)
        
        Label(popup, text="🚗 New Ride Request!", font=("Arial", 16, "bold")).pack(pady=10)
        Label(popup, text=f"Passenger ID: {match['passenger_id']}").pack(pady=5)
        Label(popup, text=f"Vehicle Type: {match['vehicle_type']}").pack(pady=5)
        Label(popup, text=f"Pickup: {match['pickup_lat']}, {match['pickup_lng']}").pack(pady=5)
        Label(popup, text=f"Destination: {match['destination_lat']}, {match['destination_lng']}").pack(pady=5)
        
        # simple accept match stuff
        def accept_match():
            try:
                response = requests.post(f"{connect_url}/sakay/driver_checkreq.php", data={
                    "driver_id": driver_id,
                    "match_id": match['id'],
                    "action": "accept"
                })
                result = response.json()
                
                if result.get('success'):
                    progress_response = requests.post(f"{connect_url}/sakay/drvaccept_match.php", data={
                        "driver_id": driver_id, 
                        "match_id": match['id']
                    })
                    
                    if progress_response.status_code == 200:
                        progress_result = progress_response.json()
                        
                        if progress_result.get('success'):
                            # update to en route then passenger scans this
                            messagebox.showinfo("Success", "Match accepted and en route!")
                            popup_active["active"] = False
                            popup.destroy()
                            

                            ping_control["should_ping"] = False
                            
                            driver_window.drvloc_to_pass.load_drvloc_to_pass(
                                frame=frame,
                                match_data=match,
                                back_callback=back_callback
                            )
                        else:
                            # debug stuff it might cause an error again IDK WHY
                            error_msg = progress_result.get('error', 'Unknown error')
                            debug_info = progress_result.get('debug', {})
                            
                            # more details WHAT IS CAUSING THE PROBLEM
                            messagebox.showerror("Progress Update Failed", 
                                f"Match accepted but couldn't start journey:\n\n"
                                f"Error: {error_msg}\n\n"
                                f"Debug Info:\n"
                                f"Match ID: {debug_info.get('current_match', {}).get('id', 'N/A')}\n"
                                f"Driver Accepted: {debug_info.get('can_update', {}).get('driver_accepted', 'N/A')}\n"
                                f"Progress is 'not': {debug_info.get('can_update', {}).get('driver_progress_not', 'N/A')}\n"
                                f"Status is 'ongoing': {debug_info.get('can_update', {}).get('status_ongoing', 'N/A')}"
                            )
                    else:
                        # show error on server
                        messagebox.showerror("Error", f"Failed to update progress: HTTP {progress_response.status_code}")
                        
                else:
                    # if match fails
                    messagebox.showerror("Error", f"Failed to accept match: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Network error: {str(e)}")
                print(f"Full error: {e}") 
        
        def reject_match():
            try:
                response = requests.post(f"{connect_url}/sakay/driver_checkreq.php", data={
                    "driver_id": driver_id,
                    "match_id": match['id'],
                    "action": "reject"
                })
                result = response.json()
                if result.get('success'):
                    messagebox.showinfo("Success", "Match rejected!")
                    popup_active["active"] = False  
                    popup.destroy()
                else:
                    messagebox.showerror("Error", result.get('error', 'Unknown error'))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reject match: {e}")
        
        Button(popup, text="✓ Accept Ride", command=accept_match, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)
        Button(popup, text="✗ Reject Ride", command=reject_match, bg="red", fg="white", font=("Arial", 12)).pack(pady=5)

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