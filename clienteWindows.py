import socket

# Creamos un objeto socket para el servidor. Podemos dejarlo sin parametros pero si
# quieren pueden pasarlos de la manera server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IPv4 = raw_input("IPv4 del servidor > ")
Port = int(input("Puerto > "))
s.connect((IPv4, Port))

nick = raw_input("Por favor introduce tu nick > ")
print("\n")

# Enviamos el nick al server

s.send(nick)

# Recibimos la confirmacion o denegacion del server

truck = s.recv(1)

# Mientras sea 0 es decir lo deniege entramos en el loop hasta que reciba 1 es decir lo acepte

while (truck == "0"):
    nick = raw_input("\nEse nick ya esta en uso, por favor introduce otro > ")
    s.send(nick)
    truck = s.recv(1)
print(s.recv(2048))

# Creamos un bucle para retener la conexion
while True:
    # Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
    mensaje = raw_input("Mensaje: ")

    # Con la instancia del objeto servidor (s) y el metodo send, enviamos el mensaje introducido
    s.send(mensaje)
    print("1")
    print(s.recv(2048))
    print("2")

    # Si por alguna razon el mensaje es close cerramos la conexion
    if mensaje == "close":
        break

# Imprimimos la palabra Adios para cuando se cierre la conexion
print "Adios."

# Cerramos la instancia del objeto servidor
s.close()