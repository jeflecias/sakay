import tkinter as tk
#kelangan ko isa isahin amp
from tkinter import Frame, Label, Button

class Page0(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black', relief='ridge',bd=5)

class HomePage(Page0):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)
        self.create_widgets()

    def create_widgets(self):
        # welcoming banneryheyyy
        banner = Frame(self, bg="black", relief='ridge', bd=5, height=100)
        banner.pack(fill="x")
        Label(banner, text="Welcome to Sakay", font=("Times New Roman", 16), fg="#4ff244", bg="black").pack(pady=5)
        Label(banner, text="San ka punta", font=("Times New Roman", 12), fg="#4ff244", bg="black").pack()

        # Vehicle selection buttons
        Button(self, text="MotoTaxi", fg='#4ff244', bg='black', relief='ridge', bd=5,
         command=lambda: self.controller.show_frame("MotoTaxiPage")).pack(pady=20)
        Button(self, text="4 seater", fg='#4ff244', bg='black', relief='ridge', bd=5,
         command=lambda: self.controller.show_frame("Four_SeaterPage")).pack(pady=20)
        Button(self, text="6 seater", fg='#4ff244', bg='black', relief='ridge', bd=5,
         command=lambda: self.controller.show_frame("Six_Seater")).pack(pady=20)
        Button(self, text="Chinese naval Warship", fg='#4ff244', bg='black', relief='ridge', bd=5,
         command=lambda: self.controller.show_frame("ChineseNavalWarship")).pack(pady=20)

#dito yung mga page ng kanya kanyang option sa sasakyan

class MotoTaxiPage(Page0):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)
        Label(self, text="MotoTaxi Booking", font=("Times New Roman", 16)).pack(pady=10)
        Label(self, text="Enter your destination:", font=("Times New Roman", 12)).pack(pady=5)
        Button(self, text="Back to Home", command=lambda: self.controller.show_frame("MotoTaxiPage")).pack(pady=10)

class Four_SeaterPage(Page0):
    def __init__(self, parent, controller):
        Page0.__init__(self,parent, controller)
        Label(self, text="4 seater Booking", font=("Times New Roman", 16)).pack(pady=10)
        Label(self, text="Enter your destination: ", font=("Times new Roman", 12)).pack(pady=5)
        Button(self, text="back to Home", command=lambda: self.controller.show_frame("Four_SeaterPage")).pack(pady=10)

class Six_Seater(Page0):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)
        Label(self, text="6 seater Booking", font=("Times New Roman", 16)).pack(pady=10)
        Label(self, text="Enter your destination:", font=("Times New Roman", 12)).pack(pady=5)
        Button(self, text="Back to Home", command=lambda: self.controller.show_frame("Six_Seater")).pack(pady=10)

class ChineseNavalWarship(Page0):
    def __init__(self, parent, controller):
        Page0.__init__(self, parent, controller)
        Label(self, text="Chinese NavalWarship Booking", font=("Times New Roman", 16)).pack(pady=10)
        Label(self, text="Enter your destination:", font=("Times New Roman", 12)).pack(pady=5)
        Button(self, text="Back to Home", command=lambda: self.controller.show_frame("ChineseNavalWarship")).pack(pady=10)




#Eto nman mga classes para sa Bottom task bar
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

        # Main layout ng frames
        self.page_container = Frame(self)
        self.page_container.pack(fill="both", expand=True)

        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, ActivityPage, MessagesPage, AccountPage, MotoTaxiPage, Four_SeaterPage, Six_Seater, ChineseNavalWarship):
            page_name = F.__name__
            frame = F(parent=self.page_container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

        # bottom navigation bar
        nav_bar = Frame(self, bg="black", relief='ridge', bd=5)
        nav_bar.pack(side="bottom", fill="x")
        Button(nav_bar, text="Home", fg='#4ff244', bg='black', relief='ridge', bd=5, command=lambda: self.show_frame("HomePage")).pack(side="left", expand=True)
        Button(nav_bar, text="Activity", fg='#4ff244', bg='black', relief='ridge', bd=5, command=lambda: self.show_frame("ActivityPage")).pack(side="left", expand=True)
        Button(nav_bar, text="Messages", fg='#4ff244', bg='black', relief='ridge', bd=5, command=lambda: self.show_frame("MessagesPage")).pack(side="left", expand=True)
        Button(nav_bar, text="Account", fg='#4ff244', bg='black', relief='ridge', bd=5, command=lambda: self.show_frame("AccountPage")).pack(side="left", expand=True)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()



if __name__ == "__main__":
    app = Sakay()
    app.mainloop()