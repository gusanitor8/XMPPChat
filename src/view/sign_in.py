import tkinter as tk
from tkinter import messagebox
from view.chat_window import ChatWindow
from view.signed_menu import ChatMenu
from model.client import Client
import asyncio


class LoginForm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Form")
        self.email_entry = None
        self.password_entry = None
        self.initialize_items()

    def run(self):
        # Run the application
        self.root.mainloop()

    def submit_form(self):
        # We validate the form
        email = self.get_email()
        password = self.get_password()
        if not email or not password:
            messagebox.showwarning("Input Error", "Please fill in both fields")
            return

        client = Client(email, password)
        client.connect(disable_starttls=True, use_ssl=False)
        client.process(forever=False, timeout=10)

    def get_email(self) -> str:
        return self.email_entry.get()

    def get_password(self) -> str:
        return self.password_entry.get()

    def initialize_items(self):
        # Create the main window
        self.root.geometry("400x150")  # Set the fixed size of the window
        self.root.resizable(False, False)  # Disable resizing

        # Create a frame for the email and password fields
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Create the email label and entry field
        email_label = tk.Label(form_frame, text="Email:")
        email_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        # Create the password label and entry field
        password_label = tk.Label(form_frame, text="Password:")
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Create the submit button
        submit_button = tk.Button(self.root, text="Submit", command=self.submit_form)
        submit_button.pack(pady=10)
