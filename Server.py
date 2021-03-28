import os
from socket import *
from threading import Thread

clients = {}
addresses = {}
HOST = ''
PORT = 6000

SERVER_ADRESS = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(SERVER_ADRESS)

def accept():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to the CHAT --->type your name and pres enter", "utf8"))
        addresses[client] = client_address
        Thread(target=handle,args=(client,)).start()

def handle(client):
    name = client.recv(1024).decode("utf8")
    welcome = 'Welcome %s!, type "-quit" to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast_to_all_clients(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(1024)
        if msg == bytes("-quit", "utf8"):
            client.send(bytes("-quit", "utf8"))
            client.close()
            del clients[client]
            broadcast_to_all_clients(bytes("%s has left the chat." % name, "utf8"))
            break

        elif msg==bytes("-download","utf8"):
            send_file(client)
        elif msg==bytes("fdatx","utf8"):
            #msg=client.recv(1024)
            print(msg.decode("utf8"))
            received_file(client)
        elif msg==bytes("-cancel","utf8"):
            cancel_uplodad()

        else:
            broadcast_to_all_clients(msg, name + ": ")

def cancel_uplodad():
    os.remove("file_received")

def received_file(client):
    f = open("file_received", "wb")
    ff=str(f).split(".",2)
    data=client.recv(1024)
    while True:
        if data[-8:]!=bytes("ast_data","utf8"):
            print("server downloading the file")
            f.write(data)
            data = client.recv(1024)
        else:
            f.write(data[:-9])
            print()
            break
    f.close()
    print("[+] Download complete!")

def broadcast_to_all_clients(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

def send_file(client):
        f=  open("file_received", "rb")
        client.send(bytes("fdatx", "utf8"))
        while True:
            data = f.read(1024)
            client.send(data)
            if not data:
                break
        client.send(bytes("last_data", "utf8"))
        f.close()


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()