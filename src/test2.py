import slixmpp
from slixmpp.exceptions import IqError, IqTimeout


class MUCClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        # Register plugins
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0045')  # Multi-User Chat (MUC)
        self.register_plugin('xep_0059')

        # Event handlers
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        try:
            # Discover MUC rooms on the server
            muc_server = 'conference.alumchat.lol'  # Replace with your MUC server
            muc_rooms = await self.plugin['xep_0030'].get_items(jid=muc_server, iterator=True)

            print(f"Rooms discovered on {muc_server}:")
            for room in muc_rooms['disco_items']:
                room_jid = room['jid']
                room_name = room['name']
                print(f"Room JID: {room_jid}, Name: {room_name}")


        except IqError as e:
            print(f"Error discovering MUC rooms: {e.iq['error']['text']}")
        except IqTimeout:
            print("No response from server.")
        finally:
            self.disconnect()

if __name__ == '__main__':
    jid = 'gon21438-test4@alumchat.lol'  # Replace with your JID
    password = '21438'   # Replace with your password

    xmpp = MUCClient(jid, password)
    xmpp.connect(disable_starttls=True, use_ssl=False)
    xmpp.process(forever=False, timeout=10)


