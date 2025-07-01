# tk gamitin nyo batas na yan wag kayo mag * pag nag * sasapakin ko -jeflecias
import tkinter as tk
from tkinter import messagebox
import requests

def cursor_hovering(e):
    e.widget['background'] = '#e2eb3d'  # shiny effect
    e.widget['fg'] = 'black'
    e.widget['relief'] = 'raised'
    e.widget['bd'] = '3'


def cursor_not_hovering(e):
    e.widget['bg'] = '#D2B48C' #default na itsura nong button
    e.widget['fg'] = '#643602'
    e.widget['relief'] = 'flat'
    e.widget['bd'] = '1'

def open_register(parent, go_back):
    # window na pangalan lahat ng mga window naten wag kayong mag iba ng pangalan sa ibang mga file thank you
    window = tk.Frame(parent, bg='#D2B48C')

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
        elif role == "driver":
            is_driver = 1

        try:
            # mismong $POST
            response = requests.post("https://6653-2001-4451-411d-7e00-a00-27ff-fe01-7f54.ngrok-free.app/sakay/register.php", data={
                "username": username,
                "email": email,
                "password": password,
                "is_driver": int(is_driver),
                "is_passenger": int(is_passenger)
            })

            messagebox.showinfo("Register", response.text)

        except:
            messagebox.showerror("Error", "failed connect")

    # username
    # pag ililimit nyo to sabihan nyo ko, para ma edit ko rin sa db
    tk.Label(window, text="Username", bg="#D2B48C", fg='#643602', font=('Comic Sans MS',9)).pack()
    username_entry = tk.Entry(window)
    username_entry.pack()

    # email
    # if want nyo lang, sbihan nyo den ako, if want nyo yong parang check if email is valid, or pede kayo na den bahal jan
    tk.Label(window, text="Email", bg="#D2B48C", fg='#643602', font=('Comic Sans MS',9)).pack(pady=(10))
    email_entry = tk.Entry(window)
    email_entry.pack()

    # password
    # for frontend, cguro kayo mag add like password strength something o enter your password twice hahaha
    tk.Label(window, text="Password", bg="#D2B48C", fg='#643602', font=('Comic Sans MS',9)).pack(pady=(10))
    password_entry = tk.Entry(window, show="*")
    password_entry.pack()

    # yan lagay mo kung alien ka ba o hindi
    # edit nyo to hahahahahahah
    tk.Label(window, text="Role", bg="#D2B48C", fg='#643602', font=('Comic Sans MS',9)).pack(pady=(10))

    # default value = passenger sige pord
    pord = tk.StringVar(value="passenger") 
    tk.Radiobutton(window, text="alien ako", variable=pord, value="passenger", bg='#D2B48C', fg='#643602', font=('Comic Sans MS',9)).pack()
    tk.Radiobutton(window, text="drayber ako", variable=pord, value="driver", bg='#D2B48C', fg='#643602', font=('Comic Sans MS',9)).pack()

    # register button
    button = tk.Button(window, text="Register", command=register, bg='#D2B48C', fg='#643602', font=('Comic Sans MS',9))
    button.bind("<Enter>", cursor_hovering)
    button.bind("<Leave>", cursor_not_hovering)
    button.pack(pady=15)

    # back to login button
    back_button = tk.Button(window, text="Back to Login", command=go_back, bg='#D2B48C', fg='#643602', font=('Comic Sans MS',9))
    back_button.bind("<Enter>", cursor_hovering)
    back_button.bind("<Leave>", cursor_not_hovering)
    back_button.pack()

    return window

