import tkinter as tk
from passenger_window.home_page import load_home
from passenger_window.activity_page import load_activity
from passenger_window.messages_page import load_messages
from passenger_window.account_page import load_account
from passenger_window.welcome_page import load_welcome
from utils import cursor_hovering, cursor_not_hovering

def open_passenger(parent, uid):
    passenger_frame = tk.Frame(parent, bg="#D2B48C")
    passenger_frame.place(relwidth=1, relheight=1)

    # main content area
    content_frame = tk.Frame(passenger_frame, bg="#D2B48C")
    content_frame.pack(expand=True, fill="both")

    # higlight when clicked
    clicked_button = tk.Frame(passenger_frame, bg="#A1866F", bd=2, relief="ridge")
    clicked_button.pack(side="bottom", fill="x", pady=10)

    # button frame
    button_frame = tk.Frame(clicked_button, bg="#D2B48C")
    button_frame.pack(padx=5, pady=5, fill="x")

    highlight_frame = tk.Frame(button_frame, bg="#79674F", height=3) # highlight bar

    navigation_buttons = {} # dictionary to track nav buttons

    def switch_page(name, load_function):
        # load the corresponding page
        load_function(content_frame)

        # reset all button backgrounds
        for key, button in navigation_buttons.items():
            button.configure(bg="#D2B48C")

        if name == "Home":
            # highlight only if Home is clicked
            navigation_buttons[name].configure(bg="#A16F36")
            highlight_frame.place(
                in_=navigation_buttons[name],
                relx=0, rely=1.0,
                relwidth=1.0, anchor="sw"
            )
        else:
            highlight_frame.place_forget()  # remove highlight for other buttons

    # Create each navigation button
    def create_page_button(name, load_function):
        button = tk.Button(
            button_frame,
            text=name,
            font=("Comic Sans MS", 10),
            fg="#643602",
            bg="#D2B48C",
            relief="flat",
            width=12,
            command=lambda: switch_page(name, lambda f: load_function(f, uid))
        )
        button.bind("<Enter>", cursor_hovering)
        button.bind("<Leave>", cursor_not_hovering)
        button.pack(side="left", expand=True, padx=10)
        navigation_buttons[name] = button

    # create page buttons
    create_page_button("Home", load_home)
    create_page_button("Activity", load_activity)
    create_page_button("Messages", load_messages)
    create_page_button("Account", load_account)

    # load welcome page on start (without highlight)
    load_welcome(content_frame)

    # for future use
    return passenger_frame