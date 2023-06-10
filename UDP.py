import socket
import time
from threading import Thread
from SimulationPackage import SimulationPackage

class UDP:
    def __init__(self, IP = "127.0.0.1", ListeningPort = 8080,SendingPort = 8081):
        """
        Initializes a new instance of the class with the given IP address, listening port, and sending port.
        :param IP: A string representing the IP address in the format "xxx.xxx.xxx.xxx". Default is "127.0.0.1".
        :param ListeningPort: An integer representing the port number for listening. Default is 8080.
        :param SendingPort: An integer representing the port number for sending. Default is 8081.
        """
        self.active = True
        self.ip = IP
        self.listeningPort = ListeningPort
        self.sendingPort = SendingPort

        self.reciveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.reciveSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.reciveSocket.bind((self.ip, self.listeningPort))
        self.reciveThread = Thread(target=self.reciveThreadFn,daemon=True)
        self.reciveThread.start()
        
        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sendAdress = (self.ip, self.sendingPort)
        self.sendSocket.connect()

        """
        This code continuously attempts to establish a TCP connection to a target address specified
        by self._sendAddress. The while True: loop ensures that the code keeps running until a connection is established.
        The if statement checks if the connection was not successful, and if so, attempts to connect again.
        If the connection is successful, the loop is broken and the program continues to the next line.
        The print() statement simply indicates that the program is waiting for a connection.
        """                  
        
        self.packages = []
        self._lastGettedPackage = None
                
    def SendString(self,str):
        byt = str.encode()
        print(f"size {len(byt)}")
        self.sendSocket.send(byt)
    
    def reciveThreadFn(self):
        while self.active:
            data, addr = self.reciveSocket.recvfrom(8192)
            data = data.decode()
            if(len(data) > 0):
                self.packages.append(data)                
                if(len(self.packages) > 100):
                    self.packages.pop(0)
    
    def GetNewPackage(self):
        outPackage = None
        if self._lastGettedPackage == None:
            if len(self.packages) > 0:
                outPackage = self.packages[-1]
                self._lastGettedPackage = outPackage
                return True,outPackage
            return False,None
        if self._lastGettedPackage == self.packages[-1]:
            return False,None
        
        outPackage = self.packages[-1]
        self._lastGettedPackage = outPackage
        return True,outPackage
       
    def Close(self):
        self.active = False
        self.sendSocket.close()        
        self.reciveThread.join()
        self.reciveSocket.close()

