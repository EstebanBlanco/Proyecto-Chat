import socket
import sys
import select
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = str(socket.gethostbyname(socket.gethostname())) #raw_input("IPv4 a conectar: ")
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

estoyEnChat = False

"""
    Flujo de conexion con el servidor.
"""
while True:
    """
    message = server.recv(2048)
    print message
    message = raw_input(":::> ")
    if message == "5":
        lanzarChat(server)
    server.send(message)
    """
    if not estoyEnChat:
        imprimirMenu()

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

server.close()