# tk gamitin nyo batas na yan wag kayo mag * pag nag * sasapakin ko -jeflecias
import tkinter as tk
from tkinter import messagebox
from register_page import open_register
from passenger_window.main_booking import open_passenger
from driver_window.driver_window import open_driver
from utils import cursor_hovering, cursor_not_hovering
import requests

connect_url = "https://5c23-2001-4451-411d-7e00-a00-27ff-fe01-7f54.ngrok-free.app"

# window na pangalan lahat ng mga window naten wag kayong mag iba ng pangalan sa ibang mga file thank you
# !!!!!!!!!!!!!!!! mga front end pagandahin nyo nlng to !!!!!!!!!!!!!!!!!!
window = tk.Tk()
window.config(background='#D2B48C')
window.title("login skelly page")
window.geometry("1280x720")
login_frame = tk.Frame(window, bg='#D2B48C')

# switch to regis
def switch_frame(target):
    target.tkraise()

# dito kayo maglagay ng funcs
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    # if empty end function
    if not (username and password):
        messagebox.showerror("Error", "enter all fields")
        return
    
    # local testing for non-server
    if password == "123":
        user_id = 123
        if username == "guestp":
            fin_frame = open_passenger(window, user_id)
            login_frame.destroy()
            return
        elif username == "guestd":
            fin_frame = open_driver(window, user_id)
            login_frame.destroy()
            return

    try:
        response = requests.post(f"{connect_url}/sakay/login.php", data={
            "username": username,
            "password": password
        })

        data = response.json()

        if data["status"] == "success":
            user_id = data["user_id"] # for later
            messagebox.showinfo("Login", data["message"])
            # TO DO
            # pagkatapos ma login, mabubuksan na yong main app, lalagay ko skelly dito later
            
            if data["is_passenger"]:
                fin_frame = open_passenger(window, user_id)
                login_frame.destroy()

            elif data["is_driver"]:
                fin_frame = open_driver(window, user_id)
                login_frame.destroy()

            else:
                messagebox.showinfo("Role","No role assigned to this user!")

        else:
            messagebox.showerror("Login", data["message"])

    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        messagebox.showerror("Connection Error", f"could not connect:\n{e}")

    


#helper function angkalat kse eh grr
def create_label(parent, text):
    return tk.Label(parent, text=text, background='#D2B48C', fg='#643602', font=('Comic Sans MS', 9))

def create_entry(parent, **kwargs):
    return tk.Entry(parent, **kwargs)

def create_button(parent, text, command):
    btn = tk.Button(parent, text=text, command=command, font=("Comic Sans MS", 9),
                    bg='#D2B48C', fg='#643602', relief='flat', bd=1)
    btn.bind("<Enter>", cursor_hovering)
    btn.bind("<Leave>", cursor_not_hovering)
    return btn

# username entry
create_label((login_frame), "Username").pack(pady=(10, 0))
username_Label = tk.Entry(login_frame)

username_entry = tk.Entry(login_frame)
username_entry.pack()

# password entry
create_label(login_frame, text="Password").pack(pady=(10,0))
password_Label = tk.Entry(login_frame)
password_entry = tk.Entry(login_frame)
password_entry.pack()

#gawin kolang sila variable para ma call ko ahhh
Login_button = create_button(login_frame, text="Login", command=login)
Login_button.pack(pady=10)

Register_Button = create_button(login_frame, text="No account? Register", command=lambda: switch_frame(register_frame))
Register_Button.pack(pady=10)
register_frame = open_register(window, lambda: switch_frame(login_frame))

# main guard, for debugging
if __name__ == "__main__":
    for frame in (login_frame, register_frame):
        frame.place(relwidth=1, relheight=1)

    login_frame.tkraise()
    window.mainloop()