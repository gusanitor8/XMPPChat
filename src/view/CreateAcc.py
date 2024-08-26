import tkinter as tk
from tkinter import ttk, messagebox
from model.AccountCreator import register_new_user

class CreateAccountWindow:
    def __init__(self):
        self.master = tk.Toplevel()
        self.master.title("Create XMPP Account")
        self.master.geometry("300x250")

        # Username field
        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.pack(pady=(10, 0))
        self.username_entry = tk.Entry(self.master, width=30)
        self.username_entry.pack()

        # Password field
        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.pack(pady=(10, 0))
        self.password_entry = tk.Entry(self.master, width=30, show="*")
        self.password_entry.pack()

        # Confirm Password field
        self.confirm_password_label = tk.Label(self.master, text="Confirm Password:")
        self.confirm_password_label.pack(pady=(10, 0))
        self.confirm_password_entry = tk.Entry(self.master, width=30, show="*")
        self.confirm_password_entry.pack()

        # Create Account button
        self.create_button = tk.Button(self.master, text="Create Account", command=self.create_account)
        self.create_button.pack(pady=(20, 0))

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        success = register_new_user(username, password)

        if success:
            messagebox.showinfo("Success", "Account created successfully!")
            self.master.destroy()
        else:
            messagebox.showerror("Error", "Failed to create account. Please try again.")

def open_create_account_window(xmpp_client):
    app = CreateAccountWindow(root, xmpp_client)
