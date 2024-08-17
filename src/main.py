from src.model.client import Client
from view.chat_window import ChatWindow
from view.main_view import XMPPChatInterface


def main():
    gui = XMPPChatInterface()
    gui.run()


if __name__ == "__main__":
    main()
