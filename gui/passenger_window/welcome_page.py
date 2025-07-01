from tkinter import Frame, Label

# welcome page for the sakay app
def load_welcome(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    # center content
    center_frame = Frame(frame, bg="#D2B48C")
    center_frame.place(relx=0.5, rely=0.5, anchor="center") 

    # label widgets
    label_1 = Label(center_frame, text="Welcome to Sakay!", fg="#643602", bg="#D2B48C")
    label_2 = Label(center_frame, text="Where are you headed to?", fg="#643602", bg="#D2B48C")
    label_3 = Label(center_frame, text="Click the Home page to start your journey!", fg="#643602", bg="#D2B48C")

    # pack labels inside the frame
    label_1.pack(pady=(10, 0))
    label_2.pack(pady=(0, 10))
    label_3.pack()

    # update font size based on frame
    def update_fonts(event=None):
        try:
            # wag i update kapag nasira na yong widget
            # andaming error sa terminal
            for label in (label_1, label_2, label_3):
                if not label.winfo_exists():
                    return
                
            width = frame.winfo_width()
            main_size = max(int(width * 0.05), 12)
            sub_size = max(int(width * 0.03), 10)
            small_size = max(int(width * 0.02), 8)
            
            label_1.config(font=("Comic Sans MS", main_size, "bold", "italic"))
            label_2.config(font=("Comic Sans MS", sub_size, "bold"))
            label_3.config(font=("Comic Sans MS", small_size))
        except:
            pass

    update_fonts() # initial call to set fonts
    frame.bind("<Configure>", update_fonts) # bind to resize
