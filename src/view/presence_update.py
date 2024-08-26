import tkinter as tk
from tkinter import ttk


class AvailabilityWindow:
    def __init__(self, client):
        self.client = client
        self.master = tk.Toplevel()
        self.master.title("Set Availability")
        self.master.geometry("300x150")

        # Availability state dropdown
        self.availability_label = tk.Label(self.master, text="Availability:")
        self.availability_label.pack(pady=(10, 0))

        self.availability_states = ["Available", "Away", "Do Not Disturb", "Invisible"]
        self.availability_var = tk.StringVar(self.master)
        self.availability_var.set(self.availability_states[0])  # Set default value

        self.availability_dropdown = ttk.Combobox(self.master, textvariable=self.availability_var,
                                                  values=self.availability_states)
        self.availability_dropdown.pack(pady=(0, 10))

        # Custom status text field
        self.status_label = tk.Label(self.master, text="Custom Status:")
        self.status_label.pack()

        self.status_entry = tk.Entry(self.master, width=30)
        self.status_entry.pack(pady=(0, 10))

        # Submit button
        self.submit_button = tk.Button(self.master, text="Set Status", command=self.submit_status)
        self.submit_button.pack()

    def submit_status(self):
        availability = self.availability_var.get()
        custom_status = self.status_entry.get()

        # Map the selected state to XMPP presence values (example)
        xmpp_state = {
            "Available": "chat",  # None means 'available'
            "Away": "away",
            "Do Not Disturb": "dnd",
            "Invisible": "xa"
        }[availability]

        self.client.update_presence(xmpp_state, custom_status)
        self.master.destroy()
