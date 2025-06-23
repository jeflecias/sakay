# tk gamitin nyo batas na yan wag kayo mag * pag nag * sasapakin ko -jeflecias
import tkinter as tk
from tkinter import messagebox
import requests


def open_register():
    # window na pangalan lahat ng mga window naten wag kayong mag iba ng pangalan sa ibang mga file thank you
    window = tk.Toplevel()
    window.title("register skelly page")
    window.geometry("500x500")

    # register function
    def register():
        # kunin yong mga entries
        username = username_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        role = pord.get()

        # if empty end func
        if not (username and email and password):
            messagebox.showerror("Error", "fill all fields")
            return
        
        is_passenger = 0
        is_driver = 0

        if role == "passenger":
            is_passenger = 1
        else:
            is_driver = 1
        
        try:
            # mismong $POST
            response = requests.post("http://localhost/sakay/register.php", data={
                "username": username,
                "email": email,
                "password": password,
                "is_driver": is_driver,
                "is_passenger": is_passenger
            })

            messagebox.showinfo("Register", response.text)

        except:
            messagebox.showerror("Error", "failed connect")

    # username
    # pag ililimit nyo to sabihan nyo ko, para ma edit ko rin sa db
    tk.Label(window, text="Username").pack()
    username_entry = tk.Entry(window)
    username_entry.pack()

    # email
    # if want nyo lang, sbihan nyo den ako, if want nyo yong parang check if email is valid, or pede kayo na den bahal jan
    tk.Label(window, text="Email").pack(pady=(10))
    email_entry = tk.Entry(window)
    email_entry.pack()

    # password
    # for frontend, cguro kayo mag add like password strength something o enter your password twice hahaha
    tk.Label(window, text="Password").pack(pady=(10))
    password_entry = tk.Entry(window, show="*")
    password_entry.pack()

    # yan lagay mo kung alien ka ba o hindi
    # edit nyo to hahahahahahah
    tk.Label(window, text="Role").pack(pady=(10))

    # default value = passenger sige pord
    pord = tk.StringVar(value="passenger") 
    tk.Radiobutton(window, text="alien ako", variable=pord, value="passenger").pack()
    tk.Radiobutton(window, text="drayber ako", variable=pord, value="driver").pack()

    # register button
    tk.Button(window, text="Register", command=register).pack(pady=15)

