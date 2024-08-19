from typing import Optional

import asyncio
import slixmpp
from slixmpp import JID
from slixmpp.types import MessageTypes, OptJidStr
from slixmpp.roster import RosterItem
from view.signed_menu import ChatMenu
from view.chat_window import ChatWindow
from aioconsole import ainput


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

    async def start(self, event):
        self.send_presence(pshow="chat", pstatus="Connected")
        await self.get_roster()
        self.is_user_connected = True
        asyncio.create_task(self.start_gui())


    async def start_gui(self):
        self.send_msg('gon21438-test42@alumchat.lol', 'aver')
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

    async def receive_message(self, message):
        if message["type"] == "chat":
            emitter = str(message["from"])
            actual_name = emitter.split("/")[0]
            message_body = message["body"]

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
        self.disconnect()
        raise ValueError

    def set_handlers(self):
        # Message event handler.
        self.add_event_handler("message", self.receive_message)
        self.add_event_handler("failed_auth", self.failed_auth)
        self.add_event_handler("session_start", self.start)
