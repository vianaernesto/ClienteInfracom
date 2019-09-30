import socket
import time
import hashlib
import sys

ipMaquinaServidor = "23.96.54.150"
archivo = 'archivo.mkv'
cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

h = hashlib.sha256()

print("Cliente iniciado")
##Para probar localmente cambiar "ipMaquinaServidor" por socket.gethostname()
cs.connect(ipMaquinaServidor,5000))
print("Cliente conectandose")
cs.send(b"syn")
ack = cs.recv(2048)
if(ack == b"ack"):
    print("Cliente Conectado")
    cs.send(b"Preparado")
else:
    print("Cliente no se pudo conectar")
    cs.close()

print("Recibiendo..")
with open(archivo, 'wb') as fw:
    while True:
        ##Esto es para que no sea bloqueante
        cs.settimeout(1)
        t1 = time.time()*1000
        try:
            data = cs.recv(2048)
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
hrecibido = cs.recv(2048)
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

