import socket as s
import json

class Client():
    
    def __init__(self, port, host, dataPort):
        self.socketPort = port
        self.dataPort = dataPort
        self.socket = s.socket()
        self.host = host
        self.path = "localFiles"

    def clientStart(self):
        try:
            self.socket.connect((self.host,self.socketPort))
        except:
            print(s.error())
            return
        print("Connected to the server " + self.host)
        
        self.commandMenu()
    def receiveData(self):
        response = self.socket.recv(1024)
        data = json.loads(response.decode('utf-8'))
        print(data)
    
    def sendGet(self):
        dataPacket = {"method" : "GET"}
        validData = json.dumps(dataPacket).encode('utf-8')
        self.socket.sendall(validData)

    def sendPost(self, data):
        dataPacket = {
            "method" : "POST",
            "value" : data
                    }
        validData = json.dumps(dataPacket).encode('utf-8')
        self.socket.sendall(validData)
    
    def sendFileDownload(self, fileName):
        dataPacket = {
            "method" : "DWL",
            "value" : fileName
            }
        validData = json.dumps(dataPacket).encode('utf-8')    
        self.socket.sendall(validData)
        dataSock = s.socket(s.AF_INET, s.SOCK_STREAM)
        dataSock.bind((self.host, self.dataPort))
        dataSock.listen(1)
        conn, _ = dataSock.accept()
        with open(self.path+"/"+fileName, "wb") as file:
            data = conn.recv(1024)
            while (data):
                file.write(data)
                data = conn.recv(1024)
        dataSock.close()
        return "Archivo descargado con éxito"
    
    def sendFileUpload(self, fileName): 
        dataPacket = {
            "method" : "UPL",
            "value" : fileName
            }
        validData = json.dumps(dataPacket).encode('utf-8')    
        self.socket.sendall(validData)
        dataSock = s.socket(s.AF_INET, s.SOCK_STREAM)
        dataSock.bind((self.host, self.dataPort))
        dataSock.listen(1)
        conn, _ = dataSock.accept()
        with open(self.path+"/"+fileName, "rb") as file:
            data = file.read(1024)
            while (data):
                conn.sendall(data)
                data = file.read(1024)
        dataSock.close()
        return "Archivo subido con éxito"
        
    
    
    def commandMenu(self):
        entryPoint = input("Bienvenido al server, escoja alguna de las siguientes opciones \n1. Envíar una GET request simple \n2. Envíar una POST request simple \n3. Recibir un archivo tipo PDF \n4. Envíar un archivo \n")
        if(entryPoint is not None):
            if(entryPoint == "1"):
                self.sendGet()
                self.receiveData()
            elif(entryPoint == "2"):
                data = input("Por favor ingrese su primer nombre y género así; \"John, hombre\"")
                self.sendPost(data)
                self.receiveData()
            elif(entryPoint == "3"):
                data = input("Por favor ingrese el nombre del archivo \n")
                self.sendFileDownload(data)
            elif(entryPoint == "4"):
                data = input("Por favor ingrese el nombre del archivo \n")
                self.sendFileUpload(data)
        