# tk gamitin nyo batas na yan wag kayo mag * pag nag * sasapakin ko -jeflecias
import tkinter as tk
from tkinter import messagebox
from register_page import open_register
import requests

# window na pangalan lahat ng mga window naten wag kayong mag iba ng pangalan sa ibang mga file thank you
# !!!!!!!!!!!!!!!! mga front end pagandahin nyo nlng to !!!!!!!!!!!!!!!!!!
window = tk.Tk()
window.config(background='black')
window.title("login skelly page")

# dito kayo maglagay ng funcs
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    # if empty end function
    if not (username and password):
        messagebox.showerror("Error", "enter all fields")
        return
    
    try:
        response = requests.post("http://localhost/sakay/login.php", data={
            "username": username,
            "password": password
        })

        data = response.json()

        if data["status"] == "success":
            messagebox.showinfo("Login", data["message"])
            # TO DO
            # pagkatapos ma login, mabubuksan na yong main app, lalagay ko skelly dito later

            if data["is_passenger"]:
                messagebox.showinfo("passenger,passenger")
            elif data["is_driver"]:
                messagebox.showinfo("driver","driver")
            else:
                messagebox.showinfo("Role","No role assigned to this user!")

        else:
            messagebox.showerror("Login", data["message"])

    except:
        messagebox.showerror("Connection Error", "could not connect")
    

def cursor_hovering(e):
    e.widget['background'] = '#e2eb3d'  # shiny effect
    e.widget['fg'] = 'black'
    e.widget['relief'] = 'raised'
    e.widget['bd'] = '3'


def cursor_not_hovering(e):
    e.widget['background'] = 'black' #default na itsura nong button
    e.widget['fg'] = '#0fff13'
    e.widget['relief'] = 'flat'
    e.widget['bd'] = '1'

#helper function angkalat kse eh grr
def create_label(parent, text):
    return tk.Label(parent, text=text, background='black', fg='#0fff13', font=('Times New Roman', 9))

def create_entry(parent, **kwargs):
    return tk.Entry(parent, **kwargs)

def create_button(parent, text, command):
    btn = tk.Button(parent, text=text, command=command, font=("Times New Roman", 9),
                    bg='black', fg='#0fff13', relief='flat', bd=1)
    btn.bind("<Enter>", cursor_hovering)
    btn.bind("<Leave>", cursor_not_hovering)
    return btn

# username entry
create_label(window, "Username").pack(pady=(10, 0))
username_Label = tk.Entry(window)

username_entry = tk.Entry(window)
username_entry.pack()

# password entry
create_label(window, text="Password").pack(pady=(10,0))
password_Label = tk.Entry(window)

password_entry = tk.Entry(window)
password_entry.pack()

#gawin kolang sila variable para ma call ko ahhh
Login_button = create_button(window, text="Login", command=login)
Login_button.pack(pady=10)

Register_Button = create_button(window, text="No account? Register", command=open_register)
Register_Button.pack(pady=10)

window.mainloop()