import tkinter as tk
from tkinter import ttk
import asyncio


class GroupForm:
    def __init__(self, root, client):
        self.root = root
        self.client = client

    def initialize(self):
        # Create a new Toplevel window
        form_window = tk.Toplevel()
        form_window.title("Form Window")

        # Set the size of the window
        form_window.geometry("300x200")

        # Create a label and entry for "Email"
        email_label = ttk.Label(form_window, text="Group Name:")
        email_label.pack(pady=5)
        email_entry = ttk.Entry(form_window)
        email_entry.pack(pady=5)

        # Create a submit button
        submit_button = ttk.Button(form_window, text="Submit",
                                   command=lambda: self.submit_form(email_entry.get()))
        submit_button.pack(pady=20)

    def submit_form(self, group_name):
        asyncio.create_task(self.client.create_group(group_name))

