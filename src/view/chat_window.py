import tkinter as tk
import asyncio
import os
from tkinter import filedialog
from tkinter import messagebox


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
            self.contact_var = tk.StringVar(self.root)
            self.contacts = [""] + client.get_contacts()
            self.client = client
            self.initialize_items()
            self._initialized = True
            self.is_running = False
            self.loop = asyncio.get_event_loop()

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

    def get_entry(self) -> str:
        return self.message_entry.get()

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
            "Show all my contacts.",  # check
            "Show a contact info.",
            "Send contact request.",
            "Send a DM.",
            "Send a group message.",
            "Update your presence.",
            "Send a file message.",
            "Sign out."
        ]

        for index, option in enumerate(options):
            button = tk.Button(menu_frame, text=option, command=lambda opt=index: self.handle_option(opt))
            button.pack(pady=5, fill=tk.X, padx=10)

        # Create a frame for the chat area on the right side
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create a dropdown menu for selecting a contact
        self.contact_var.set(self.contacts[0])  # Set the default contact
        contact_menu = tk.OptionMenu(chat_frame, self.contact_var, *self.contacts)
        contact_menu.pack(pady=10)

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



    def handle_option(self, option):
        # Implement functionality for each option as needed
        if option == 0:
            contacts = self.client.get_contacts()
            print(contacts)

        if option == 1:
            contact = self.contact_var.get()
            details = self.client.get_contact_details(contact)

            if details:
                print(details)

        elif option == 3:
            # Example: Open the chat window when "Send a DM" is selected
            self.run()

        elif option == 7:
            self.sign_out()

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
