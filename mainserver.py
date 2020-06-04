import socket
import threading
import random
import argparse

ip_keypair = {}


def take_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip",
                        help="the number for which factorial has to be find")
    options = parser.parse_args()
    return options.ip


def clientthread(conn, addr):
    pub_key = conn.recv(2048).decode('utf-8')
    ip_keypair.update({addr[0]: pub_key})
    associated_client = conn.recv(2048).decode('utf-8')
    try:
        conn.sendto(ip_keypair[associated_client].encode('utf-8'), addr)
    except KeyError:
        conn.send(("Key error").encode('utf-8'))
    while True:
        try:
            message = conn.recv(4096)
            if message:
                try:
                    for x in client_list:
                        if x.getpeername()[0] == associated_client:
                            x.sendall(message)
                            break
                except:
                    conn.close()
                    remove(conn)
            else:
                remove(conn)
        except:
            continue


def remove(connection):
    if connection in client_list:
        client_list.remove(connection)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    input_ip = take_input()
    # getting the IP address using socket.gethostbyname() method

    server.bind((input_ip, 8000))
except OSError:
    print("Couldn't Start Check Your connection and try again")
    exit()
server.listen(25)
client_list = []
addr_list = []
print("Waiting For Incoming Connection")
while True:
    conn, addr = server.accept()
    client_list.append(conn)
    addr_list.append(addr[0])
    print(addr[0]+"connected")
    threading._start_new_thread(clientthread, (conn, addr))
conn.close()
server.close()
