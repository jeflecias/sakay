from tkinter import Frame, Label, Button
from PIL import Image, ImageTk
import os
from utils import cursor_hovering, cursor_not_hovering

image_refs = []
image_labels = []
selected_vehicle = {"name": None}
confirm_button = None

# absolute path for images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# vehicle selection confirmation
def confirm_selection():
    if selected_vehicle["name"]:
        print(f"Confirmed: {selected_vehicle['name']} selected")
    else:
        print("No vehicle selected")

# resize images and display in the center frame
def resize_and_display_images(center_frame, width):
    global confirm_button

    # clear previous images and labels
    for label in image_labels:
        label.destroy()
    image_labels.clear()
    image_refs.clear()
    if confirm_button:
        confirm_button.destroy()
        confirm_button = None

    # create a new frame for vehicle selection
    Label(center_frame, text="What vehicle would you want to choose?", font=("Comic Sans MS", 16, "bold"),
          fg="#643602", bg="#D2B48C").pack(pady=(10, 5))
    
    # create a frame to hold the vehicle options
    vehicle_frame = Frame(center_frame, bg="#D2B48C")
    vehicle_frame.pack(pady=10)

    # kng pano adjust ang icon size base sa frame
    icon_size = max(min(width // 6, 200), 20)

    # create vehicle options
    def create_option(label_text, image_path):
        # abs image path, batas na to
        image_path = os.path.join(BASE_DIR, "img", image_path)

        subframe = Frame(vehicle_frame, bg="#D2B48C", highlightbackground="white", highlightthickness=2)
        subframe.pack(side="left", padx=10, pady=10, expand=True)

        # selection handler
        def on_select():
            for label in image_labels:
                label.config(highlightbackground="white")
            subframe.config(highlightbackground="#5DA83F")
            selected_vehicle["name"] = label_text

        # create icon label
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path).resize((icon_size, icon_size))
                photo = ImageTk.PhotoImage(img)
                image_refs.append(photo)
                icon = Label(subframe, image=photo, bg="#D2B48C")

            # debug results if image=not loading/available
            else: 
                icon = Label(subframe, text="❌", fg="red", bg="#D2B48C", font=("Comic Sans MS", 20, "bold"))
        except Exception:
            icon = Label(subframe, text="⚠️", fg="orange", bg="#D2B48C", font=("Comic Sans MS", 20, "bold"))

        # bind icon and label click to select vehicle
        icon.bind("<Button-1>", lambda e: on_select())
        icon.pack()
        label = Label(subframe, text=label_text, fg="#643602", bg="#D2B48C", font=("Comic Sans MS", 10))
        label.pack()
        label.bind("<Button-1>", lambda e: on_select())

        image_labels.append(subframe) # store subframe for later use

    # vehicle options and their file paths
    create_option("UFO", "ufo.png")
    create_option("Tank", "tanke.png")
    create_option("Space Shuttle", "spshuttle.png")
    create_option("Jet Fighter", "jetf.png")

    # confirm button
    confirm_button = Button(center_frame, text="Confirm Selection", font=("Comic Sans MS", 12, "bold"),
                            fg="white", bg="#5E7530", command=confirm_selection)
    confirm_button.bind("<Enter>", cursor_hovering)
    confirm_button.bind("<Leave>", cursor_not_hovering)
    confirm_button.pack(pady=20)

# home page for sakay app
def load_home(frame):
    for widget in frame.winfo_children():
        widget.destroy() 

    # center frame to hold content
    center_frame = Frame(frame, bg="#D2B48C")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    # create label widgets
    frame.update_idletasks()
    width = frame.winfo_width() or 480
    resize_and_display_images(center_frame, width)

    # resize when app is adjusted
    # error checking as well, hndi ako sure if eto yong mismong problema
    def on_resize(event):
        try:
            if not center_frame.winfo_exists():
                return
            for widget in center_frame.winfo_children():
                widget.destroy()
            resize_and_display_images(center_frame, event.width)
        except:
            pass

    frame.bind("<Configure>", on_resize) # bind to resize