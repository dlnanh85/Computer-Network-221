import socket
import threading
import json
import sqlite3 as sl


HEADER = 64
PORT = 55555
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

con = sl.connect('user.db')

peers = []
peer_addr = []
peer_server_addr = []
nicknames = []

def broadcast(message):
    for peer in peers:
        sendMessage(peer, message)

def sendMessage(peer, msg):
    if(msg):
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


def sendPeersList(peer, nickname):
    peerNicknames = json.dumps(nicknames)
    sendMessage(peer, 'ONL')
    try:
        peerServer = receiveMessage(peer)
        sendMessage(peer, json.dumps(peer_server_addr))
        sendMessage(peer, peerNicknames)
        peer_server_addr.append(json.loads(peerServer))
        nicknames.append(nickname)
        broadcastNewPeer(peerServer, nickname)
        exists = con.execute(f"SELECT EXISTS(SELECT 1 FROM USER WHERE name = '{nickname}')")
        for row in exists:
            if row[0] == 0:
                con.execute(f"INSERT INTO USER (name, friends) VALUES ('{nickname}', '[]')")
                sendMessage(peer, '[]')
            else:
                friends = con.execute(f"SELECT friends FROM USER WHERE name = '{nickname}'")
                for friend in friends:
                    sendMessage(peer, friend[0])
    except Exception as e:
        print("Something went wrong")
        print(e)

def broadcastNewPeer(peer_addr, nickname):
    for peer in peers:
        sendMessage(peer, 'NEW')
        sendMessage(peer, peer_addr)
        sendMessage(peer, nickname)

def broadCastLeftPeer(peer_addr):
    for peer in peers:
        sendMessage(peer, 'LEFT')
        sendMessage(peer, json.dumps(peer_addr))

def handle(client):
    while True:
        try:
            message = receiveMessage(client)
            print(message)
            broadcast(message)
        except:
            index = peers.index(client)
            peers.remove(client)
            client.close()
            addr = peer_addr[index]
            nickname = nicknames[index]
            serverAddr = peer_server_addr[index]
            print(f'{nickname} left!')
            broadcast(f'{nickname} left!')
            peer_addr.remove(addr)
            nicknames.remove(nickname)
            peer_server_addr.remove(serverAddr)
            broadCastLeftPeer(serverAddr)
            break

def receive():
    while True:
        peer, address = server.accept()
        print(f"{str(address)} has connected")

        sendMessage(peer, 'NICK')
        nickname = receiveMessage(peer)

        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} has joined")
        sendMessage(peer, "Connected to server")
        sendPeersList(peer, nickname)
        peers.append(peer)
        peer_addr.append(address)

        thread = threading.Thread(target=handle, args=(peer,))
        thread.start()

print("[Server is listening]...")
receive()