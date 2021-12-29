from socket import*
import time
import threading
import struct

answer = ""
client_tcp = None

def getAnswer():
    try:
        global answer
        answer = int(input())
    except Exception as e:
        pass
    

def game(conn):
    try:
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
    except Exception as e:
        pass


def protocol():
    try:
        global client_tcp
        #UDP
        port = 3333
        client_udp = socket(AF_INET,SOCK_DGRAM)
        client_udp.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        client_udp.bind(('',port))
        print("Client started, listenning for offer requests...")
        msg = addr =  None
        while msg != None:
            msg,addr = client_udp.recvfrom(1024)
            cookie,msgType,port=struct.unpack('>IBH',msg)
            if hex(int(cookie))!=hex(2882395322) or int(msgType)!=2:
                continue
        client_udp.close()


        #TCP
        print("Received offer from "+str(addr)+", attempting to connect...")
        if client_tcp == None:
            client_tcp = socket(AF_INET, SOCK_STREAM)
        client_tcp.connect((gethostname(),port))

        game(client_tcp)
    except Exception as e:
        pass

protocol()