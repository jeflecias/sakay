from tkinter import Frame, Label

def load_activity(frame, uid):
    for widget in frame.winfo_children():
        widget.destroy()

    # Centering frame in the middle of the screen
    center_frame = Frame(frame, bg="#D2B48C")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    Label(center_frame, text="Your Activity", fg="#643602", bg="#D2B48C",
          font=("Comic Sans MS", 16, "bold")).pack(pady=10)
    Label(center_frame, text="No recent activities found.", fg="#A16F36", bg="#D2B48C",
          font=("Comic Sans MS", 12)).pack(pady=5)
    Label(center_frame, text="You can view your past trips here.", fg="#A16F36", bg="#D2B48C",
          font=("Comic Sans MS", 12)).pack(pady=5)
