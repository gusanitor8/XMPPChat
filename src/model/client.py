from slixmpp.roster import RosterItem
from view.chat_window import ChatWindow
from model.services import MUC_SERVICE, AV_STATES
from slixmpp.exceptions import IqError, IqTimeout
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
            self.chat_window = None
            self._initialized = True
            self.set_handlers()
            self._register_plugins()
            print("done")

    def set_chat_window(self, chat_window):
        self.chat_window = chat_window

    def _register_plugins(self):
        # Register plugins for file transfer
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0045')

    async def start(self, event):
        self.send_presence(pshow="chat", pstatus="Connected")
        await self.get_roster()
        self.is_user_connected = True
        await asyncio.create_task(self.start_gui())

    def add_contact(self, jid):
        """Send a contact request (presence subscription) to the specified JID."""
        try:
            self.send_presence(ptype='subscribe', pto=jid)
            messagebox.showinfo("Alert", "Contact added succesfully")
        except Exception as e:
            messagebox.showinfo("Alert", "Could not add contact")
            print(e)

    async def start_gui(self):
        await self.send_dm()

    async def create_group(self, group_name: str):
        try:
            # Join the room (this will create it if it doesn't exist)
            await self.plugin["xep_0045"].join_muc(group_name, self.boundjid.user)

            # Get the room configuration form
            config_form = await self.plugin["xep_0045"].get_room_config(group_name)

            # Update the configuration
            config_form["muc#roomconfig_roomname"] = group_name
            config_form["muc#roomconfig_persistentroom"] = True
            config_form["muc#roomconfig_publicroom"] = True
            config_form["muc#roomconfig_membersonly"] = False
            config_form["muc#roomconfig_allowinvites"] = True
            config_form["muc#roomconfig_enablelogging"] = True
            config_form["muc#roomconfig_changesubject"] = True
            config_form["muc#roomconfig_maxusers"] = "64"
            config_form["muc#roomconfig_whois"] = "anyone"
            config_form["muc#roomconfig_roomdesc"] = "Group created from Gustavo's chat."
            config_form["muc#roomconfig_roomowners"] = [self.boundjid.bare]

            # Explicitly unlock the room
            config_form["muc#roomconfig_passwordprotectedroom"] = False
            config_form["muc#roomconfig_roomsecret"] = ""

            # Apply the configuration
            await self.plugin["xep_0045"].set_room_config(group_name, config=config_form)

            print(f"Group {group_name} has been created and configured.")
            messagebox.showinfo("Alert", f"Group {group_name} has been created and configured.")

        except IqError as e:
            print(f"Error creating group: {e.iq['error']['condition']}")
            messagebox.showinfo("Alert", "Error creating group")
        except IqTimeout:
            messagebox.showinfo("Alert", "Timeout while creating group")

    async def join_group(self, group_name):
        # Method to join the group.
        try:
            await self.plugin["xep_0045"].join_muc(room=group_name, nick=self.boundjid.user)
            messagebox.showinfo("Alert", "Group Joined Successfully")
        except Exception as e:
            messagebox.showinfo("Alert", "Couldn't join group")

    async def get_joined_groups(self):
        try:
            # Get the list of joined rooms
            iq = self.Iq()
            iq['type'] = 'get'
            iq['to'] = 'conference.alumchat.lol'  # Use the MUC service domain
            iq['disco_items']

            result = await iq.send(timeout=10)  # Use a timeout to prevent hanging

            rooms = result['disco_items']['items']

            # Now, let's get the rooms the user is actually in
            joined_rooms = self.plugin['xep_0045'].get_joined_rooms()

            return list(joined_rooms)

        except (IqError, IqTimeout) as e:
            print(f"Error retrieving joined groups: {e}")
            return []

    async def get_all_groups(self):
        try:
            # Get the list of joined rooms
            iq = self.Iq()
            iq['type'] = 'get'
            iq['to'] = 'conference.alumchat.lol'  # Use the MUC service domain
            iq['disco_items']

            result = await iq.send(timeout=10)  # Use a timeout to prevent hanging

            rooms = result['disco_items']['items']
            return [room[0] for room in rooms]


        except (IqError, IqTimeout) as e:
            print(f"Error retrieving joined groups: {e}")
            return []

    # Async function that sends a DM.
    async def send_dm(self):
        chat_win = ChatWindow(self)
        chat_win.run()
        await chat_win.get_input()

    def set_recv_msg(self, recv_msg: callable):
        self.recv_msg = recv_msg

    def send_msg(self, mto: str, msg):
        if mto.endswith(MUC_SERVICE):
            self.send_message(mto=mto, mbody=msg, mtype='groupchat')
            return

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

    def get_contact_details(self, jid: str) -> Optional[RosterItem]:
        if jid in self.client_roster:
            return self.client_roster[jid]
        return None

    def failed_auth(self):
        messagebox.showinfo("Alert", "Failed to Authenticate")
        self.disconnect()

    def on_roster_update(self, event):
        if self.chat_window:
            self.chat_window.update_dropdown()

    def update_presence(self, show, status):
        if show in AV_STATES:
            self.send_presence(pshow=show, pstatus=status)
            messagebox.showinfo("Alert", "Presence and status where changed")

    def set_handlers(self):
        # Message event handler.
        self.add_event_handler("message", self.receive_message)
        self.add_event_handler("failed_auth", self.failed_auth)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("roster_update", self.on_roster_update)
