import slixmpp
from slixmpp.exceptions import IqError, IqTimeout


class DiscoClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)

        # Load the XEP-0030 plugin for service discovery
        self.register_plugin('xep_0030')

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        try:
            # Discover information about the server
            info = await self['xep_0030'].get_info(jid=self.boundjid.domain)
            print(f"Server Identity: {info['disco_info']['identities']}")
            print(f"Server Features: {info['disco_info']['features']}")

            # Optionally, you can also discover available items (e.g., services)
            items = await self['xep_0030'].get_items(jid=self.boundjid.domain)
            print("Items discovered on server:")
            for item in items['disco_items']['items']:
                print(f" - {item['name']}: {item['jid']}")

        except IqError as e:
            print(f"Error fetching service discovery info: {e.iq['error']['text']}")
        except IqTimeout:
            print("No response from server.")
        finally:
            self.disconnect()


if __name__ == '__main__':
    # Replace with your actual JID and password
    jid = 'gon21438-test4@alumchat.lol'
    password = '21438'

    xmpp = DiscoClient(jid, password)
    xmpp.connect(disable_starttls=True, use_ssl=False)
    xmpp.process(forever=False, timeout=10)
