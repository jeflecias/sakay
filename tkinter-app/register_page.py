# tk gamitin nyo batas na yan wag kayo mag * pag nag * sasapakin ko -jeflecias
import tkinter as tk
from tkinter import messagebox
import requests

# window na pangalan lahat ng mga window naten wag kayong mag iba ng pangalan sa ibang mga file thank you
window = tk.Tk()
window.title("register skelly page")
window.geometry("300x200")

# register function
def register():
    username = username_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    pass

# username
tk.Label(window, text="Username").pack()
username_entry = tk.Entry(window)
username_entry.pack()

# email
tk.Label(window, text="Email").pack(pady=(10, 0))
email_entry = tk.Entry(window)
email_entry.pack()

# password
# for frontend, cguro kayo mag add like password strength something o enter your password twice hahaha
tk.Label(window, text="Password").pack(pady=(10, 0))
password_entry = tk.Entry(window, show="*")
password_entry.pack()

# register button
tk.Button(window, text="Register", command=register).pack(pady=15)

window.mainloop()
