import socket
from threading import Thread
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '127.0.0.1'
port=8000
server.bind((ip_address, port))
server.listen()
list_of_clients = []
nicknames = []
print("server has started")

def clientThread(conn,nickname):
    conn.send("Welcome to the chat room".encode("utf-8"))
    while True:
        try:
            message=conn.recv(2048).decode("utf-8")
            if message:
                print(message)
                broadCast(message,conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

def broadCast(message,connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message.encode("utf-8"))
            except:
                remove(client)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn,addr=server.accept()
    conn.send("NICKNAME".encode("utf-8"))
    nickname=conn.recv(2048).decode("utf-8")
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message = "{} joined!".format(nickname)
    print(message)
    broadCast(message, conn)
    new_thread = Thread(target=clientThread,args=(conn, nickname))
    new_thread.start()