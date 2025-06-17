# tk gamitin nyo batas na yan wag kayo mag * pag nag * sasapakin ko -jeflecias
import tkinter as tk
from tkinter import messagebox
from register_page import open_register
import requests

# window na pangalan lahat ng mga window naten wag kayong mag iba ng pangalan sa ibang mga file thank you
# !!!!!!!!!!!!!!!! mga front end pagandahin nyo nlng to !!!!!!!!!!!!!!!!!!
window = tk.Tk()
window.title("login skelly page")
window.geometry("300x150")

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
        result = response.text.strip()

        if result == "Login successful!":
            messagebox.showinfo("Login", result)
            # TO DO
            # pagkatapos ma login, mabubuksan na yong main app, lalagay ko skelly dito later

        else:
            messagebox.showerror("Login", result)

    except:
        messagebox.showerror("Connection Error", "could not connect")
    



# username entry
tk.Label(window, text="Username")
username_entry = tk.Entry(window)
username_entry.pack()

# password entry
tk.Label(window, text="Password").pack(pady=(10,0))
password_entry = tk.Entry(window, show="*")
password_entry.pack()

# login button
tk.Button(window, text="Login", command=login).pack(pady=10)

# register button
tk.Button(window, text="No account? Register", command=open_register, fg="blue").pack()
window.mainloop()