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
        conn.send("Nemo".encode())
        quest = conn.recv(2048).decode()
        print(quest)
        timer = time.time()
        thread = threading.Thread(target = getAnswer, args = ())
        thread.start()
        while time.time() - timer < 10:
            if answer != "":
                conn.send(answer.encode())
                break
        thread.join()
        winner =  conn.recv(2048).decode() 
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
            msg,addr = client_udp.recvfrom(2048)
            cookie,msgType,port=struct.unpack('IBH',msg)
            if cookie!=0xabcddcba or msgType!=0x2:
                continue
        client_udp.close()


        #TCP
        print("Received offer from "+str(addr[0])+", attempting to connect...")
        if client_tcp == None:
            client_tcp = socket(AF_INET, SOCK_STREAM)
        client_tcp.connect((addr[0],port))

        game(client_tcp)
    except Exception as e:
        pass

protocol()