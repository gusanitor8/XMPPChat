from model.client import Client
from view.chat_window import ChatWindow
from view.signed_menu import ChatMenu
import asyncio


def main():
    client = Client('gon21438-test4@alumchat.lol', '21438')
    chat_menu = ChatWindow(client)
    chat_menu.run()
    client.connect(disable_starttls=True, use_ssl=False)
    client.process(forever=False)

if __name__ == "__main__":
    main()