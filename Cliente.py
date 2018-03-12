import socket
import sys

import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = raw_input("Digite el servidor a conectar: ")
Port = int(input("Digite el puerto del servidor: "))

server.connect((IP_address, Port))

nick = raw_input("Por favor introduce tu nick > ")
print("\n")

# Enviamos el nick al server
server.send(nick)
# Recibimos la confirmacion o denegacion del server
truck = server.recv(1)
# Mientras sea 0 es decir lo deniege entramos en el loop hasta que reciba 1 es decir lo acepte
while (truck == "0"):
    nick = raw_input("\nEse nick ya esta en uso, por favor introduce otro > ")
    server.send(nick)
    truck = server.recv(1)

while True:
    # Mantiene una lista de posible flujos de entrada
    sockets_list = [server]

    """Hay dos posible situaciones de entrada. O el usuario quiere dar una entrada manual para
    enviar a otras personas o el servidor esta enviando un mensaje para ser impreso en pantalla.
    Selecciona las devoluciones de sockets_list, la stream que es el lector para la entrada.
    Entonces, por ejemplo si el servidor quiere enviar un mensaje, entonces la condicion if
    se mantendra verdadera. Si el usuario desea enviar un mensaje, la condicion se evaluara como 
    verdadera """
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets + [sys.stdin]:
        if socks == server:
            message = socks.recv(2048)
            print message
        else:
            message = sys.stdin.readline()
            server.send(message)
            # Borramos la linea que escribimos por estetica
            CURSOR_UP = '\033[F'
            ERASE_LINE = '\033[K'
            print(CURSOR_UP + ERASE_LINE)
            print ("<Tu>")
            print (message)
server.close()