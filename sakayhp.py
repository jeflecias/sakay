import tkinter as tk
from tkinter import ttk

def create_app():
    root = tk.Tk()
    root.title("sakay")
    root.geometry("400x600")  

    #home page header
    header_frame = tk.Frame(root, bg='black', height=120, relief='ridge', bd=5)
    header_frame.pack(fill='x')

    #home page welcoming text
    header_label = tk.Label(header_frame, text="Welcome to Sakay", bg='black', fg='#23fa43', font=('Times New Roman', 20))
    header_label.pack(pady=5)
    subheader_label = tk.Label(header_frame, text="gew lang", bg='black', fg='#23fa43', font=('Times New Roman', 12))
    subheader_label.pack()

    #image o logo basta
    illustration_label = tk.Label(header_frame, text="dito naten lagay logo", bg='black', fg='#23fa43', font=('Times New Roman', 12))
    illustration_label.pack(pady=10)

    # main frame/body
    content_frame = tk.Frame(root, bg='black', relief='ridge', bd=5)
    content_frame.pack(fill='both', expand=True)

    #motor selection
    moto_label = tk.Label(content_frame, text="Motor", bg='black', fg='#23fa43', font=('Times New Roman', 16), relief='ridge', bd=5)
    moto_label.pack(pady=20)

    #4seater car selection
    moto_label = tk.Label(content_frame, text="4 seater car", bg='black', fg='#23fa43', font=('Times New Roman', 16), relief='ridge', bd=5)
    moto_label.pack(pady=20)

    #6 seater selection
    moto_label = tk.Label(content_frame, text="6 seater", bg='black', fg='#23fa43', font=('Times New Roman', 16), relief='ridge', bd=5)
    moto_label.pack(pady=20)

    #North Korean Warship selection
    moto_label = tk.Label(content_frame, text="North Korean Warship", bg='black', fg='#23fa43', font=('Times New Roman', 16), relief='ridge', bd=5)
    moto_label.pack(pady=20)

    #bottom navigation bar
    nav_frame = tk.Frame(root, bg='black', height=50, relief='ridge', bd=5)
    nav_frame.pack(fill='x')

    #other pages n shi
    home_button = tk.Button(nav_frame, text="Home", bg='black', fg='#23fa43',font=('Times New Roman',12), relief='ridge', bd=5)
    home_button.pack(side='left', padx=10)
    activity_button = tk.Button(nav_frame, text="Activity", bg='black', fg='#23fa43',font=('Times New Roman',12), relief='ridge', bd=5)
    activity_button.pack(side='left', padx=10)
    messages_button = tk.Button(nav_frame, text="Messages", bg='black', fg='#23fa43',font=('Times New Roman',12), relief='ridge', bd=5)
    messages_button.pack(side='left', padx=10)
    account_button = tk.Button(nav_frame, text="Account", bg='black', fg='#23fa43',font=('Times New Roman',12), relief='ridge', bd=5)
    account_button.pack(side='left', padx=10)

    root.mainloop()

create_app()
