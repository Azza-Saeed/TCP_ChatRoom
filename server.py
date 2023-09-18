import socket
import threading


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#  set up an IP and port number to the socket
ip = socket.gethostname()
# print(ip)
port = 1234

arr =(ip, port)
# Bind the IP and the port to the socket object 's'
server.bind(arr)
server.listen(3)

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)

def handel(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client.index(client)
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

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joind the chat".encode('ascii'))
        client.send("Connected to the server".encode('ascii'))

        thread = threading.Thread(target=handel, args=(client,))
        thread.start()


print("server is listening....")
receive()
