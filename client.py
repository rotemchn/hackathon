from socket import*
import time
import threading

answer = ""
client_tcp = None

def getAnswer():
    global answer
    answer = int(input())
    

def game(conn):
    quest = conn.recv(1024).decode()
    print(quest)
    timer = time.time()
    thread = threading.Thread(target = getAnswer, args = ())
    thread.start()
    while time.time() - timer < 10:
        if answer != "":
            conn.send(answer.encode())
            break
    thread.join()
    winner =  conn.recv(1024).decode() 
    print(winner)
    protocol()


def protocol():
    global client_tcp
    #UDP
    port = 3333
    client_udp = socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    client_udp.bind(('',port))
    print("Client started, listenning for offer requests...")
    msg = addr =  None
    while msg != None:
        msg,addr = client_udp.recvfrom(1024)
    client_udp.close()


    #TCP
    print("Received offer from "+str(addr)+", attempting to connect...")
    if client_tcp == None:
        client_tcp = socket(AF_INET, SOCK_STREAM)
    client_tcp.connect((socket.gethostname(),port))

    game(client_tcp)

protocol()