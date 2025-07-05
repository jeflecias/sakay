from tkinter import Frame, Label, Scrollbar, Canvas, VERTICAL, RIGHT, Y, BOTH, LEFT
import json
import os
from datetime import datetime

def load_activity(frame, uid):
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Main container
    main_frame = Frame(frame, bg="#D2B48C")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Header
    Label(main_frame, text="📊 Your Activity", fg="#643602", bg="#D2B48C",
          font=("Comic Sans MS", 18, "bold")).pack(pady=10)
    
    # Create scrollable frame for transaction history
    canvas = Canvas(main_frame, bg="#D2B48C", highlightthickness=0)
    scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#D2B48C")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Load and display transaction history
    try:
        history_file = r"sakay\gui\transaction_history.json"
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
                transactions = history.get("transactions", [])
                
                if transactions:
                    # Display each transaction
                    for i, transaction in enumerate(transactions, 1):
                        # Transaction container
                        trans_frame = Frame(scrollable_frame, bg="#F5DEB3", relief="raised", bd=2)
                        trans_frame.pack(fill="x", pady=5, padx=10)
                        
                        # Transaction number and ID
                        Label(trans_frame, text=f"🚗 Trip #{i} - ID: {transaction.get('ride_request_id', 'N/A')}", 
                              fg="#8B4513", bg="#F5DEB3", font=("Comic Sans MS", 12, "bold")).pack(anchor="w", padx=10, pady=2)
                        
                        # Vehicle type and fare type
                        Label(trans_frame, text=f"🚙 Vehicle: {transaction.get('vehicle_type', 'N/A')} ({transaction.get('fare_type', 'N/A')})", 
                              fg="#654321", bg="#F5DEB3", font=("Comic Sans MS", 10)).pack(anchor="w", padx=10, pady=1)
                        
                        # Distance and duration
                        Label(trans_frame, text=f"📏 Distance: {transaction.get('distance_km', 'N/A')} km | ⏱️ Duration: {transaction.get('duration_minutes', 'N/A')} min", 
                              fg="#654321", bg="#F5DEB3", font=("Comic Sans MS", 10)).pack(anchor="w", padx=10, pady=1)
                        
                        # Fare amount
                        fare_amount = transaction.get('fare_amount', 0)
                        Label(trans_frame, text=f"💰 Fare Earned: ₱{fare_amount:.2f}", 
                              fg="#006400", bg="#F5DEB3", font=("Comic Sans MS", 11, "bold")).pack(anchor="w", padx=10, pady=1)
                        
                        # Pickup location
                        pickup_loc = transaction.get('pickup_location', 'N/A')
                        if len(pickup_loc) > 80:
                            pickup_loc = pickup_loc[:80] + "..."
                        Label(trans_frame, text=f"📍 From: {pickup_loc}", 
                              fg="#654321", bg="#F5DEB3", font=("Comic Sans MS", 9)).pack(anchor="w", padx=10, pady=1)
                        
                        # Destination location
                        dest_loc = transaction.get('destination_location', 'N/A')
                        if len(dest_loc) > 80:
                            dest_loc = dest_loc[:80] + "..."
                        Label(trans_frame, text=f"🎯 To: {dest_loc}", 
                              fg="#654321", bg="#F5DEB3", font=("Comic Sans MS", 9)).pack(anchor="w", padx=10, pady=1)
                        
                        # Date and time
                        start_time = transaction.get('ride_start_time', 'N/A')
                        end_time = transaction.get('ride_end_time', 'N/A')
                        
                        if start_time != 'N/A' and start_time:
                            try:
                                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                                start_formatted = start_dt.strftime("%Y-%m-%d %H:%M:%S")
                                Label(trans_frame, text=f"🕐 Started: {start_formatted}", 
                                      fg="#654321", bg="#F5DEB3", font=("Comic Sans MS", 9)).pack(anchor="w", padx=10, pady=1)
                            except:
                                Label(trans_frame, text=f"🕐 Started: {start_time}", 
                                      fg="#654321", bg="#F5DEB3", font=("Comic Sans MS", 9)).pack(anchor="w", padx=10, pady=1)
                        
                        if end_time != 'N/A' and end_time:
                            try:
                                end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                                end_formatted = end_dt.strftime("%Y-%m-%d %H:%M:%S")
                                Label(trans_frame, text=f"🕐 Completed: {end_formatted}", 
                                      fg="#654321", bg="#F5DEB3", font=("Comic Sans MS", 9)).pack(anchor="w", padx=10, pady=1)
                            except:
                                Label(trans_frame, text=f"🕐 Completed: {end_time}", 
                                      fg="#654321", bg="#F5DEB3", font=("Comic Sans MS", 9)).pack(anchor="w", padx=10, pady=1)
                        
                        # Driver ID
                        Label(trans_frame, text=f"👤 Driver ID: {transaction.get('driver_id', 'N/A')}", 
                              fg="#654321", bg="#F5DEB3", font=("Comic Sans MS", 9)).pack(anchor="w", padx=10, pady=(1, 5))
                    
                    # Summary at the bottom
                    summary_frame = Frame(scrollable_frame, bg="#DEB887", relief="sunken", bd=2)
                    summary_frame.pack(fill="x", pady=10, padx=10)
                    
                    total_trips = len(transactions)
                    total_earnings = sum(transaction.get('fare_amount', 0) for transaction in transactions)
                    total_distance = sum(transaction.get('distance_km', 0) for transaction in transactions)
                    
                    Label(summary_frame, text="📈 Summary", fg="#8B4513", bg="#DEB887", 
                          font=("Comic Sans MS", 14, "bold")).pack(pady=5)
                    Label(summary_frame, text=f"Total Trips: {total_trips}", fg="#654321", bg="#DEB887", 
                          font=("Comic Sans MS", 11)).pack(pady=1)
                    Label(summary_frame, text=f"Total Earnings: ₱{total_earnings:.2f}", fg="#006400", bg="#DEB887", 
                          font=("Comic Sans MS", 11, "bold")).pack(pady=1)
                    Label(summary_frame, text=f"Total Distance: {total_distance:.2f} km", fg="#654321", bg="#DEB887", 
                          font=("Comic Sans MS", 11)).pack(pady=(1, 5))
                    
                else:
                    # No transactions found
                    Label(scrollable_frame, text="📋 No transactions found.", fg="#A16F36", bg="#D2B48C",
                          font=("Comic Sans MS", 12)).pack(pady=20)
                    Label(scrollable_frame, text="Complete some rides to see your activity here.", fg="#A16F36", bg="#D2B48C",
                          font=("Comic Sans MS", 12)).pack(pady=5)
        else:
            # File doesn't exist
            Label(scrollable_frame, text="📋 No transaction history file found.", fg="#A16F36", bg="#D2B48C",
                  font=("Comic Sans MS", 12)).pack(pady=20)
            Label(scrollable_frame, text="Complete some rides to see your activity here.", fg="#A16F36", bg="#D2B48C",
                  font=("Comic Sans MS", 12)).pack(pady=5)
    
    except Exception as e:
        # Error loading file
        Label(scrollable_frame, text="❌ Error loading transaction history", fg="#FF0000", bg="#D2B48C",
              font=("Comic Sans MS", 12, "bold")).pack(pady=20)
        Label(scrollable_frame, text=f"Error: {str(e)}", fg="#A16F36", bg="#D2B48C",
              font=("Comic Sans MS", 10)).pack(pady=5)
    
    # Pack the canvas and scrollbar
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # Bind mousewheel to canvas
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)