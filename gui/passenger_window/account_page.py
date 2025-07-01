from tkinter import Frame, Label, Button

# account page for the sakay app
def load_account(frame, user_name="Passenger"):
    for widget in frame.winfo_children():
        widget.destroy()

    # center content
    center_frame = Frame(frame, bg="#D2B48C")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    # label widgets for account page
    Label(center_frame, text="Account Info", fg="#643602", bg="#D2B48C",
          font=("Comic Sans MS", 16, "bold")).pack(pady=10)

    Label(center_frame, text=f"Hello, {user_name}!", fg="#643602", bg="#D2B48C",
          font=("Comic Sans MS", 14)).pack(pady=5)

    Label(center_frame, text="Profile: No detailed info available yet.", fg="#A16F36", bg="#D2B48C",
          font=("Comic Sans MS", 12)).pack(pady=5)

    Button(center_frame, text="Settings", font=("Comic Sans MS", 12),
           bg="#8E9B73", fg="white").pack(pady=5)

    Button(center_frame, text="Contact Support", font=("Comic Sans MS", 12),
           bg="#A16F36", fg="white").pack(pady=5)
