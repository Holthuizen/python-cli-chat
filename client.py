import socket
from utils import sanitize, _input
#connection = sanitize(_input("connection string",128))
# mode,public,local,port,id
# example of local connect_id 178.30:5050:44
# example of public connect_id 5.500.200.10:178.30:30

#setup 
SERVER = ''
input_str = "178.30:53006:44"
c = input_str.split(':')
if len(c) == 3:
    SERVER = "192.168."+c[0]
elif len(c) == 4: 
    SERVER = c[0]
else: 
    print("connection input invalid error")
    exit()

PORT = int(c[1])
ID = int(c[2])
print(SERVER,PORT ,ID)

HEADER= 10
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#blocking, can timeout
client.connect(ADDR)
print(f"connected to server {ADDR[0]} at {ADDR[1]}")

def send(message):
    message = message.encode(FORMAT)
    message_header = f"{len(message):<{HEADER}}".encode('utf-8')
    msg = message_header + message
    client.send(msg)
    if message.decode(FORMAT) == DISCONNECT_MESSAGE: 
        return False
    receive(client)
    return True

def receive(conn):
    message_header = conn.recv(HEADER)
    msg_length = int(message_header.decode('utf-8').strip())
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        print(f"{msg}")

sending = True
while sending: 
    msg = _input("client",1024)
    sending = send(msg)
    #send(DISCONNECT_MESSAGE)

client.close()
exit()

