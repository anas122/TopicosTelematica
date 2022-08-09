import socket as s, socketserver
import json

class Web():
    socketServer:socketserver.ThreadingTCPServer
    def __init__(self, port, host):
        self.socketServer = socketserver.ThreadingTCPServer((host, port), RequestManager)
        self.BUFFER_SIZE = 4096

    def web_start(self):
        print("Servidor iniciado con éxito")
        self.socketServer.serve_forever()
        
        

class RequestManager(socketserver.StreamRequestHandler):
    def handle(self):
        clientAddress = self.request.getpeername()
        print(clientAddress, "conectado exitosamente")

        def get():
            print("Se ha recibido una HTTP-Request de GET desde ", clientAddress)
            data = """
                    <html>
                    <header><title>Esta es la aplicacion</title></header>
                    <body>
                    Hola Mundo
                    </body>
                    </html>
                """
            self.connection.sendall(json.dumps(data).encode('utf-8'))
            print("Se ha enviado una HTTP-Response")
            
        def post(data):
            print("Se ha recibido una HTTP-Request de POST desde " , clientAddress , "con esta información: " , data )
            response =  "HTTP/0.9 200 OK\n\n %s" %data 

            self.connection.sendall(json.dumps(response).encode('utf-8'))
            print("Se ha enviado una HTTP-Response")
        
        def uploadFile(fileName):
            path = "localFiles"
            
            serverAddress = self.server.server_address[0]
            dataPort = self.client_address[1] + 10
            
            filename = fileName
            dataSock = s.socket(s.AF_INET, s.SOCK_STREAM)
            dataSock.bind((serverAddress, dataPort))
            dataSock.listen(1)
            conn, _ = dataSock.accept()
            with open(path+"/"+filename, "rb") as file:
                try:
                    data = file.read(1024)
                    while (data):
                        conn.sendall(data)
                        data = file.read(1024)
                except Exception as e:
                    print(e)
            dataSock.close()
            print("Archivo subido con éxito")
        
        def downloadFile(fileName):
            path = "localFiles"

            serverAddress = self.server.server_address[0]
            dataPort = self.client_address[1] + 10
            
            dataSock = s.socket(s.AF_INET, s.SOCK_STREAM)
            dataSock.bind((serverAddress, dataPort))
            dataSock.listen(1)
            conn, _ = dataSock.accept()
           
            filename = fileName
            
            with open(path+"/"+filename, "wb") as file:
                try:    
                    data = conn.recv(1024)
                    while (data):
                        file.write(data)
                        data = conn.recv(1024)
                except Exception as e:
                    print(e)
            dataSock.close()
            print("Archivo descargado con éxito")


        entryBytes = self.connection.recv(1024)
        data = json.loads(entryBytes.decode('utf-8'))
        
        if(data.get("method") == "GET"):
            get()
        
        elif(data.get("method") == "POST"):
            post(data.get("value"))

        elif(data.get("method") == "UPL"):
            downloadFile(data.get("value"))

        elif(data.get("method") == "DWL"):
            uploadFile(data.get("value"))


        