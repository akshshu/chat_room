import socket
import sys
import threading
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.43.237", 8000))


def receive_message_from_server(sck, m):
    while True:
        from_server = sck.recv(4096)
        if not from_server:
            break
        else:
            sys.stdout.flush()

            print("\t\t\t\t"+from_server)

    sck.close()


def send_mssage_to_server():
    message = raw_input()
    client.send(message)
    sys.stdout.flush()
    if message == "exit":
        client.close()


threading._start_new_thread(receive_message_from_server, (client, "m"))

while True:
    send_mssage_to_server()
client.close()
