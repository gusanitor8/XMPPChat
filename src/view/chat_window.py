import tkinter as tk
import asyncio

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
            self.contacts = ['gon21438-test42@alumchat.lol']
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
            await asyncio.sleep(0.01)  # Yield control to the asyncio event loop

    def receive_message(self, msg_data):
        message = msg_data['body']
        emitter = msg_data['emitter']

        selected_contact = self.contact_var.get()
        if message and selected_contact:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"{emitter}:\n" + message + "\n", "right_align")
            self.chat_display.config(state=tk.DISABLED)

            # Configure the tag for right alignment
            self.chat_display.tag_configure("right_align", justify='right')

    def send_message(self):
        message = self.get_entry()
        selected_contact = self.contact_var.get()
        if message and selected_contact:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"You to {selected_contact}:\n" + message + "\n")
            self.chat_display.config(state=tk.DISABLED)
            self.message_entry.delete(0, tk.END)

            # We send the message
            self.client.send_msg(mto=selected_contact, msg=message)

    def get_entry(self) -> str:
        return self.message_entry.get()

    def initialize_items(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create the main window
        self.root.geometry("400x500")  # Set the fixed size of the window
        self.root.resizable(False, False)  # Disable resizing

        # Create a dropdown menu for selecting a contact
        self.contact_var.set(self.contacts[0])  # Set the default contact
        contact_menu = tk.OptionMenu(self.root, self.contact_var, *self.contacts)
        contact_menu.pack(pady=10)

        # Create the chat display area
        self.chat_display = tk.Text(self.root, state=tk.DISABLED, wrap=tk.WORD)
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Create a frame for the message entry and send button
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        # Create the message entry field
        self.message_entry = tk.Entry(bottom_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Create the send button
        send_button = tk.Button(bottom_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT)

    async def get_input(self):
        """Awaitable function to get input from the user."""
        self.future = self.loop.create_future()
        self.root.bind("<Return>", self.on_enter_pressed)  # Bind Enter key to capture input
        result = await self.future
        self.future = None
        return result

    def on_enter_pressed(self, event):
        """Handler for the Enter key press."""
        if self.future and not self.future.done():
            self.future.set_result(self.message_entry.get())
            self.message_entry.delete(0, tk.END)  # Clear the entry after submission

    def on_closing(self):
        self.is_running = False
        self.root.destroy()