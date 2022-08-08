import socket as s, socketserver
import json

class Web():
    socketServer:socketserver.ThreadingTCPServer
    
    def __init__(self, port, host, dataPort):
        self.socketServer = socketserver.ThreadingTCPServer((host, port), RequestManager)
        self.path = "localFiles"
        self.BUFFER_SIZE = 4096
        self.dataPort = dataPort
        
    def web_start(self):
        print("Servidor iniciado con éxito")
        self.socketServer.serve_forever()
        
        

class RequestManager(socketserver.StreamRequestHandler):
    def handle(self):
        clientAddress = self.request.getpeername()
        print(clientAddress, "conectado exitosamente")

        entryBytes = self.connection.recv(1024)
        data = json.loads(entryBytes.decode('utf-8'))
        
        if(data.get("method") == "GET"):
            self.get()
        
        elif(data.get("method") == "POST"):
            self.post(data.get("value"))

        elif(data.get("method") == "UPL"):
            self.downloadFile(data.get("value"))

        elif(data.get("method") == "DWL"):
            self.uploadFile(data.get("value"))


    def get(self):
        clientAddress = self.request.getpeername()
        print("Se ha recibido una HTTP-Request de GET desde ", clientAddress)
        data = """
                <html>
                <header><title>Esta es la aplicación</title></header>
                <body>
                Hola Mundo
                </body>
                </html>
            """
        self.connection.sendall(json.dumps(data).encode('utf-8'))
        print("Se ha enviado una HTTP-Response")
        
    def post(self, data):
        clientAddress = self.request.getpeername()
        print("Se ha recibido una HTTP-Request de POST desde " , clientAddress , "con esta información: " , data )
        response =  "HTTP/0.9 200 OK\n\n %s" %data 

        self.connection.sendall(json.dumps(response).encode('utf-8'))
        print("Se ha enviado una HTTP-Response")
    
    def uploadFile(self, fileName):
        filename = fileName
        dataSock = s.socket(s.AF_INET, s.SOCK_STREAM)
        dataPort = int(self.connection.getsockname()[1]) + 10
        dataSock.bind((self.connection.getpeername()[0], dataPort))
        dataSock.listen(1)
        conn, _ = dataSock.accept()
        with open(self.path+"/"+filename, "rb") as file:
            data = file.read(1024)
            while (data):
                conn.sendall(data)
                data = file.read(1024)
        dataSock.close()
        print("Archivo subido con éxito")
    
    def downloadFile(self, fileName):
        filename = fileName
        dataSock = s.socket(s.AF_INET, s.SOCK_STREAM)
        dataPort = int(self.connection.getsockname()[1]) + 10
        dataSock.bind((self.connection.getpeername()[0], dataPort))
        dataSock.listen(1)
        conn, _ = dataSock.accept()
        with open(self.path+"/"+filename, "wb") as file:
            data = conn.recv(1024)
            while (data):
                file.write(data)
                data = conn.recv(1024)
        dataSock.close()
        return "Archivo descargado con éxito"
