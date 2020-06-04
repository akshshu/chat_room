import socket
import sys
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import random
import subprocess
import argparse


def take_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip",
                        help="the number for which factorial has to be find")
    options = parser.parse_args()
    return options.ip


def exec_command(command):
    try:
        result = subprocess.check_output([command])
    except FileNotFoundError:
        result = bytes("Invalid Command Try again", 'utf-8')
    return result


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((input_ip, 8000))
    except ConnectionRefusedError:
        print("Server Not Accepting Connection ,Try again")
        exit()
    return client


def connection_setup(client):
    client.sendall(pubKeyPEM.encode('utf-8'))
    print("Enter an address to communicate")
    selected_net = input()
    client.send(selected_net.encode('utf-8'))
    partner_pub_key = client.recv(2048).decode('utf-8')
    if(partner_pub_key == "Key error"):
        print(
            "Provided CLient not connected to server,Try again after connecting to server")
        client.close()
        exit()
    return partner_pub_key


def handle_keys():
    keyPair = RSA.generate(1024)
    pubKey = keyPair.publickey()
    pubKeyPEM = pubKey.exportKey()
    with open("receiver.pem", "wb") as file_out:
        file_out.write(pubKeyPEM)
        file_out.close()
    pubKeyPEM = open("receiver.pem").read()
    return keyPair, pubKey, pubKeyPEM


def decryption_process(sck):
    global keyPair
    while True:
        from_server = sck.recv(8096)
        if not from_server:
            break
        else:
            sys.stdout.flush()
            decryptor = PKCS1_OAEP.new(keyPair)
            decrypted = decryptor.decrypt(from_server)
            first_word = (decrypted.decode('utf-8')).split()[0]
            if(first_word == "syscmd"):
                print("Command: ", end=" ")
                decrypted = bytes(decrypted.decode('utf-8')[7:], 'utf-8')
                print(decrypted.decode('utf-8'))
                decrypted = exec_command(
                    decrypted.decode('utf-8'))
                print('Command result:', decrypted.decode('utf-8'))
            else:
                print('Message:', decrypted.decode('utf-8'))
    sck.close()


def encryption_process(sess_pubKey, message):
    pubKey = RSA.import_key(sess_pubKey)
    encryptor = PKCS1_OAEP.new(pubKey)
    return encryptor.encrypt(message)


def send_mssage_to_server(sess_pubKey, message):

    message = bytes(message, 'utf-8')
    first_word = (message.decode('utf-8')).split()[0]
    if(first_word == "syscmd"):
        print("Command: ", end=" ")
        print(message.decode('utf-8')[7:])
    else:
        print("Message :", end=" ")
        print(message.decode('utf-8'))
    encrypted = encryption_process(sess_pubKey, message)
    # print("Encrypted:", binascii.hexlify(encrypted))
    client.sendall(encrypted)
    sys.stdout.flush()
    if message == "exit":
        client.close()


try:
    input_ip = take_input()
    keyPair, pubKey, pubKeyPEM = handle_keys()
    client = connect()
    partner_pub_key = connection_setup(client)
    t1 = threading.Thread(target=decryption_process, args=[client])
    t1.start()
    while True:
        inp = input()
        if(len(inp) > 0):
            send_mssage_to_server(partner_pub_key, inp)

    client.close()
except KeyboardInterrupt:
    print("\nCommunication interrupted ,Connection is closed")
    client.close()
    exit()
