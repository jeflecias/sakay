from tkinter import *

class UserInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Input")

        # Label
        self.label = Label(self.root, text="Username: ")
        self.label.config(font=("Consolas", 30))
        self.label.pack(side=LEFT)

        # Entry
        self.entry = Entry(self.root)
        self.entry.config(font=('Times New Roman', 50), bg='#111111', fg='#00FF00', width=10)
        self.entry.pack()

        # Button
        self.submit_button = Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(side=BOTTOM)

    def submit(self):
        username = self.entry.get()
        with open("pickup_location.txt", "a") as file:
            file.write(username + "\n")
