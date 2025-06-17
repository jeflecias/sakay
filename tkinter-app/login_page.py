# tk gamitin nyo batas na yan wag kayo mag * pag nag * sasapakin ko -jeflecias
import tkinter as tk
from tkinter import messagebox

# window na pangalan lahat ng mga window naten wag kayong mag iba ng pangalan sa ibang mga file thank you
# !!!!!!!!!!!!!!!! mga front end pagandahin nyo nlng to !!!!!!!!!!!!!!!!!!
window = tk.Tk()
window.title("login skelly page")
window.geometry("300x150")

# dito kayo maglagay ng funcs
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "123":
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showerror("Login", "Invalid.")

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

window.mainloop()