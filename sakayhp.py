import tkinter as tk
from backend_for_pickup_location import *
from PIL import Image, ImageTk
#hellow guys sabi ni gpt di daw gagana yung import * unless isa isahin ko sow-
from tkinter import Frame, Label, Button

# don't mind these, gumawa lang ako helper functions para di na masayang oras ko kaka set ng font saka color
def create_styled_label(parent, text, font_size=12):
    return Label(parent,
                 text=text,
                 font=("Times New Roman", font_size),
                 fg='#FFD700',
                 bg='black')
    

#gumawa na den ako ng pang style nung buong button like bg color tas border
def create_styled_button(parent, text,command,font_size=10, image=None):
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
    e.widget['background'] = '#FFD700'  # shiny effect
    e.widget['fg'] = 'black'
    e.widget['relief'] = 'ridge'
    e.widget['bd'] = '2'


def cursor_not_hovering(e):
    e.widget['background'] = 'black' #default na itsura nong button
    e.widget['fg'] = '#FFD700'
    e.widget['relief'] = 'ridge'
    e.widget['bd'] = '2'

# base page or parent class
class Page0(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')

class HomePage(Page0):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        #Lagay ko here mga image (temporary lng)
        self.moto_img = ImageTk.PhotoImage(Image.open("motor.png").resize((64, 64)))
        self.car4_img = ImageTk.PhotoImage(Image.open("sedan.png").resize((64, 64)))
        self.car6_img = ImageTk.PhotoImage(Image.open("van.png").resize((64, 64)))
        self.ship_img = ImageTk.PhotoImage(Image.open("warship.png").resize((50, 50)))
        self.create_widgets()

                


    def create_widgets(self):
        # Welcoming Banneryeheyyyyy
        banner = Frame(self, bg="black", relief='ridge', bd=1, height=100)
        banner.pack(fill="x")
        create_styled_label(banner, "Welcome to Sakay", font_size=16).pack(pady=5)
        create_styled_label(banner, "San ka punta", font_size=12).pack()

        # Vehicle options naten
        create_styled_button(self,
                             "MotoTaxi", 
                             lambda: self.controller.show_frame("MotoTaxiPage"),
                             image=self.moto_img).pack(side="left", padx=5)
        create_styled_button(self,
                             "4 seater",
                             lambda: self.controller.show_frame("Four_SeaterPage"),
                             image=self.car4_img).pack(side="left", padx=5)
        create_styled_button(self,
                             "6 seater",
                             lambda: self.controller.show_frame("Six_Seater"),
                             image=self.car6_img).pack(side="left", padx=5)
        create_styled_button(self,
                             "Chinese naval Warship",
                             lambda: self.controller.show_frame("ChineseNavalWarship"),
                             image=self.ship_img).pack(side="left", padx=5)

# gumawa aq dito ng frames or pages for each selection ng vehicles naten para sa kanya kanyang vehicle
class MotoTaxiPage(Page0, UserInputApp):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller,)
        create_styled_label(self,
                            "MotoTaxi Booking", 
                            font_size=16).pack(pady=10)
        create_styled_label(self, 
                            "Enter your destination:", 
                            font_size=12).pack(pady=5)
        create_styled_entry(self, 
                            "Enter your destination:").pack(pady=5)
        create_styled_button(self, 
                             "Back to Home", 
                             lambda: self.controller.show_frame("HomePage")).pack(pady=10)

class Four_SeaterPage(Page0, UserInputApp):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)
        create_styled_label(self, 
                            "4 seater Booking", 
                            font_size=16).pack(pady=10)
        create_styled_label(self, 
                            "Enter your destination:", 
                            font_size=12).pack(pady=5)
        create_styled_entry(self, 
                            "Enter your destination:").pack(pady=5)
        create_styled_button(self, 
                             "Back to Home", 
                             lambda: self.controller.show_frame("HomePage")).pack(pady=10)

class Six_Seater(Page0, UserInputApp):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)
        create_styled_label(self, 
                            "6 seater Booking", 
                            font_size=16).pack(pady=10)
        create_styled_label(self, 
                            "Enter your destination:", 
                            font_size=12).pack(pady=5)
        create_styled_entry(self, 
                            "Enter your destination:").pack(pady=5)
        create_styled_button(self, 
                             "Back to Home", 
                             lambda: self.controller.show_frame("HomePage")).pack(pady=10)

class ChineseNavalWarship(Page0, UserInputApp):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)
        create_styled_label(self, 
                            "Chinese Naval Warship Booking", 
                            font_size=16).pack(pady=10)
        create_styled_label(self, 
                            "Warship Requires Battlepass to access", 
                            font_size=12).pack(pady=5)
        create_styled_button(self, 
                             "Back to Home", 
                             lambda: self.controller.show_frame("HomePage")).pack(pady=10)

# Bottom navigation bar para di ka maligaw mwa (wala pa q inaadd sa loob ng mga frames nila)
class ActivityPage(Page0):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)

class MessagesPage(Page0):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)

class AccountPage(Page0):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)

# constructor ng everything,pag mag aadd kayo ng page isama nyo sa loop para di mawala sa ouput
# dito den nkalagay yung configurations naten
class Sakay(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Sakay")
        self.geometry("400x500")

        # Main container for pages
        self.page_container = Frame(self)
        self.page_container.pack(fill="both", expand=True)

        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # constructer loop ng mga frame
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

        # bottom navigation bar configurations
        nav_bar = Frame(self, bg="black", relief='ridge', bd=1)
        nav_bar.pack(side="bottom", fill="x")
        create_styled_button(nav_bar,
                             "Home",
                             lambda: self.show_frame("HomePage")).pack(side="left",expand=True)
        create_styled_button(nav_bar,
                             "Activity",
                             lambda: self.show_frame("ActivityPage")).pack(side="left", expand=True)
        create_styled_button(nav_bar,
                             "Messages",
                             lambda: self.show_frame("MessagesPage")).pack(side="left", expand=True)
        create_styled_button(nav_bar,
                             "Account",
                             lambda: self.show_frame("AccountPage")).pack(side="left", expand=True)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = Sakay()
    app.mainloop()

# yeheyyyy
# ang galing 