# Importing Tkinters
from tkinter import *

class MyApp:
    def __init__(self, parent):
        self.parent = parent
        self.main_frame = Frame(parent)
        self.main_frame.pack(expand=True)
        
        label = Label(self.main_frame, text="Hello, Everyone!", font=("impact", 16), fg="white", bg="blue", relief=RAISED, bd=10)
        label.pack()
        
        self.tab_frame = LabelFrame(self.main_frame, text="This is the object of interest", font=("impact", 11), bg='blue', fg='white', relief=RAISED, bd=10)
        self.tab_frame.pack()
        
        self.tab_button = Button(self.tab_frame, text="Tabs", font=("impact", 20), padx=20, pady=20, command=self.open_frame, bg='#b402f5', fg='white', relief=RAISED, bd=10)
        self.tab_button.pack()
        
        self.label_button = Button(self.tab_frame, text="Label", font=("impact", 20), padx=20, pady=20, command=self.open_label,fg='white',bg='#b402f5', relief=RAISED, bd=10)
        self.label_button.pack()
        
        self.button_button = Button(self.tab_frame, text="Button", font=("impact", 20), padx=20, pady=20, command=self.open_button,fg='white',bg='#b402f5', relief=RAISED, bd=10)
        self.button_button.pack()
        
        self.button_checker = Button(self.tab_frame, text="Button checker", font=("impact", 20), padx=20, pady=20, command=self.open_button_checker,fg='white',bg='#b402f5', relief=RAISED, bd=10)
        self.button_checker.pack()
        
        self.exit_button = Button(self.tab_frame, text="Exit", font=("impact", 20), padx=20, pady=20, command=self.parent.destroy,fg='white', bg='#b402f5', relief=SUNKEN, bd=10)
        self.exit_button.pack()
        
    def open_frame(self):
        new_window = Toplevel(self.parent)
        new_window.geometry("500x500")
        new_window.title("Tabs")
        
        frame = Frame(new_window, bg="#b402f5")
        frame.pack(expand=True)
        
        label = Label(frame, text="This is a tab", font=("impact", 16),fg='white', bg="#f502ed", relief=RAISED, bd=10)
        label.pack(pady=20)
        
    def open_label(self):
        new_window = Toplevel(self.parent)
        new_window.geometry("500x500")
        new_window.title("Label")
        
        frame = Frame(new_window, bg="#f502ed", relief=RAISED, bd=10)
        frame.pack(expand=True)
        
        label = Label(frame, text="This is a label", font=("impact", 16),fg='white', bg="#1307f2", relief=RAISED, bd=10)
        label.pack(pady=20)
        
    def open_button(self):
        new_window = Toplevel(self.parent)
        new_window.geometry("500x500")
        new_window.title("Button")
        
        frame = Frame(new_window, bg="#f502ed", relief=RAISED, bd=10)
        frame.pack(expand=True)
        
        label = Label(frame, text="This is a button", font=("Arial", 16),fg='white', bg="#1307f2", relief=RAISED, bd=10)
        label.pack(pady=20)
        
        button = Button(frame, text="Click me", font=("Arial", 20),fg='white', bg="#1307f2", padx=20, pady=20, command=self.parent.destroy, relief=RAISED, bd=10)
        button.pack(pady=20)
        
        label = Label(frame, text="Click it to close all of the tabs", font=("Arial", 17),fg='white', bg="#1307f2", relief=RAISED, bd=10)
        label.pack(pady=20)
        
    def open_button_checker(self):
        new_window = Toplevel(self.parent)
        new_window.title("Button checker")
        new_window.geometry("500x500")
        
        frame = Frame(new_window, bg="blue", relief=RAISED, bd=10)
        frame.pack(expand=True)
        
        label = Label(frame, text="This is a frame", font=("impact", 16),fg='white', bg="#f502ed", relief=RAISED, bd=10)
        label.pack(pady=20)
        
        self.result_label = Label(frame, text="hey guys", font=("impact", 10),fg='white', bg="blue")
        self.result_label.pack(pady=20)
        
        label = Label(frame, text="Checkbutton is off", font=("impact", 16),fg='white',bg="#f502ed", relief=RAISED)
        label.pack(pady=20)
        
        self.check_var = IntVar()
        self.check_button = Checkbutton(frame, text="Check", font=("impact", 16),fg='#f5f2f3', bg="#f502ed", padx=20, pady=20, command=self.update_window, variable=self.check_var, relief=RAISED, bd=10)
        self.check_button.pack(pady=20)
        
        self.exit_button = Button(frame, text="Close", font=("impact", 16),fg='black', bg="#ff0303", padx=20, pady=20, command=new_window.destroy, relief=SUNKEN, bd=10)
        self.exit_button.pack(pady=20)
        
    def update_window(self):
        if self.check_var.get() == 1:
            self.result_label.config(text="Checkbutton is on")
        else:
            self.result_label.config(text="Checkbutton is off")
            
if __name__ == "__main__":
    root = Tk()
    root.geometry("500x500")
    app = MyApp(root)
    root.mainloop()
