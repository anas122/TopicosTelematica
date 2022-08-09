import socket as s
import json
import time

class Client():
    
    def __init__(self, port, host):
        self.socketPort = port
        self.socket = s.socket()
        self.host = host
        self.path = "localFiles"
        self.dataPort = self.socketPort + 10

    def clientStart(self):
        try:
            self.socket.connect((self.host,self.socketPort))
        except:
            print(s.error())
            return
        print("Conectado al servidor " + self.host)
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
        
        time.sleep(1)
        
        dataSock = s.socket(s.AF_INET, s.SOCK_STREAM)
        dataSock.connect((self.host, self.dataPort))
        with open(self.path+"/"+fileName, "wb") as file:
            try:
                data = dataSock.recv(1024)
                while (data):
                    file.write(data)
                    data = dataSock.recv(1024)
            except Exception as e: 
                print(e)
        dataSock.close()
        print("Archivo descargado con exito")
    
    def sendFileUpload(self, fileName): 
        dataPacket = {
            "method" : "UPL",
            "value" : fileName
            }
        validData = json.dumps(dataPacket).encode('utf-8')    
        self.socket.sendall(validData)
        
        time.sleep(1)

        dataSock = s.socket(s.AF_INET, s.SOCK_STREAM)
        dataSock.connect((self.host, self.dataPort))
        with open(self.path+"/"+fileName, "rb") as file:
            try:
                data = file.read(1024)
                while (data):
                    dataSock.sendall(data)
                    data = file.read(1024)
            except Exception as e:
                print(e)
        dataSock.close()
        print("Archivo subido con exito")
        
    
    
    def commandMenu(self):
        entryPoint = input("Bienvenido al server, escoja alguna de las siguientes opciones \n1. Enviar una GET request simple \n2. Enviar una POST request simple \n3. Recibir un archivo \n4. Enviar un archivo \n")
        if(entryPoint is not None):
            if(entryPoint == "1"):
                self.sendGet()
                self.receiveData()
            elif(entryPoint == "2"):
                data = input("Por favor ingrese su primer nombre y genero asi; \"John, hombre\"")
                self.sendPost(data)
                self.receiveData()
            elif(entryPoint == "3"):
                data = input("Por favor ingrese el nombre del archivo \n")
                self.sendFileDownload(data)
            elif(entryPoint == "4"):
                data = input("Por favor ingrese el nombre del archivo \n")
                self.sendFileUpload(data)
    