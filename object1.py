import socket
import sys
import threading
import os

#Single packet representation class.
class Packet(object):
    def __init__(self, seqNumber, character):
        self.seqNumber  = seqNumber
        self.character  = character
        self.serialized = str(seqNumber)+":"+str(character)
    
    def unserialize(self, serializedString):
        self.seqNumber, self.character = serializedString.split(':', 1)
        self.seqNumber = int(self.seqNumber)
        self.serialized = serializedString

    def getSerialized(self):
        return self.serialized

#Node representation. Superclass containing server, middle, and client.     
class Node(object):
   def __init__(self, mode, port):
        self.mode         = mode
        self.port         = port
        #TCP/IP socket for use:
        self.sock         = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        connectAddress = ('localhost',self.port)
        self.sock.connect(connectAddress)

    def bind(self , portToBind):
        bindAddress = ('localhost',self.port)
        self.sock.bind(bindAddress)
    
    def closeSocket(self):
        self.sock.close()
                                 
class Client(Node):
    def __init__(self, mode, port, timeout, windowSize):
        super(Client,self).__init__(mode, port)
        self.packetList = []
        self.ackArray = [] #
        self.lower = 0 #lower and upper to handle sliding window
        self.upper = windowSize - 1
        self.windowSize = windowSize
        self.timeout    = timeout
        print 'client'

    def readFromFile(self, filename):
        with open(filename) as f:
            counter = 0
            while True:
                readChar = f.read(1)
                if not readChar:
                    break
                counter += 1 
                self.packetList.append(packet(counter,readChar))

    def sendPacket(self, index):
        self.sock.send(packetList[index].getSerialized())
    
    def sendWindow(self):
        i = self.lower
        while i <= self.upper:
            self.sendPacket(i)
            i += 1
        
    def recieveAck(self):
        ack = self.sock.recv(1)
        if ack:
            self.ackArray[int(ack)] = True 
    
    def checkAllAcks(self):
        completed = any(ack == False for ack in self.ackArray)
        if completed is False:
            for i in [i for i,x in enumerate(self.ackArray) if x == False]:
                self.sendPacket(self.lower+i)
        else:
            self.lower += self.windowSize
            self.upper += self.windowSize
              

class Server(Node):
    def __init__(self, mode, port, timeout, windowSize):
        super(Server, self).__init__(mode, port)
        self.packetList = []
        self.timeout    = timeout
        self.windowSize = windowSize
        print 'server'
    
    def sendAck(self):
        self.sock.send('')#manda ACK
        
    def listen(self):
        self.sock.listen(self.windowSize)
        
    def recieve(self):
        self.sock.recv(1024)



class Middle(Node):#proba
    def __init__(self, mode, clientPort, serverPort):
        self.mode = mode
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# def ReadFile(name, sock):
#     filename = sock.recv(1024)
#     if os.path.isfile(filename):
#         sock.send("Exists " + str(os.path.getsize(filename)))
#         userResponse = sock.recv(1024)
#         if userResponse[:2] == 'ok':
#             with open(filename, 'rb') as f:
#                 bytesToSend = f.read(1024)
#                 sock.send(bytesToSend)
#                 while bytesToSend != "":
#                     bytesToSend = f.read(1024)
#                     sock.send(bytesToSend)
#     else:
#         sock.send("ERR")
        
#     sock.close()
    
# def Main():
#     host = '127.0.0.1'
#     port = 5000
    
#     print "Hola!"
    
#     s = socket.socket()
#     s.bind((host,port))
    
#     s.listen(5)
    
#     print "Server Started"
    
#     while True:
#         c, addr = s.accept()
#         print "client connected ip: " + str(addr)
#         t = threading.Thread(target=ReadFile, args=("retrThread", c))
#         t.start()
    
#     s.close()
    
# if __name__ == '__main__':
#     Main()
