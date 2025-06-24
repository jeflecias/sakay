# pinalitan ko yong * kakalat
import tkinter as tk

class UserInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Input")

        self.label = tk.Label(self.root, text="Username: ")
        self.label.config(font=("Consolas", 30))
        self.label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.root)
        self.entry.config(font=('Times New Roman', 50), bg='#111111', fg='#00FF00', width=10)
        self.entry.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        self.submit_button.pack(side=tk.BOTTOM)

    def submit(self):
        username = self.entry.get()
        with open("pickup_location.txt", "a") as file:
            file.write(username + "\n")