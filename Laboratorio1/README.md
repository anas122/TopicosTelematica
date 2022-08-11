# Info de la materia: ST0263 Tópicos Especiales en Telemática
#
# Estudiante(s): Ana Sofia Arango Gonzalez, asarangog@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# Laboratorio 1
#
# 1. Breve descripción de la actividad
Implementación de un mini servidor de web sockets y HTTP requests
#
## 1.1. Qué aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
El mini servidor escucha peticiones HTTP a nivel de sockets TCP en cualquier puerto, procesa el mensaje, localiza el recurso y en caso de que el recurso exista, envia el objeto por sockets a través de HTTP response, sino envia un mensaje como respuesta. También es concurrente, decodifica el protocolo HTTP Request y HTTP Response en consola por medio de un menú y el servidor entrega archivos .html y cualquier otro tipo de archivos como .pdf, .json, entre otros.

## 1.2. Qué aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
No hay manera de verificar si los métodos son 100% HTTP. Las instancias están creadas en el servidor de AWS, el servidor está desplegado y funciona correctamente, pero con el cliente ocurre un error al ejecutarse.

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Como mejores prácticas se utilizó DRY y KISS.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Python 3.10.6  
Libreria socket versión de Python 3.10.6  
Libreria socketserver versión de Python 3.10.6  
Libreria json versión de Python 3.10.6  
Libreria time versión de Python 3.10.6

## Cómo se compila y ejecuta.
Para ejecutar el programa se abren dos terminales y se ejecuta el comando "python main.py" en cada terminal, para así poder abrir el cliente en una y el servidor en otra.

## Detalles técnicos
El programa funciona en cualquier sistema operativo que tenga Python.

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Python 3.10.6

# IP o nombres de dominio en nube o en la máquina servidor.
IP de la máquina servidor: 34.194.9.46

## Una mini guia de como un usuario utilizaría el software o la aplicación
Para ejecutar el programa se abren dos terminales y se ejecuta el comando "python main.py" en cada terminal, para así poder abrir el cliente en una y el servidor en otra.

# Referencias:
## https://github.com/sagudeloo/MyFirstTCPServer/blob/main/server.py 


#### Versión README.md -> 1.0 (2022-agosto)