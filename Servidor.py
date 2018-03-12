import socket
from thread import *

import subprocess

nombreServidor = socket.gethostname()
# Obtener Nombre del Servidor
def ObtenerNombreServidor():
    return "\tEl nombre del servidor es: " + nombreServidor
    #print "Nombre del Servidor: %s" % nombreServidor

# Obtener la direccion IP del servidor
def ObtenerDireccionIPServidor():
    direccionIP = socket.gethostbyname(nombreServidor)
    print "\tDireccion IP: %s" % direccionIP
    return "\tLa direccion IP del servidor corresponde a: "+ direccionIP
    #print "Direccion IP: %s" % direccionIP

def ObtenerCantidadProcesos():
    procs = subprocess.check_output(['ps', '-a', '-c', '-ocomm=']).splitlines()
    count = procs.count('kms')
    return "\tLa cantidad de servicios en el servidor es: "+ str(count)


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
    # Le enviamos un mensaje al nuevo cliente conectado
    conn.send("Bienvenido al chat {0}!!!".format(nicks[conn]))

    while True:
        try:
            message = conn.recv(2048)
            if message:
                # Imprime direccion y mensaje del usuario
                print "<" + addr[0] + " " + nicks[conn] + " > " + message
                message_to_send = "<" + nicks[conn] + "> " + message
                broadcast(message_to_send, conn)
            else:
                """El mensaje puede no tener contenido si la conexion
                esta rota, en este caso eliminamos la conexion """
                # La funcion remove la escribire ahora
                remove(conn)
        except:
            continue


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
            # Si el enlace esta roto eliminamos el cliente
            remove(clients)


"""La siguiente funcion simplemente elimina el objeto de la lista que se creara al comienzo, ahora 
escribire esa parte """


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
    # Ahora imrimos la direccion y el nick del usuario que se acaba de conectar
    print addr[0] + " " + nick + " conectado"
    conn.send("--> Bienvenido al Servidor de Chat!!!")

    #Hacemos un bucle en las opciones primarias del cliente.
    while True:
        conn.send("\nMenu Servidor Chat\n"
                  "1: Obtener nombre\n"
                  "2: IPv4 del servidor\n"
                  "3: Cantidad de procesos\n"
                  "4: Consultar la hora\n"
                  "5: Entrar al chat")

        message = conn.recv(1)
        if message == "1":
            conn.send(ObtenerNombreServidor())
        elif message == "2":
            conn.send(ObtenerDireccionIPServidor())
        elif message == "3":
            print ("El cliente quiere la opcion 3")
        elif message == "4":
            print ("El cliente quiere la opcion 4")
        else:
            start_new_thread(clientthread, (conn, addr))  # Creamos un proceso individual para el cliente que se conecta

conn.close()
server.close()