import xmpp


def register_new_user(jid, password):
    # Connecting to the server.
    xmpp_jid = xmpp.JID(jid)
    xmpp_account = xmpp.Client(xmpp_jid.getDomain(), debug=[])
    xmpp_account.connect()

    # Status to create the account.
    xmpp_status = xmpp.features.register(
        xmpp_account,
        xmpp_jid.getDomain(),
        {"username": xmpp_jid.getNode(), "password": password}
    )

    # Return the account's creation casted to boolean.
    return bool(xmpp_status)
