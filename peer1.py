import socket
import threading
import json
import re
from PyQt5 import QtCore, QtGui, QtWidgets

HEADER = 64
SERVER = '172.22.208.1'
PORT = 55555
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 0))
server.listen()

PEER = socket.gethostbyname(socket.gethostname())
PEER_PORT = server.getsockname()[1]

ADDR = (PEER, PEER_PORT)

print(ADDR)

class Ui_MainWindow(object):
    def __init__(self):
        self.peerSockets = []
        self.peerNicknames = []
        self.peersList = []
        self.chat = {}

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(782, 701)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Online = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Online.setFont(font)
        self.Online.setObjectName("Online")
        self.verticalLayout_2.addWidget(self.Online)
        self.scrollArea = QtWidgets.QScrollArea(self.frame_2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 206, 585))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.onlineList = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.onlineList.setObjectName("onlineList")
        self.onlineList.itemClicked.connect(self.startChat)
        self.gridLayout_3.addWidget(self.onlineList, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.Name = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Name.setFont(font)
        self.Name.setObjectName("Name")
        self.verticalLayout.addWidget(self.Name)
        self.chatDisplay = QtWidgets.QTextBrowser(self.frame_2)
        self.chatDisplay.setObjectName("chatDisplay")
        self.verticalLayout.addWidget(self.chatDisplay)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sendText = QtWidgets.QPlainTextEdit(self.frame_2)
        self.sendText.setObjectName("sendText")
        self.horizontalLayout.addWidget(self.sendText)
        self.uploadButton = QtWidgets.QPushButton(self.frame_2)
        self.uploadButton.setObjectName("uploadButton")
        self.horizontalLayout.addWidget(self.uploadButton)
        self.sendButton = QtWidgets.QPushButton(self.frame_2)
        self.sendButton.setObjectName("sendButton")
        self.sendButton.clicked.connect(self.sendMessage)
        self.horizontalLayout.addWidget(self.sendButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 40)
        self.verticalLayout.setStretch(2, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 5)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 782, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def initOnline(self):
        for peer in self.peerNicknames:
            self.onlineList.addItem(peer)
            self.chat[peer] = []

    def joinPeer(self, name):
        #self.peerNicknames.append(name)
        self.onlineList.addItem(name)
        self.chat[name] = []

    def takeinput(self):
        name, done = QtWidgets.QInputDialog.getText(self.Name, 'Input Dialog', 'Enter your name:')
        if done:
            self.nickname = name
            print(self.nickname)

    def startChat(self, chatPeer):
        self.Name.setText(chatPeer.text())
        self.displayChatHistory(chatPeer.text())

    def displayChatHistory(self, name):
        self.chatDisplay.clear()
        chatHistory = self.chat[name]
        for message in chatHistory:
            self.chatDisplay.append(message)

    def leftPeer(self, name):
        #self.peerNicknames.remove(name)
        self.chat[name].append(f"{name} has left the chat")
        self.onlineList.clear()
        for peer in self.peerNicknames:
            print("hihi debug")
            self.onlineList.addItem(peer)

    def sendMessage(self):
        if(self.sendText.toPlainText() and self.Name.text() in self.peerNicknames):
            current = self.Name.text()
            message = f"{self.nickname}: {self.sendText.toPlainText()}"
            self.chat[current].append(message)
            self.sendText.clear()
            self.displayChatHistory(current)
            print("CHAT", self.peerNicknames)
            receiverSocket = self.peerSockets[self.peerNicknames.index(current)]
            write_thread = threading.Thread(target=sendMessage, args=(receiverSocket, message))
            write_thread.start()
            write_thread.join()

    def receiveMessage(self, name, message):
        self.chat[name].append(message)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Online.setText(_translate("MainWindow", "Online"))
        self.Name.setText(_translate("MainWindow", "TextLabel"))
        self.uploadButton.setText(_translate("MainWindow", "Upload"))
        self.sendButton.setText(_translate("MainWindow", "Send"))


import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
ui.takeinput()
nickname = ui.nickname
ui.initOnline()

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
    while True:
        try:
            message = receiveMessage(client)
            if message == 'NICK':
                #client.send(nickname.encode(FORMAT))
                sendMessage(client, nickname)
            elif message == 'ONL':
                sendMessage(client, json.dumps(ADDR))
                ui.peersList = json.loads(receiveMessage(client))
                ui.peerNicknames = json.loads(receiveMessage(client))
                print("ONL", ui.peerNicknames)
                print('Online peers:')
                for p, n in zip(ui.peersList, ui.peerNicknames):
                    print(f"{n}: {p}")
                    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    newSocket.connect(tuple(p))
                    ui.peerSockets.append(newSocket)
                #ui.online = peerNicknames
                ui.initOnline()
            elif message == 'NEW':
                peerAddr = json.loads(receiveMessage(client))
                peerNickname = receiveMessage(client)
                newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                newSocket.connect(tuple(peerAddr))
                ui.peersList.append(peerAddr)
                ui.peerSockets.append(newSocket)
                ui.peerNicknames.append(peerNickname)
                print("NEW", ui.peerNicknames)
                ui.joinPeer(peerNickname)
                print(f'New peers connected: {peerNickname} {peerAddr}')
            elif message == 'LEFT':
                peerAddr = json.loads(receiveMessage(client))
                print("first index")
                index = ui.peersList.index(peerAddr)
                print(index)
                print("second index")
                print(ui.peerSockets)
                peerSocket = ui.peerSockets[index]
                print(peerSocket)
                print("third index")
                print(ui.peerNicknames)
                peerNickname = ui.peerNicknames[index]
                print(peerNickname)
                print("final")
                ui.peersList.remove(peerAddr)
                ui.peerSockets.remove(peerSocket)
                ui.peerNicknames.remove(peerNickname)
                print("LEFT",ui.peerNicknames)
                ui.leftPeer(peerNickname)
            else:
                print(message)
        except Exception as e:
            print("[An error has occured]")
            print(e)
            print("[Disconnected!]")
            client.close()
            break

# def startChat(receiver):
#     # global peerNicknames
#     # global peerSockets
#     # while True:
#     #     print(f'{peerNicknames} choose')
#     #     receiver = input("To: ")
#     #     if(receiver not in peerNicknames):
#     #         print(f'{receiver} is not connected')
#     #         pass
#     #     else:
#     receiverSocket = peerSockets[peerNicknames.index(receiver)]
#     write_thread = threading.Thread(target=write, args=(receiverSocket,))
#     write_thread.start()
#     write_thread.join()

# def write(client):
#     while True:
#         message = input("")
#         if(message == "exit"):
#             break
#         sendMessage(client, f'{nickname}: {message}')

def handle(client):
    while True:
        try:
            message = receiveMessage(client)
            ui.receiveMessage(re.findall('^(.*):', message)[0], message)
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

sys.exit(app.exec_())