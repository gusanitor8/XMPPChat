import xmpp


def register_new_user(jid, password):
    """
    This function registers a new user for us
    :param jid: the user we want to create with the domain of the server included
    :param password: the password for the jid
    :return:
    """
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
