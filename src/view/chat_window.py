import tkinter as tk
import asyncio
import os
from tkinter import filedialog
from tkinter import messagebox
from model.services import MUC_SERVICE
from view.group_form import GroupForm
from view.groupchat_selector import GroupChatSelector
from view.add_contact import AddContact
from view.presence_update import AvailabilityWindow


class ChatWindow:
    _instance = None

    def __new__(cls, client, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ChatWindow, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, client):
        if not hasattr(self, '_initialized'):  # Ensure __init__ is only called once
            self.root = tk.Tk()
            self.root.title = "XMPP Chat Window"
            self.chat_display = None
            self.message_entry = None
            self.contact_menu = None
            self.dropdown_frame = None
            self.contact_var = tk.StringVar(self.root)
            self.contacts = [""] + client.get_contacts()
            self.client = client
            self.initialize_items()
            self._initialized = True
            self.is_running = False
            client.set_chat_window(self)
            self.loop = asyncio.get_event_loop()
            asyncio.create_task(self.initialize_contacts_and_groups())

    async def initialize_contacts_and_groups(self):
        # We add the groups we are in to the contact list
        groups = await self.client.get_joined_groups()
        self.contacts += groups
        self.update_dropdown()

    def update_dropdown(self):
        # Clear the old menu items
        self.contact_menu['menu'].delete(0, 'end')

        # Add new menu items
        for contact in self.contacts:
            self.contact_menu['menu'].add_command(label=contact, command=tk._setit(self.contact_var, contact))

        # Optionally, you can set the default value to the first contact in the updated list
        self.contact_var.set(self.contacts[0])

    def add_contact(self, new_contact):
        self.contacts.append(new_contact)
        self.update_dropdown()

    def run(self):
        # Run the application
        asyncio.ensure_future(self.run_tk())  # Run the Tkinter event loop in asyncio
        self.is_running = True

    async def run_tk(self):
        while self.is_running:
            self.root.update()
            await asyncio.sleep(0.1)  # Yield control to the asyncio event loop

    def receive_message(self, msg_data):
        message = msg_data['body']
        emitter = msg_data['emitter']

        selected_contact = self.contact_var.get()
        if message and selected_contact:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"{emitter}:\n" + message + "\n", "right_align")
            self.chat_display.config(state=tk.DISABLED)

            self.notify(f"From {emitter}", message)

    def send_message(self):
        message = self.get_entry()
        selected_contact = self.contact_var.get()
        if message and selected_contact:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"You to {selected_contact}:\n" + message + "\n", "sender")
            self.chat_display.config(state=tk.DISABLED)
            self.message_entry.delete(0, tk.END)

            # We send the message
            self.client.send_msg(mto=selected_contact, msg=message)

    def create_group(self):
        group_form = GroupForm(self.root, self.client)
        group_form.initialize()

    def get_entry(self) -> str:
        return self.message_entry.get()

    def handle_option(self, option):
        if option == 0:
            contact = self.contact_var.get()
            details = self.client.get_contact_details(contact)

            if details:
                print(details)

        elif option == 1:
            contact_form = AddContact(self.client, self)
            contact_form.initialize()

        elif option == 2:
            GroupChatSelector(self.client, self)

        elif option == 3:
            self.create_group()

        elif option == 4:
            AvailabilityWindow(self.client)

        elif option == 5:
            self.sign_out()

    def initialize_items(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Set up the main window
        self.root.geometry("600x500")  # Adjusted size to accommodate the menu
        self.root.resizable(False, False)  # Disable resizing

        # Create a frame for the menu on the left side
        menu_frame = tk.Frame(self.root, width=200)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create the options in the menu
        options = [
            "Show a contact info.",  # 1
            "Send contact request.",  # 2
            "Join a Group",  # 3
            "Create a Group",  # 4
            "Update your presence.",  # 5
            "Sign out."  # 6
        ]

        for index, option in enumerate(options):
            button = tk.Button(menu_frame, text=option, command=lambda opt=index: self.handle_option(opt))
            button.pack(pady=5, fill=tk.X, padx=10)

        # Create a frame for the chat area on the right side
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create a frame for the dropdown menu and info button
        self.dropdown_frame = tk.Frame(chat_frame)
        self.dropdown_frame.pack(pady=10, anchor='w')

        # Create a dropdown menu for selecting a contact
        self.contact_var.set(self.contacts[0])  # Set the default contact
        self.contact_menu = tk.OptionMenu(chat_frame, self.contact_var, *self.contacts)
        self.contact_menu.pack(pady=10)

        # Create an info button next to the dropdown menu
        info_button = tk.Button(self.dropdown_frame, text="ℹ️", command=self.show_contact_info)
        info_button.pack(side=tk.LEFT, padx=5)

        # Create the chat display area
        self.chat_display = tk.Text(chat_frame, state=tk.DISABLED, wrap=tk.WORD)
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Add tag configurations for colored text
        self.chat_display.tag_configure("sender", foreground="#ffd5b8")
        self.chat_display.tag_configure("right_align", justify='right', foreground="#b8c8ff")

        # Create a frame for the message entry and send button
        bottom_frame = tk.Frame(chat_frame)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        # Create the message entry field
        self.message_entry = tk.Entry(bottom_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Create send file button
        send_file_button = tk.Button(bottom_frame, text="📁", command=self.handle_select_file)
        send_file_button.pack(side=tk.RIGHT)

        # Create the send button
        send_button = tk.Button(bottom_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT)

    def show_contact_info(self):

        # Client roster containing the contacts.
        client_roster = self.client.client_roster
        contact: str = self.contact_var.get()

        if contact.endswith(MUC_SERVICE):
            messagebox.showinfo("Alert", "This is a groupchat")
            return

        if contact not in client_roster:
            messagebox.showinfo("Alert", f"Information not found for contact: {contact}")
            return

        # Predetermined values.
        presence_value = "Offline"
        status = "None"

        # Iterating through the contact's information.
        for _, presence in client_roster.presence(contact).items():
            # Show contact's presence.
            presence_value = presence["show"] or "Offline"

            # Show contact's status.
            status = presence["status"] or "None"

            messagebox.showinfo("Alert", f"{contact}\nPresence: {presence_value}\nStatus: {status}")

    def select_file(self):
        # Open a file dialog and return the path to the selected file
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )

        # Print the selected file path or use it in your application
        if file_path:
            print("Selected file:", file_path)
            return file_path
        else:
            print("No file selected")
            return None

    def handle_select_file(self):
        file_path = self.select_file()
        selected_contact = self.contact_var.get()

        if not file_path:
            messagebox.showinfo("Alert", "Please select a valid file")
            return

        asyncio.create_task(self.client.send_file(mto=selected_contact, file_path=file_path))

        # We display it to the user
        selected_contact = self.contact_var.get()
        if selected_contact:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"You to {selected_contact}:\nYou have sent a file! \n", "sender")
            self.chat_display.config(state=tk.DISABLED)
            self.message_entry.delete(0, tk.END)

    def notify(self, title, text):
        os.system("""
                  osascript -e 'display notification "{}" with title "{}"'
                  """.format(text, title))

    def sign_out(self):
        self.is_running = False
        self.client.disconnect()
        self.root.destroy()

    async def get_input(self):
        """Awaitable function to get input from the user."""
        self.future = self.loop.create_future()
        result = await self.future
        self.future = None
        return result

    def on_closing(self):
        self.sign_out()
