import socket
import time

cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cs.connect((socket.gethostname(),5000))

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
