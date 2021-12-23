from socket import*
import threading
import time

wait = True
def waiting(msg, clientAddress):
    while wait:
        server_udp.sendto(msg,clientAddress)
        time.sleep(1)

#UPD
server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server_udp.bind(('',13117))
print ("Server started, listening on IP address 172.1.0.36")
server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
port = 3333 
thread = threading.Thread(target=waiting, args=("Server started, listening on IP address 172.1.0.36", ('<broadcast>', 13117)))
thread.start()

#TCP
server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_tcp.bind(("172.1.0.36", port))
server_tcp.listen(2)
