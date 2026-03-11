import socket
import threading
from config import HOST, PORT, BUFFER_SIZE

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass


def update_users():
    names = ",".join(nicknames)
    msg = f"USERS:{names}".encode("utf-8")
    broadcast(msg)


def handle(client):
    while True:
        try:
            message = client.recv(BUFFER_SIZE)

            if not message:
                raise Exception("Disconnected")

            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)

            nickname = nicknames[index]
            nicknames.remove(nickname)

            broadcast(f"SYSTEM:{nickname} left the chat".encode("utf-8"))
            update_users()

            client.close()
            break


def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        print("Connected with", address)

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(BUFFER_SIZE).decode("utf-8")

        if nickname in nicknames:
            client.send("SYSTEM:Nickname already taken".encode("utf-8"))
            client.close()
            continue

        nicknames.append(nickname)
        clients.append(client)

        print("Nickname:", nickname)

        broadcast(f"SYSTEM:{nickname} joined the chat".encode("utf-8"))
        update_users()

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
