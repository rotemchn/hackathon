from socket import*
import threading
import time
import random

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
thread = threading.Thread(target=waiting, args=("Server started, listening on IP address 172.1.0.36".encode(), ('<broadcast>', 13117)))
thread.start()

#TCP
server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_tcp.bind(("172.1.0.36", port))
server_tcp.listen(2)
conn1, addr1 = server_tcp.accept()
# client_thread1 = threading.Thread(target= )
conn2, addr2 = server_tcp.accept()

def game(conn1):
    conn1.send("Please enter your name: U+1F920".encode())
    name1 = conn1.recv(1024).decode()
    name2 = None
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
    timer = time.time()
    if time.time() - timer == 10:
        pass
    
    ans = conn1.recv(1024).decode()

    msg = ""
    if int(ans) == result:
        msg = \
            f"""
            Game over!
            The correct answer was {result}!
            Congratulations to the winner: {name1}
            """
    else: 
        msg = \
            f"""
            Game over!
            The correct answer was {result}!
            Congratulations to the winner: {name2}
            """

    conn1.send(msg.encode())
    conn1.close()
