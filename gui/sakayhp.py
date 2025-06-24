import tkinter as tk
from tkinter import Frame, Label, Button, Entry
from backend.backend_for_pickup_location import UserInputApp
from PIL import Image, ImageTk
import os

# naglagay ako neto kase magkaka error siya kase 
# mag kaka iba tayo ng working dir, and if thats the case this works on one user but breaks on another
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Helper functions
def create_styled_label(parent, text, font_size=12):
    return Label(parent,
                 text=text,
                 font=("Times New Roman", font_size),
                 fg='#FFD700',
                 bg='black')

def create_styled_button(parent, text, command, font_size=10, image=None):
    button = tk.Button(parent,
                       text=text,
                       font=("Times New Roman", font_size),
                       image=image,
                       compound='top',
                       fg='#FFD700',
                       bg='black',
                       relief='ridge',
                       bd=3,
                       command=command)
    button.bind("<Enter>", cursor_hovering)
    button.bind("<Leave>", cursor_not_hovering)
    return button

def create_styled_entry(parent, text):
    entry = Entry(parent, text=text, fg='#FFD700', bg='black')
    return entry

def cursor_hovering(e):
    e.widget['background'] = '#FFD700'
    e.widget['fg'] = 'black'
    e.widget['relief'] = 'ridge'
    e.widget['bd'] = '2'

def cursor_not_hovering(e):
    e.widget['background'] = 'black'
    e.widget['fg'] = '#FFD700'
    e.widget['relief'] = 'ridge'
    e.widget['bd'] = '2'

class Page0(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')

class HomePage(Page0):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Load images using absolute path
        self.moto_img = ImageTk.PhotoImage(Image.open(os.path.join(BASE_DIR, "img", "motor.png")).resize((64, 64)))
        self.car4_img = ImageTk.PhotoImage(Image.open(os.path.join(BASE_DIR, "img", "sedan.png")).resize((64, 64)))
        self.car6_img = ImageTk.PhotoImage(Image.open(os.path.join(BASE_DIR, "img", "van.png")).resize((64, 64)))
        self.ship_img = ImageTk.PhotoImage(Image.open(os.path.join(BASE_DIR, "img", "warship.png")).resize((50, 50)))

        self.create_widgets()

    def create_widgets(self):
        banner = Frame(self, bg="black", relief='ridge', bd=1, height=100)
        banner.pack(fill="x")
        create_styled_label(banner, "Welcome to Sakay", font_size=16).pack(pady=5)
        create_styled_label(banner, "San ka punta", font_size=12).pack()

        create_styled_button(self, "MotoTaxi", lambda: self.controller.show_frame("MotoTaxiPage"), image=self.moto_img).pack(side="left", padx=5)
        create_styled_button(self, "4 seater", lambda: self.controller.show_frame("Four_SeaterPage"), image=self.car4_img).pack(side="left", padx=5)
        create_styled_button(self, "6 seater", lambda: self.controller.show_frame("Six_Seater"), image=self.car6_img).pack(side="left", padx=5)
        create_styled_button(self, "Chinese naval Warship", lambda: self.controller.show_frame("ChineseNavalWarship"), image=self.ship_img).pack(side="left", padx=5)

class MotoTaxiPage(Page0, UserInputApp):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)
        create_styled_label(self, "MotoTaxi Booking", font_size=16).pack(pady=10)
        create_styled_label(self, "Enter your destination:", font_size=12).pack(pady=5)
        create_styled_entry(self, "Enter your destination:").pack(pady=5)
        create_styled_button(self, "Back to Home", lambda: self.controller.show_frame("HomePage")).pack(pady=10)

class Four_SeaterPage(Page0, UserInputApp):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)
        create_styled_label(self, "4 seater Booking", font_size=16).pack(pady=10)
        create_styled_label(self, "Enter your destination:", font_size=12).pack(pady=5)
        create_styled_entry(self, "Enter your destination:").pack(pady=5)
        create_styled_button(self, "Back to Home", lambda: self.controller.show_frame("HomePage")).pack(pady=10)

class Six_Seater(Page0, UserInputApp):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)
        create_styled_label(self, "6 seater Booking", font_size=16).pack(pady=10)
        create_styled_label(self, "Enter your destination:", font_size=12).pack(pady=5)
        create_styled_entry(self, "Enter your destination:").pack(pady=5)
        create_styled_button(self, "Back to Home", lambda: self.controller.show_frame("HomePage")).pack(pady=10)

class ChineseNavalWarship(Page0, UserInputApp):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)
        create_styled_label(self, "Chinese Naval Warship Booking", font_size=16).pack(pady=10)
        create_styled_label(self, "Warship Requires Battlepass to access", font_size=12).pack(pady=5)
        create_styled_button(self, "Back to Home", lambda: self.controller.show_frame("HomePage")).pack(pady=10)

class ActivityPage(Page0):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)

class MessagesPage(Page0):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)

class AccountPage(Page0):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)

class Sakay(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Sakay")
        self.geometry("400x500")

        self.page_container = Frame(self)
        self.page_container.pack(fill="both", expand=True)
        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage,
                  ActivityPage,
                  MessagesPage,
                  AccountPage,
                  MotoTaxiPage,
                  Four_SeaterPage,
                  Six_Seater,
                  ChineseNavalWarship):
            page_name = F.__name__
            frame = F(parent=self.page_container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

        nav_bar = Frame(self, bg="black", relief='ridge', bd=1)
        nav_bar.pack(side="bottom", fill="x")
        create_styled_button(nav_bar, "Home", lambda: self.show_frame("HomePage")).pack(side="left", expand=True)
        create_styled_button(nav_bar, "Activity", lambda: self.show_frame("ActivityPage")).pack(side="left", expand=True)
        create_styled_button(nav_bar, "Messages", lambda: self.show_frame("MessagesPage")).pack(side="left", expand=True)
        create_styled_button(nav_bar, "Account", lambda: self.show_frame("AccountPage")).pack(side="left", expand=True)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = Sakay()
    app.mainloop()
