#Server side Chat room

import socket
import threading
from datetime import datetime


#Define constants to be used
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
ENCODER = 'ascii'
BYTESIZE = 1024

#Create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST_IP, HOST_PORT))
server.listen()

#Create two black list to store connected socket and there names.
clients = []
nicknames = []

def broadcast(message):
    '''Send a message to al the clients connected to the server'''
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
            print(message.decode(ENCODER))

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            file = open("history.txt", "a")
            file.write(f'{current_time}==>  {message.decode(ENCODER)}\n')
            file.close()

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!!'.encode(ENCODER))
            nicknames.remove(nickname)
            break

def receive():
    '''Receive an incoming message from a specific client and forward to be broadcasted'''
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode(ENCODER))
        nickname = client.recv(1024).decode(ENCODER)
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!!'.encode(ENCODER))
        client.send('Connected to the server....'.encode(ENCODER))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listning....')
receive()
