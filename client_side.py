#Client Side Chat room

import socket
import threading

nickname = input('Enter a nickname : ')

#Define constants to be used
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 12345
ENCODER = 'ascii'
BYTESIZE = 1024

#Create a client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((DEST_IP, DEST_PORT))

def write():
    '''Send a message to the server to be broadcast'''
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode(ENCODER))

def receive():
    '''Receive an incoming message from the server'''
    while True:
        try:
            message = client.recv(1024).decode(ENCODER)
            if message == 'NICK':
                client.send(nickname.encode(ENCODER))                
            else:
                print(message)

        except:
            print('ERROR occured!!')
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()