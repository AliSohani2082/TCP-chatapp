import threading
import socket

host = "127.0.0.1"  # local host
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        if nickname == 'admin':
            client.send("PASS".encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != 'adminpass':
                client.send("REFUSE".encode("ascii"))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('ascii'))
        client.send("Connected to server!".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
