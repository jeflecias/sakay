from tkinter import Frame, Label, Button, Entry

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
            bg="#8E9B73", fg="white", command=lambda: load_authentication(frame)).pack(pady=5)

      Button(center_frame, text="Contact Support", font=("Comic Sans MS", 12),
            bg="#A16F36", fg="white", command=lambda: load_support(frame)).pack(pady=5)

def load_authentication(frame):
      for widget in frame.winfo_children():
            widget.destroy()

      authentication_frame = Frame(frame, bg="#D2B48C")
      authentication_frame.place(relx=0.5, rely=0.5, anchor="center")

      Label(authentication_frame, text="Please input password.", fg="#643602", bg="#D2B48C",
            font=("Comic Sans MS", 12)).pack(pady=5)

      Entry(authentication_frame, text="Password", font=("Comic Sans MS", 12), 
            bg="white", fg="#5E7530").pack(pady=10)
      
      Button(authentication_frame, text="Enter", font=("Comic Sans MS", 12), 
            bg="#A16F36", fg="white", command=lambda: load_settings(frame)).pack(pady=10) # lagay niyo rito na magchecheck ng password sa account para maaccess ang settings
      
      Button(authentication_frame, text="Back", font=("Comic Sans MS", 12), 
            bg="#8E9B73", fg="white", 
            command=lambda: load_account(frame)).pack(pady=10)

def load_settings(frame):
      for widget in frame.winfo_children():
            widget.destroy()

      settings_frame = Frame(frame, bg="#D2B48C")
      settings_frame.place(relx=0.5, rely=0.5, anchor="center")

      Label(settings_frame, text="Account Settings", fg="#643602", bg="#D2B48C",
            font=("Comic Sans MS", 12)).pack(pady=5)

      Button(settings_frame, text="Change Password", font=("Comic Sans MS", 12), 
            bg="#A16F36", fg="white", command=lambda: load_changepass(frame)).pack(pady=10)

      Button(settings_frame, text="Back", font=("Comic Sans MS", 12), 
            bg="#8E9B73", fg="white", 
            command=lambda: load_account(frame)).pack(pady=10)
      
def load_changepass(frame):
      for widget in frame.winfo_children():
            widget.destroy()

      changepass_frame = Frame(frame, bg="#D2B48C")
      changepass_frame.place(relx=0.5, rely=0.5, anchor="center")

      Label(changepass_frame, text="Please input new password.", fg="#643602", bg="#D2B48C",
            font=("Comic Sans MS", 12)).pack(pady=5)

      Entry(changepass_frame, text="New Password", font=("Comic Sans MS", 12), 
            bg="white", fg="#5E7530").pack(pady=10)
      
      Entry(changepass_frame, text="Confirm New Password", font=("Comic Sans MS", 12), 
            bg="white", fg="#5E7530").pack(pady=10) # lagay niyo nalang ng pang change type shi
      
      Button(changepass_frame, text="Enter", font=("Comic Sans MS", 12), 
            bg="#A16F36", fg="white", command=lambda: load_settings(frame)).pack(pady=10)

      Button(changepass_frame, text="Back", font=("Comic Sans MS", 12), 
            bg="#8E9B73", fg="white", 
            command=lambda: load_settings(frame)).pack(pady=10)

def load_support(frame):
      for widget in frame.winfo_children():
            widget.destroy()

      # settings content
      support_frame = Frame(frame, bg="#D2B48C")
      support_frame.place(relx=0.5, rely=0.5, anchor="center")

      Label(support_frame, text="Contact Support", fg="#643602", bg="#D2B48C",
            font=("Comic Sans MS", 16, "bold")).pack(pady=5)
      
      Label(support_frame, text="📞Phone number: 09123456771\n 📧Email: JefLecias@gmail.com", fg="#643602", bg="#D2B48C",
            font=("Comic Sans MS", 13)).pack(pady=5)

      Button(support_frame, text="Back", font=("Comic Sans MS", 12),
            bg="#8E9B73", fg="white",
            command=lambda: load_account(frame)).pack(pady=10)

