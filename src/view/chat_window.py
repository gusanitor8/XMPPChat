import tkinter as tk


class ChatWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title = "XMPP Chat Window"
        self.chat_display = None
        self.message_entry = None
        self.initialize_items()

    def run(self):
        # Run the application
        self.root.mainloop()

    def receive_message(self):
        message = self.get_entry()
        if message:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, "You: " + message + "\n")
            self.chat_display.config(state=tk.DISABLED)
            self.message_entry.delete(0, tk.END)

    def send_message(self):
        message = self.get_entry()
        if message:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, message + "\n", "right_align")
            self.chat_display.config(state=tk.DISABLED)

            # Configure the tag for right alignment
            self.chat_display.tag_configure("right_align", justify='right')

    def get_entry(self) -> str:
        return self.message_entry.get()

    def initialize_items(self):
        # Create the main window
        self.root.geometry("400x500")  # Set the fixed size of the window
        self.root.resizable(False, False)  # Disable resizing

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
        send_button = tk.Button(bottom_frame, text="Send", command=self.receive_message)
        send_button.pack(side=tk.RIGHT)
