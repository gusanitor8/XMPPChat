import tkinter as tk
from src.model.client import Client


class ChatMenu:
    def __init__(self, client: Client):
        self.root = tk.Tk()
        self.client = client
        self.root.title("Chat Options")
        self._initialize_menu()

    def _initialize_menu(self):
        # Set window size and disable resizing
        self.root.resizable(False, False)

        # Create a list of options
        options = [
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
        for index, option in enumerate(options):
            button = tk.Button(self.root, text=option, command=lambda opt=index: self.handle_option(opt))
            button.pack(pady=5, fill=tk.X, padx=10)

    def handle_option(self, option):
        # Handle each menu option (to be implemented)
        print(f"Selected option: {option}")

    def run(self):
        # Run the application
        self.root.mainloop()
