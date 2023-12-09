import threading
import TelegramBot.server as server
import detection.controller as client


if __name__ == "__main__":
    server_thread = threading.Thread(target=server.run)
    client_thread = threading.Thread(target=client.run)

    server_thread.start()
    client_thread.start()

    server_thread.join()
    client_thread.join()
