import tkinter as tk
import asyncio
from view.chat_window import ChatWindow
from tkinter import messagebox


class ChatMenu:
    def __init__(self, client):
        self.root = tk.Tk()
        self.client = client
        self.root.title("Chat Options")
        self._initialize_menu()
        self.loop = asyncio.get_event_loop()

    def _initialize_menu(self):
        # Set window size and disable resizing
        self.root.resizable(False, False)

        # Create a list of options
        self.options = [
            "Show all my contacts.",
            "Show a contact info.",
            "Send contact request.",
            "Send a DM.",
            "Send a group message.",
            "Update your presence.",
            "Send a file message.",
            "Sign out."
        ]

        # Display options in the window
        for index, option in enumerate(self.options):
            button = tk.Button(self.root, text=option, command=lambda opt=index: self.handle_option(opt))
            button.pack(pady=5, fill=tk.X, padx=10)

    def handle_option(self, option):
        print("Option chosen: ", option)
        if option == 0:
            contacts = self.client.get_contacts()
            print(contacts)

        elif option == 1:
            pass

        elif option == 2:
            pass

        elif option == 3:
            chat_window = ChatWindow(self.client)
            chat_window.run()

        if hasattr(self, 'future') and self.future and not self.future.done():
            self.future.set_result(option)  # Resolve the future with the chosen option

    async def get_user_choice(self):
        """Awaitable function to get user's menu choice."""
        self.future = self.loop.create_future()
        result = await self.future
        self.future = None
        return result

    def on_closing(self):
        # Code to execute when the window is closing
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()  # Closes the window

    async def run(self):
        # Run the application with asyncio event loop
        while True:
            self.root.update()
            await asyncio.sleep(0.01)  # Yield control to the asyncio event loop
