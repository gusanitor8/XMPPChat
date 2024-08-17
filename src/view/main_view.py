import tkinter as tk
from view.sign_in import LoginForm


class XMPPChatInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("XMPP Chat Interface")
        self.initialize_items()

    def run(self):
        # Run the application
        self.root.mainloop()

    def sign_up(self):
        pass

    def sign_in(self):
        login_form = LoginForm()
        login_form.run()

    def close_chat(self):
        print("Close XMPP Chat.")

    def delete_account(self):
        print("Delete account on XMPP Chat.")

    def initialize_items(self):
        # Create buttons
        btn_sign_up = tk.Button(self.root, text="Sign up to XMPP Chat", command=self.sign_up)
        btn_sign_in = tk.Button(self.root, text="Sign in to XMPP Chat", command=self.sign_in)
        btn_close_chat = tk.Button(self.root, text="Close XMPP Chat", command=self.close_chat)
        btn_delete_account = tk.Button(self.root, text="Delete account on XMPP Chat", command=self.delete_account)

        # Arrange buttons on the window
        btn_sign_up.pack(pady=10)
        btn_sign_in.pack(pady=10)
        btn_close_chat.pack(pady=10)
        btn_delete_account.pack(pady=10)
