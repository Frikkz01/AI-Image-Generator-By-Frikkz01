import requests
import io
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ttkbootstrap import Style
from urllib.parse import quote
import threading
import time
import webbrowser
from tkinter import filedialog

# In-memory user storage (username: password)
users = {}

def show_login_popup():
    def login():
        username = username_var.get()
        password = password_var.get()
        if users.get(username) == password:
            login_popup.destroy()
            create_gui()
        else:
            error_label.config(text="Invalid username or password")

    login_popup = tk.Toplevel(root)
    login_popup.title("Login")
    login_popup.geometry("300x200")
    tk.Label(login_popup, text="Username").pack(pady=5)
    username_var = tk.StringVar()
    tk.Entry(login_popup, textvariable=username_var).pack(pady=5)
    tk.Label(login_popup, text="Password").pack(pady=5)
    password_var = tk.StringVar()
    tk.Entry(login_popup, textvariable=password_var, show='*').pack(pady=5)
    tk.Button(login_popup, text="Login", command=login).pack(pady=10)
    error_label = tk.Label(login_popup, text="", fg="red")
    error_label.pack(pady=5)
    tk.Button(login_popup, text="Register", command=show_register_popup).pack(pady=5)

def show_register_popup():
    def register():
        username = username_var.get()
        password = password_var.get()
        if username in users:
            error_label.config(text="Username already exists")
        else:
            users[username] = password
            register_popup.destroy()
            show_login_popup()

    register_popup = tk.Toplevel(root)
    register_popup.title("Register")
    register_popup.geometry("300x200")
    tk.Label(register_popup, text="Username").pack(pady=5)
    username_var = tk.StringVar()
    tk.Entry(register_popup, textvariable=username_var).pack(pady=5)
    tk.Label(register_popup, text="Password").pack(pady=5)
    password_var = tk.StringVar()
    tk.Entry(register_popup, textvariable=password_var, show='*').pack(pady=5)
    tk.Button(register_popup, text="Register", command=register).pack(pady=10)
    error_label = tk.Label(register_popup, text="", fg="red")
    error_label.pack(pady=5)
    tk.Button(register_popup, text="Back to Login", command=register_popup.destroy).pack(pady=5)

def create_gui():
    global category_var, generate_button, label, category_dropdown, switch_button, download_button

    root.title("AI Image Generator By Frikkz01")
    root.geometry("1280x720")
    root.config(bg="white")
    root.resizable(False, False)
    style = Style(theme="sandstone")

    category_var = tk.StringVar(value=texts[current_language]["choose_category"])
    category_dropdown = ttk.OptionMenu(root, category_var, *texts[current_language]["categories"], command=enable_button)
    category_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    category_dropdown.config(width=14)

    generate_button = ttk.Button(text=texts[current_language]["generate_image"], state="disabled", command=lambda: display_image(category_var.get()))
    generate_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    label = tk.Label(root, background="white")
    label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    download_button = ttk.Button(text=texts[current_language]["download_image"], state="disabled", command=download_image)
    download_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")  # Centered below the image
    download_button.config(width=15)  # Set width to make it smaller

    switch_button = ttk.Button(text=texts[current_language]["switch_language"], command=switch_language)
    switch_button.grid(row=3, column=1, padx=10, pady=10, sticky="se")

    github_logo = ImageTk.PhotoImage(Image.open(io.BytesIO(requests.get("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png").content)).resize((30, 30), Image.LANCZOS))
    github_button = tk.Button(root, image=github_logo, command=open_github, borderwidth=0)
    github_button.image = github_logo  # Keep a reference to avoid garbage collection
    github_button.grid(row=3, column=0, padx=10, pady=10, sticky="sw")

    root.columnconfigure([0, 1], weight=1)
    root.rowconfigure([0, 1, 2, 3], weight=1)
    root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    show_login_popup()
    root.mainloop()
