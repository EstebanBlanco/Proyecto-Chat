import socket
import sys
import select
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = raw_input("IPv4 a conectar: ") #str(socket.gethostbyname(socket.gethostname()))
Port = int(input("Puerto: "))
server.connect((IP_address, Port))

"""
Entrada del nick al servidor.
"""
nick = raw_input("Por favor introduce tu nick > ")
server.send(nick)
truck = server.recv(1)

while truck == "0":
    nick = raw_input("\nEse nick ya esta en uso, por favor introduce otro > ")
    server.send(nick)
    truck = server.recv(1)

def imprimirMenu():
    print("\n--> Bienvenido al Servidor de Chat!!!\n"
    "### Menu Servidor Chat ###\n"
    "1: Obtener nombre\n"
    "2: IPv4 del servidor\n"
    "3: Cantidad de procesos\n"
    "4: Consultar la hora\n"
    "5: Entrar al chat\n")

def hiloEscucha(conn, addr):
    while True:
        sockets_list = [conn]
        read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
        if read_sockets[0] == conn:
            message = read_sockets[0].recv(2048)
            print message

def hiloEscribe(conn, addr):
    estoyEnChat = False
    while True:
        if not estoyEnChat:
            imprimirMenu()
            message = raw_input(":::> ")
        else:
            message = raw_input()

        server.send(message)
        if message == "4":
            message = raw_input(":::> ")
            server.send(message)
        elif message == "5":
            estoyEnChat = True
        elif message == "salir":
            estoyEnChat = False


start_new_thread(hiloEscucha, (server, "listening"))

start_new_thread(hiloEscribe, (server, "writing"))

estoyEnChat = False

"""
    Flujo de conexion con el servidor.
"""
while True:
    """
    if not estoyEnChat:
        imprimirMenu()
<<<<<<< HEAD
=======

>>>>>>> e4949916c4b52657e86d6f73d36fb3333d058a68
    sockets_list = [server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets + [sys.stdin]:
        if socks == server:
            message = socks.recv(2048)
            print message
        else:
            message = raw_input(":::> ")
            server.send(message)
            print("<Tu> " + str(message))
            if message == "5":
                estoyEnChat = True
            elif message == "salir":
                estoyEnChat = False
    """

server.close()