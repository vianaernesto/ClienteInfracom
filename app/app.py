import socket
import time
import hashlib
import sys

ipMaquinaServidor = "13.92.208.121"
archivo = 'archivo.png'
cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("Cliente iniciado")
##Para probar localmente cambiar "ipMaquinaServidor" por socket.gethostname()
cs.connect((socket.gethostname(),5000))
print("Cliente conectandose")
cs.send(b"syn")
ack = cs.recv(1024)
if(ack == b"ack"):
    print("Cliente Conectado")
    cs.send(b"Preparado")
else:
    print("Cliente no se pudo conectar")
    cs.close()

t1 = time.time()*1000
print("Recibiendo..")
with open(archivo, 'wb') as fw:
    while True:
        ##Esto es para que no sea bloqueante
        cs.settimeout(0.1)
        try:
            data = cs.recv(1024)
            fw.write(data)
            if not data:
                t2 = time.time()*1000
                break
        except Exception as e:
            t2 = time.time()*1000
            break
    fw.close()
cs.send(b"Recibido")
print("Recibido")


cs.shutdown(socket.SHUT_WR)
cs.close()
tiempoTransferencia= t2-t1
print(tiempoTransferencia)
sys.exit(0)
