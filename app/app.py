import socket
import time
import hashlib
import sys

ipMaquinaServidor = "13.92.208.121"
archivo = 'archivo.png'
cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

h = hashlib.sha256()

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
        cs.settimeout(1)
        try:
            data = cs.recv(1024)
            h.update(data)
            fw.write(data)
            if not data:
                t2 = time.time()*1000
                cs.send(b"hash")
                break
        except Exception as e:
            t2 = time.time()*1000
            cs.send(b"hash")
            break
    fw.close()
print("Hash obtenido del archivo recibido",h.digest())
hrecibido = cs.recv(1024)
print("Hash recibido desde el servidor:  ",hrecibido)
if(hrecibido == h.digest()):
    cs.send(b"Recibido")
    print("Recibido correctamente, el archivo esta completo y el Hash concuerda")
else:
    cs.send(b"noIntegridad")
    print("La integridad se vio comprometida debido a que el Hash no concuerda")

cs.shutdown(socket.SHUT_WR)
cs.close()
tiempoTransferencia= t2-t1
print(tiempoTransferencia)
try:
    sys.exit(0)
except:
    print("Se apaga el cliente")

