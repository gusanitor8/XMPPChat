from slixmpp.roster import RosterItem
from view.chat_window import ChatWindow
from typing import Optional
from tkinter import messagebox
import asyncio
import slixmpp
import base64


class Client(slixmpp.ClientXMPP):
    _instance = None

    # We implement the singleton design pattern
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls)
        return cls._instance

    def __init__(self, jid, password):
        if not hasattr(self, '_initialized'):  # To ensure __init__ is not called multiple times
            super().__init__(jid=jid, password=password)
            self._initialized = True
            self.set_handlers()
            self._register_plugins()
            print("done")

    def _register_plugins(self):
        # Register plugins for file transfer
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0065')  # SOCKS5 Bytestreams
        self.register_plugin('xep_0095')  # Stream Initiation
        self.register_plugin('xep_0096')  # SI File Transfer
        self.register_plugin('xep_0004')

    async def start(self, event):
        self.send_presence(pshow="chat", pstatus="Connected")
        await self.get_roster()
        self.is_user_connected = True
        await asyncio.create_task(self.start_gui())

    async def start_gui(self):
        await self.send_dm()

    # Async function that sends a DM.
    async def send_dm(self):
        chat_win = ChatWindow(self)
        chat_win.run()
        await chat_win.get_input()

    def set_recv_msg(self, recv_msg: callable):
        self.recv_msg = recv_msg

    def send_msg(self, mto, msg):
        self.send_message(mto=mto, mbody=msg, mtype='chat')

    async def send_file(self, mto, file_path):
        # Splitting the file path to get the extension.
        file_name = file_path.split("/")[-1]

        file = open(file_path, "rb")
        file_data = file.read()

        # Sending the encoded file.
        file_encoded_data = base64.b64encode(file_data).decode()
        await self.send_message(mto=mto, mbody=f"file://{file_name}://{file_encoded_data}", mtype="chat")

    async def receive_message(self, message):
        if message["type"] == "chat":

            emitter = str(message["from"])
            actual_name = emitter.split("/")[0]
            message_body = message["body"]

            if (message_body.startswith("file://")):
                file_content = message["body"].split("://")
                file_name = file_content[1]
                file_data = file_content[2]
                decoded_file_data = base64.b64decode(file_data)
                file_to_write = open(f"../files_recv/{file_name}", "wb")
                file_to_write.write(decoded_file_data)

                # data for the message to be displayed
                msg_data = {
                    "emitter": actual_name,
                    "body": f"A file was sent by {actual_name}!"
                }

            else:
                msg_data = {
                    "emitter": actual_name,
                    "body": message_body
                }

            chat_window = ChatWindow(self)
            if not chat_window.is_running:
                chat_window.run()

            chat_window.receive_message(msg_data)

    def get_contacts(self):
        contacts = []
        for jid in self.client_roster:
            contacts.append(jid)
        return contacts

    def add_contact(self, jid: str, name: Optional[str] = None):
        self.send_presence_subscription(pto=jid)
        if name:
            self.update_roster(jid, name=name)

    def get_contact_details(self, jid: str) -> Optional[RosterItem]:
        if jid in self.client_roster:
            return self.client_roster[jid]
        return None

    def failed_auth(self):
        messagebox.showinfo("Alert", "Failed to Authenticate")
        self.disconnect()

    def set_handlers(self):
        # Message event handler.
        self.add_event_handler("message", self.receive_message)
        self.add_event_handler("failed_auth", self.failed_auth)
        self.add_event_handler("session_start", self.start)
