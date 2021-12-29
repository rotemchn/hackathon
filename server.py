from socket import*
import threading
import time
import random
import struct

wait = True
answer = []
server_tcp = None

def waiting(msg, clientAddress, server_udp):
    while wait:
        server_udp.sendto(msg,clientAddress)
        time.sleep(1)
    server_udp.close()

def getAnswer(player, conn):
    global answer
    answer.append((conn.recv(1024).decode(),player))


def game(conn1,conn2):
    conn1.send("Please enter your name: U+1F920".encode())
    conn2.send("Please enter your name: U+1F920".encode())
    name1 = conn1.recv(1024).decode()
    name2 = conn2.recv(1024).decode()
    num1= random.randint(0,9)
    num2= random.randint(0,9-num1)
    operator = ["+","-"]
    place = random.randit(0,1)
    quest = ""
    result = 0

    if num1 > num2:
        quest = str(num1)+operator[place]+str(num2)
        if place == 0:
            result = num1+num2
        else: result= num1-num2
    else:
        quest = str(num2)+operator[place]+str(num1)
        if place == 0:
            result = num1+num2
        else: result= num2-num1

    msg = \
        f"""
        Welcome to Quick Maths.
        Player 1: {name1}
        Player 2: {name2}
        ==
        Please answer the following question as fast as you can:
        How much is {quest}?
        """
    conn1.send(msg.encode())
    conn2.send(msg.encode())
    
    thread1 = threading.Thread(target = getAnswer, args=(1,conn1))
    thread2 = threading.Thread(target = getAnswer, args=(2,conn2))
    thread1.start()
    thread2.start()
    timer = time.time()

    while time.time() - timer < 10:
        if answer[0] != None:
            thread1.join()
            thread2.join()
            break
    
    
    msg = ""
    if len(answer)==0:
        msg = \
            f"""
            Game over!
            The correct answer was {result}!
            The game finished with a draw.
            """
    elif int(answer[0][0]) == result:
        msg = \
            f"""
            Game over!
            The correct answer was {result}!
            Congratulations to the winner: {name1 if answer[0][1]==1 else name2}
            """
    else: 
        msg = \
            f"""
            Game over!
            The correct answer was {result}!
            Congratulations to the winner: {name2 if answer[0][1]==1 else name1}
            """

    conn1.send(msg.encode())
    conn1.close()
    conn2.send(msg.encode())
    conn2.close()
    conn1 = conn2 = None
    print("Game over, sending out offer requests...")
    protocol()

def protocol():
    global server_tcp
    global wait
    #UPD
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server_udp.bind(('',13117))
    print ("Server started, listening on IP address 172.1.0.36")
    server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    port = 3333 
    thread = threading.Thread(target=waiting, args=(struct.pack('LBH',0xabcddcba, 0x2, port), ('<broadcast>', 13117),server_udp))
    thread.start()


    #TCP
    if server_tcp == None:
        server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_tcp.bind(("172.1.0.36", port))
    server_tcp.listen(2)
    conn1 = conn2 = None
    #addr1 = addr2 = None

    while not (conn1 and conn2):
        if conn1 == None and conn2 == None:
            conn1, addr1 = server_tcp.accept() 
        else: conn2, addr2 = server_tcp.accept()
    wait = False
    game(conn1,conn2)

protocol()
