import tkinter as tk
from tkinter import ttk
import asyncio


class GroupChatSelector:
    def __init__(self, client, chat_window):
        self.chat_window = chat_window
        self.client = client

        # Create a new Toplevel window
        self.window = tk.Toplevel()
        self.window.title("Select Group Chat")

        # Set a fixed size for the window
        self.window.geometry("300x150")
        self.window.resizable(False, False)

        # List of group chats
        self.group_chats = [""]

        # Create a StringVar to hold the selected group chat
        self.selected_group = tk.StringVar()

        # Set the default option in the dropdown
        self.selected_group.set(self.group_chats[0])

        # Create a dropdown menu for selecting a group chat
        self.group_menu = ttk.OptionMenu(self.window, self.selected_group, *self.group_chats)
        self.group_menu.pack(pady=20)

        # Create a button to confirm the selection
        join_button = ttk.Button(self.window, text="Join Group", command=self.handle_join_group)
        join_button.pack(pady=10)

        asyncio.create_task(self.load_groups())

    async def load_groups(self):
        groups = await self.client.get_all_groups()
        self.update_group_menu(groups)

    def update_group_menu(self, new_groups):
        """Update the dropdown menu with new group chats."""
        self.group_chats = new_groups

        # Clear the old menu items
        self.group_menu['menu'].delete(0, 'end')

        # Add new menu items
        for group in self.group_chats:
            self.group_menu['menu'].add_command(label=group, command=tk._setit(self.selected_group, group))

        # Optionally, set the default value to the first group in the updated list
        self.selected_group.set(self.group_chats[0])

    def handle_join_group(self):
        asyncio.create_task(self.join_group())

    async def join_group(self):
        selected_group = self.selected_group.get()
        await self.client.join_group(selected_group)
        self.chat_window.add_contact(selected_group)
        self.window.destroy()
