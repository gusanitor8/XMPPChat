from model.client import Client
from view.chat_window import ChatWindow
import asyncio




if __name__ == "__main__":
    client = Client('gon21438-test4@alumchat.lol', '21438')
    client.connect(disable_starttls=True, use_ssl=False)
    client.process(forever=False)