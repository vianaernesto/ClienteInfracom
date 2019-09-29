import socket
import time

ipMaquinaServidor = "13.92.208.121"

cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
##Para probar localmente cambiar "ipMaquinaServidor" por socket.gethostname()
cs.connect((ipMaquinaServidor,5000))

archivo = 'archivo.png'

cs.send(b"archivo2")
t1 = time.time()*1000



print("Recibiendo..")
with open(archivo, 'wb') as fw:
    while True:
        data = cs.recv(1024)
        if not data:
            break
        fw.write(data)
    fw.close()
    t2 = time.time()*1000
print("Recibido")
print(t2-t1)
cs.close()
