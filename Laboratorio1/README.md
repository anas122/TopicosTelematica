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
1. Se debe instalar Python 3.10 (no hay más dependencias).
2. Clonar el repositorio https://github.com/st0263-2266/lab1-anas122
3. Si se va a ejecutar el programa en AWS o un servicio similar tiene que asegurarse que se cumplan los siguientes requisitos:  
 3.1. Que todas las máquinas estén en el mismo grupo de seguridad o la misma subred.  
 3.2. Que las máquinas tengan los puertos que se vayan a utilizar abiertos (Ejemplo: en este caso el código tiene el puerto 8183, tendríamos que abrir el puerto 8183-8193 en el grupo de seguridad, este último porque es necesario para el envio de datos, el cual es el mismo puerto +10).  
 3.3. En el archivo "main.py" se deben cambiar en las líneas 7 y 11 las direcciones IP para el servidor y el cliente por la dirección IP privada de la máquina del servidor, en todas las máquinas.
4. Se abren dos terminales y se ejecuta el comando "python main.py" en cada terminal, para así poder abrir el cliente en una y el servidor en otra. (En caso de que el comando "python main.py" no funcione, se debe utilizar el comando "python3 main.py").
5. Es importante que al desplegarse el menú que proporciona el programa se elija primero la opción de servidor, la cual es la opción número 1 y en la siguiente terminal se elija la opción 2 que es la de cliente.

## Detalles técnicos
El programa funciona en cualquier sistema operativo que tenga Python 3.10.

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Python 3.10.6

# IP o nombres de dominio en nube o en la máquina servidor.
IP elástica de la máquina servidor: 34.194.9.46

## Una mini guia de como un usuario utilizaría el software o la aplicación
Para utilizar el programa:
1. Se debe instalar Python 3.10 (no hay más dependencias).
2. Clonar el repositorio https://github.com/st0263-2266/lab1-anas122
3. Se abren dos terminales y se ejecuta el comando "python main.py" en cada terminal, para así poder abrir el cliente en una y el servidor en otra. (En caso de que el comando "python main.py" no funcione, se debe utilizar el comando "python3 main.py").
4. Es importante que al desplegarse el menú que proporciona el programa se elija primero la opción de servidor, la cual es la opción número 1 y en la siguiente terminal se elija la opción 2 que es la de cliente.
5. Finalmente el usuario envia información por consola con respecto a lo que el programa vaya mostrando paso a paso.


# Referencias:
## https://github.com/sagudeloo/MyFirstTCPServer/blob/main/server.py 


#### Versión README.md -> 1.0 (2022-agosto)