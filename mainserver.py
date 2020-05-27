import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("192.168.43.237", 8000))
server.listen(100)
client_list = []


def clientthread(conn, addr):
    print("Welcome to the chatroom")
    while True:
        try:
            message = conn.recv(2048)
            if message:
                print(addr[0]+message)
                message_to_send = addr[0]+message
                msg_send(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue


def msg_send(msg, connection):
    for client in client_list:
        if client != connection:
            try:
                client.send(msg)
            except:
                client.close()
                remove(client)


def remove(connection):
    if connection in client_list:
        client_list.remove(connection)


while True:
    conn, addr = server.accept()
    client_list.append(conn)
    print(addr[0]+"connected")
    threading._start_new_thread(clientthread, (conn, addr))
conn.close()
server.close()
