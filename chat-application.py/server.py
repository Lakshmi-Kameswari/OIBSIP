import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

print("=" * 50)
print("  🚀 Chat Server Started")
print(f"  Listening on {HOST}:{PORT}")
print("=" * 50)


def broadcast(message, sender_client=None):
    """Send a message to all connected clients."""
    for client in clients:
        try:
            client.send(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)


def handle(client):
    """Handle messages from a connected client."""
    while True:
        try:
            message = client.recv(2048)
            if message:
                broadcast(message, client)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {message.decode('utf-8')}")
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                nicknames.remove(nickname)
                leave_msg = f"SYSTEM:{nickname} has left the chat."
                broadcast(leave_msg.encode("utf-8"))
                print(f"[-] {nickname} disconnected.")
            break


def receive():
    """Accept incoming client connections."""
    while True:
        client, address = server.accept()
        print(f"[+] New connection from {address}")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        nicknames.append(nickname)
        clients.append(client)

        print(f"[+] Nickname registered: {nickname}")

        # Notify everyone
        join_msg = f"SYSTEM:{nickname} has joined the chat! 👋"
        broadcast(join_msg.encode("utf-8"))

        # Send online user list to the new client
        user_list = ",".join(nicknames)
        client.send(f"USERS:{user_list}".encode("utf-8"))

        # Start handling thread
        thread = threading.Thread(target=handle, args=(client,))
        thread.daemon = True
        thread.start()


receive()
