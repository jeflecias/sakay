from tkinter import *

def click():
    print("u-uh")
window = Tk()
window.title("Basic Button Example")
window.geometry("300x200")

logo = PhotoImage(file="pic for cv2.png")
window.iconphoto(True,logo)
window.config(background="black")


#button configx
button = Button(window, text="Click Me",command=click, fg='white', bg='blue', relief=RAISED, bd=10)
button.pack()

window.mainloop()
