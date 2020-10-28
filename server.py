import socket 
import threading

HEADER = 10
PORT = 53006
SERVER = "0.0.0.0"  #socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
STATUS = {"ok":200,"not_found": 404}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send(message, conn):
    message = message.encode(FORMAT)
    message_header = f"{len(message):<{HEADER}}".encode('utf-8')
    conn.send(message_header + message)

def receive(conn):
    message_header = conn.recv(HEADER)
    if message_header:
        msg_length = int(message_header.decode('utf-8').strip())
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                return False
            print(f"{msg_length} -> {msg}")
            return True

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
            #non blocking
            connected = receive(conn)
            if not connected: 
                break
            msg = input("server > ")
            send(msg,conn)
    conn.close()
    print(f"client {addr} disconnected", end='\n\n\n')
    print(f"[LISTENING] Server is listening on {SERVER}")



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #respond
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")

start()
