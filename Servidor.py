# coding=utf-8
import socket
from thread import *

import subprocess

# import psutil

nombreServidor = socket.gethostname()

# Obtener Nombre del Servidor
def ObtenerNombreServidor():
    return "\tEl nombre del servidor es: " + nombreServidor
    # print "Nombre del Servidor: %s" % nombreServidor

# Obtener la direccion IP del servidor
def ObtenerDireccionIPServidor():
    direccionIP = socket.gethostbyname(nombreServidor)
    return "\tLa direccion IP del servidor corresponde a: " + direccionIP

def ObtenerCantidadProcesos():
    count = len(psutil.pids())
    return "La cantidad de servicios en el servidor es: " + str(count)

""" EL primer argumento AF_INET es el dominio de la direccion del socket. ESto se usa cuando tenemos un dominio de
internet con dos hosts. El segundo argumento es el tipo socket. SOCK_STREAM siginifica que los datos caracteres se
leen en un flujo continuo
"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Configuramos el servidor para que pase datos en TCP.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = str(socket.gethostbyname(socket.gethostname())) #Sacamos la ip de la propia computadora.
Port = int(input("Digita el puerto a utilizar: "))

server.bind((IP_address, Port)) #Configuramos la IP y el puerto del servidor.
server.listen(10)           #Solo se permite 10 clientes conectado.

list_of_clients = []        #Se guardan los clientes que se conectan.
list_of_clients_in_chat = []#Se guardan los clientes que se conectan al chat.

nicks = {"admin": "admin"}

"""
-> El hilo que se ejecutara por cada cliente conectado al servidor.

:parameter conn ->La canexion del cliente
:parameter addr ->La direccion IPv4 del cliente. 
"""
def clientthread(conn, addr):
    conn.send("conectando...")
    while True:
        message = conn.recv(1)
        if message == "1":
            conn.send(ObtenerNombreServidor())
        elif message == "2":
            conn.send(ObtenerDireccionIPServidor())
        elif message == "3":
            print ("El cliente quiere la opcion 3")
            conn.send("...")
        elif message == "4":
            conn.send("...")
        elif message == "5":
            LivingRoomChat(conn)
        else:
            conn.send("\nOpcion invalida\n")


"""
-> El cuarto de chat, en esta función se corre un while true el cual esta esperando una respuesta del usuario para 
enviarla a los demas usuario en la lista de usuarios.

:parameter -> connChat, usuario que envio el mensaje.
"""
def LivingRoomChat(connChat):
    estoyEnChat = True
    list_of_clients_in_chat.append(connChat)
    broadcast("<" + addr[0] + " " + nicks[connChat] + " > Se conecto", connChat)
    connChat.send("\n\tBienvenido al chat {0}!!!\n".format(nicks[connChat]))
    while True:
        try:
            message = connChat.recv(2048)
            if message:
                if message == "salir":
                    print "<" + addr[0] + " " + nicks[connChat] + " > " + "Salio del chat"
                    message_to_send = "<" + nicks[connChat] + "> " + "Salio del chat"
                    broadcast(message_to_send, connChat)
                    estoyEnChat = False
                else:
                    print "<" + addr[0] + " " + nicks[connChat] + " > " + message
                    message_to_send = "<" + nicks[connChat] + "> " + message
                    broadcast(message_to_send, connChat)
            else:
                remove(connChat)

        except:
            pass
        if not estoyEnChat:
            removeClientOfChat(connChat)
            break
            return


def broadcast(message, connection):
    len(list_of_clients)
    for clients in list_of_clients_in_chat:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)
                removeClientOfChat(clients)


def removeClientOfChat(connection):
    if connection in list_of_clients:
        list_of_clients_in_chat.remove(connection)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept() # -> conexion y Ip del cliente.

    nick = conn.recv(2048) #-> EL nombre del cliente.

    list_of_clients.append(conn) #-> Metemos al cliente en la lista de clientes

    """Comprobamos que el nick no esta en nuestro diccionario de nicks para que no se repita """
    t = True
    for i in nicks:
        if nicks[i] == nick:
            t = True
        else:
            t = False
    # Si esta disponible lo annadimos
    if not t:
        nicks[conn] = nick
        # Enviamos una confirmacion al cliente
        conn.send("1")
    else:
        # Si no esta disponible le enviamos una denegacion al server y creamos un bucle hasta que este disponible
        while t:
            conn.send("0")
            nick = conn.recv(2048)
            if nicks[i] == nick:
                t = True
            else:
                t = False
                nicks[conn] = nick
                conn.send("1")

    print addr[0] + " " + nick + " se conecto"
    start_new_thread(clientthread, (conn, addr))  # Creamos un proceso individual para el cliente que se conecta

conn.close()
server.close()
