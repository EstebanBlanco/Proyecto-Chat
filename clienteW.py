#######################################################################
##                            LIBRERIAS                              ##
#######################################################################

from socket import *
import time
from thread import *

#######################################################################
##                            FUNCIONES                              ##
#######################################################################

def ini():
    host = raw_input("Direccion Servidor: ")
    port = int(input("Puerto: "))
    return host, port

def crearSocket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

def conectarse (host, port, s):
    s.connect((host, port))

def intentoConexion(host, port, s):

        while True:
            print("\nTrying to connect to:", host + ":" + str(port))
            try:
                conectarse(host, port, s)
                break
            except:
                print("There is no Server at:", host + ":" + str(port))
                print("Trying again in 5 Seconds\n")
                time.sleep(5)

def enviar(s):

    while True:

        global exit

        try:
            msg = input("")
            msg = client +": " + msg
            if msg == client+": salir":
                exit = True
                msg = "The "+client+" Client is gone"
                s.send(msg.encode("UTF-8"))
                s.close
                break
            else:
                s.send(msg.encode("UTF-8"))
                start_new_thread(recibir,(s,))


        except:
            print("Something happend\n")
            print("Trying in 5 seg")
            time.sleep(5)

def recibir(s):
    while True:

        try:
          reply = s.recv(2048)
          print(reply.decode("UTF-8"))
          break


        except:
            print("Cant recieve response\n")
            print("Trying in 5 seg")
            time.sleep(5)

def recibirEspecial(s):
    global client
    client = s.recv(2048).decode("UTF-8")

#######################################################################
##                          VARIABLES GLOBALES                       ##
#######################################################################

exit=False      # Si el cliente envia salir, exit se pone en true y el
                # el programa termina
client = ""

#######################################################################
##                                MAIN                               ##
#######################################################################

def main():

    host, port = ini()
    s = crearSocket()
    intentoConexion(host,port,s)
    recibirEspecial(s)
    print("\nConnection To Server Established!\nThe server is:", host+":"+str(port)+"\n")
    print("Write your messages\n")
    start_new_thread(enviar,(s,))

    while exit!=True:   # Necesarios para que los hilos no mueran
        pass

    print("\nSorry something went wrong! You have lost connection to the server.:(")
    print("Closing the windows in 5 seg")
    time.sleep(10)

main()