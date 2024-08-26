import tkinter as tk
from tkinter import ttk, messagebox
from model.AccountDeleter import Delete

class DeleteAccountWindow:
    def __init__(self):
        self.master = tk.Toplevel()
        self.master.title("Delete XMPP Account")
        self.master.geometry("300x200")

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

        # Delete Account button
        self.delete_button = tk.Button(self.master, text="Delete Account", command=self.delete_account)
        self.delete_button.pack(pady=(20, 0))


    def delete_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this account? This action cannot be undone.")
        if not confirm:
            return

        # We delete the account
        success = Delete(username, password)

        if success:
            messagebox.showinfo("Success", "Account deleted successfully!")
            self.master.destroy()
        else:
            messagebox.showerror("Error", "Failed to delete account. Please check your credentials and try again.")

def open_delete_account_window():
    app = DeleteAccountWindow()
