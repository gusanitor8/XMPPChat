from typing import Optional
import slixmpp
from slixmpp import JID
from slixmpp.types import MessageTypes, OptJidStr
from slixmpp.roster import RosterItem


class Client(slixmpp.ClientXMPP):
    _instance = None

    # We implement the singleton design pattern
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, jid, password, recv_msg: callable):
        if not hasattr(self, '_initialized'):  # To ensure __init__ is not called multiple times
            super().__init__(jid=jid, password=password)
            self.recv_msg = recv_msg
            self._initialized = True

    def send_message(self, mto: JID, mbody: Optional[str] = None,
                     msubject: Optional[str] = None,
                     mtype: Optional[MessageTypes] = None,
                     mhtml: Optional[str] = None, mfrom: OptJidStr = None,
                     mnick: Optional[str] = None):
        pass

    async def receive_message(self, message):
        if message["type"] == "chat":
            emitter = str(message["from"])
            actual_name = emitter.split("/")[0]
            message_body = message["body"]

            msg_data = {
                "emitter": actual_name,
                "body": message_body
            }

            self.recv_msg(msg_data)

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

    def set_handlers(self):
        # Message event handler.
        self.add_event_handler("message", self.receive_message)
