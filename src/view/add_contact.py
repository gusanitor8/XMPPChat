import tkinter as tk
from tkinter import ttk
import asyncio


class AddContact:
    def __init__(self, client, chat_window):
        self.chat_window = chat_window
        self.client = client
        self.contact_entry = None

        # Create a new Toplevel window
        self.form_window = tk.Toplevel()
        self.form_window.title("Add Contact Window")

        # Set the size of the window
        self.form_window.geometry("300x200")

    def initialize(self):
        # Create a label and entry for "Email"
        contact_label = ttk.Label(self.form_window, text="Contact JID:")
        contact_label.pack(pady=5)
        self.contact_entry = ttk.Entry(self.form_window)
        self.contact_entry.pack(pady=5)

        # Create a submit button
        submit_button = ttk.Button(self.form_window, text="Submit",
                                   command=lambda: self.submit_form())
        submit_button.pack(pady=20)

    def submit_form(self):
        new_contact = self.contact_entry.get()
        self.client.add_contact(new_contact)
        self.form_window.destroy()

