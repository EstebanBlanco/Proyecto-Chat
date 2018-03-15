# coding=utf-8
import socket
from thread import *

import subprocess

#import psutil

nombreServidor = socket.gethostname()
# Obtener Nombre del Servidor
def ObtenerNombreServidor():
    return "\tEl nombre del servidor es: " + nombreServidor
    #print "Nombre del Servidor: %s" % nombreServidor

# Obtener la direccion IP del servidor
def ObtenerDireccionIPServidor():
    direccionIP = socket.gethostbyname(nombreServidor)
    return "\tLa direccion IP del servidor corresponde a: "+ direccionIP


def ObtenerCantidadProcesos():
    count = len(psutil.pids())
    return "La cantidad de servicios en el servidor es: "+ str(count)


""" EL primer argumento AF_INET es el dominio de la direccion del socket. ESto se usa cuando tenemos un dominio de
internet con dos hosts. El segundo argumento es el tipo socket. SOCK_STREAM siginifica que los datos caracteres se
leen en un flujo continuo
"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

nombre_equipo = socket.gethostname()

IP_address = str(socket.gethostbyname(nombre_equipo))
Port = int(input("Digita el puerto a utilizar: "))

"""Vinculamos el server a una ip y a un puerto que deben ser los mismos que el del cliente """
server.bind((IP_address, Port))

"""Escuchamos 10 conexiones activas"""
server.listen(10)

# Aqui guardaremos los clientes que se conecten
list_of_clients = []

# Y aqui sus nicks, pongo admin para que no pueda usarse
nicks = {"admin": "admin"}

def clientthread(conn, addr):
    """conn.send("\n--> Bienvenido al Servidor de Chat!!!\n"
              "### Menu Servidor Chat ###\n"
              "1: Obtener nombre\n"
              "2: IPv4 del servidor\n"
              "3: Cantidad de procesos\n"
              "4: Consultar la hora\n"
              "5: Entrar al chat\n")
    """
    conn.send("conectando...")
    while True:
        """conn.send("\n--> Bienvenido al Servidor de Chat!!!\n"
                  "### Menu Servidor Chat ###\n"
                  "1: Obtener nombre\n"
                  "2: IPv4 del servidor\n"
                  "3: Cantidad de procesos\n"
                  "4: Consultar la hora\n"
                  "5: Entrar al chat\n")"""
        message = conn.recv(1)
        if message == "1":
            conn.send(ObtenerNombreServidor())
        elif message == "2":
            conn.send(ObtenerDireccionIPServidor())
        elif message == "3":
            print ("El cliente quiere la opcion 3")
        elif message == "4":
            print ("El cliente quiere la opcion 4")
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
    connChat.send("\n\tBienvenido al chat {0}!!!\n".format(nicks[connChat]))
    while True:
        try:
            message = connChat.recv(2048)
            if message:
                print "<" + addr[0] + " " + nicks[connChat] + " > " + message
                message_to_send = "<" + nicks[connChat] + "> " + message
                broadcast(message_to_send, connChat)
            else:
                remove(connChat)
        except:
            pass

def broadcast(message, connection):
    len(list_of_clients)
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    """Acepta una solicitud de conexion y almacena dos parametros, conn que un objeto socket
    y addr que contiene la direccion IP del cliente """
    conn, addr = server.accept()

    # El primer mensaje que recibamos sera el nick, lo veremos en el cliente cuando termine el server
    nick = conn.recv(2048)

    """Metemos al cliente en la lista de clientes """
    list_of_clients.append(conn)

    """Comprobamos que el nick no esta en nuestro diccionario de nicks para que no se repita """
    t = True
    for i in nicks:
        if nicks[i] == nick:
            t = True
        else:
            t = False
    # Si esta disponible lo annadimos
    if t == False:
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