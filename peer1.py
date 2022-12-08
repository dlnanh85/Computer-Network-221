import socket
import threading
import json

HEADER = 64
SERVER = '192.168.8.6'
PORT = 55555
FORMAT = 'utf-8'

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 0))
server.listen()

PEER = socket.gethostbyname(socket.gethostname())
PEER_PORT = server.getsockname()[1]

ADDR = (PEER, PEER_PORT)

print(ADDR)

peerSockets = []
peerNicknames = []
peersList = []

def sendMessage(peer, msg):
    message = msg.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    peer.send(send_length)
    peer.send(message)

def receiveMessage(peer):
    msg_length = peer.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    msg = peer.recv(msg_length).decode(FORMAT)
    return msg

def receive():
    global peersList
    global peerSockets
    global peerNicknames
    while True:
        try:
            message = receiveMessage(client)
            if message == 'NICK':
                #client.send(nickname.encode(FORMAT))
                sendMessage(client, nickname)
            elif message == 'ONL':
                sendMessage(client, json.dumps(ADDR))
                peersList = json.loads(receiveMessage(client))
                peerNicknames = json.loads(receiveMessage(client))
                print('Online peers:')
                for p, n in zip(peersList, peerNicknames):
                    print(f"{n}: {p}")
                    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    newSocket.connect(tuple(p))
                    peerSockets.append(newSocket)
                start_thread = threading.Thread(target=startChat)
                start_thread.start()
            elif message == 'NEW':
                peerAddr = json.loads(receiveMessage(client))
                peerNickname = receiveMessage(client)
                newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                newSocket.connect(tuple(peerAddr))
                peersList.append(peerAddr)
                peerSockets.append(newSocket)
                peerNicknames.append(peerNickname)
                print(f'New peers connected: {peerNickname} {peerAddr}')
            elif message == 'LEFT':
                peerAddr = json.loads(receiveMessage(client))
                index = peersList.index(peerAddr)
                peerSocket = peerSockets[index]
                peerNickname = peerNicknames[index]
                peerSockets.remove(peerSocket)
                peerNicknames.remove(peerNickname)
            else:
                print(message)
        except Exception as e:
            print("[An error has occured]")
            print(e)
            print("[Disconnected!]")
            client.close()
            break

def startChat():
    global peerNicknames
    global peerSockets
    while True:
        print(f'{peerNicknames} choose')
        receiver = input("To: ")
        if(receiver not in peerNicknames):
            print(f'{receiver} is not connected')
            pass
        else:
            receiverSocket = peerSockets[peerNicknames.index(receiver)]
            write_thread = threading.Thread(target=write, args=(receiverSocket,))
            write_thread.start()
            write_thread.join()

def write(client):
    while True:
        message = input("")
        if(message == "exit"):
            break
        sendMessage(client, f'{nickname}: {message}')

def handle(client):
    while True:
        try:
            message = receiveMessage(client)
            print(message)
        except:
            client.close()
            break

def serverReceive():
    while True:
        peer, address = server.accept()
        print(f"{str(address)} has connected")
        sendMessage(peer, f"Connected to {nickname}")
        thread = threading.Thread(target=handle, args=(peer,))
        thread.start()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

server_thread = threading.Thread(target=serverReceive)
server_thread.start()