import slixmpp
from slixmpp.xmlstream.stanzabase import ET


class Delete(slixmpp.ClientXMPP):

    # Constructor method.
    def __init__(self, jid, password):
        super().__init__(jid=jid, password=password)
        self.user_to_delete = jid
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        await self.delete_account()
        self.disconnect()

    async def delete_account(self):
        # Response from the server.
        response = self.Iq()
        response["from"] = self.boundjid.user
        response["type"] = "set"

        # Stanza to delete the account.
        fragment = ET.fromstring(
            "<query xmlns='jabber:iq:register'><remove/></query>"
        )

        # Appending the stanza to delete the account.
        response.append(fragment)

        # Account has been deleted succesfully.
        await response.send()
        deleted_user = self.boundjid.jid.split("/")[0]
        return True
