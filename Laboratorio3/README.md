# Info de la materia: ST0263 Tópicos Especiales en Telemática
#
# Estudiante(s): Ana Sofia Arango Gonzalez, asarangog@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# Laboratorio 3
#
# 1. Breve descripción de la actividad
Despliegue de una aplicación Wordpress con Docker en una instancia GCP y asignación de un dominio con certificado SSL.

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Despliegue de la aplicación Wordpress con Docker en la instancia de GCP. Asignación de un dominio propio con certificado SSL válido con Let's Encrypt.

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Todos los aspectos se cumplieron y desarrollaron.

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se utilizaron contenedores en Docker para la ejecución del proyecto.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

## Detalles del desarrollo.
Siguiendo el tutorial brindado por el profesor:
1. Se creó una instancia en GCP.
2. Se le asignó una dirección IP estática externa.
3. Se creó un conjunto de registros en GCP y se le asignaron los nombres de servidores al dominio propio.
4. Desde la instancia de GCP se instaló certbot, letsencrypt y nginx.
5. Se configuró nginx con el archivo "nginx.conf".
6. Se solicitaron los certificados ssl con letsencrypt y certbot.
7. Se instaló y se inicializó el docker.
8. Se clonó el repositorio donde se usarán los archivos de configuración.
9. Se inicializó el servidor Wordpress.

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o nombres de dominio en nube o en la máquina servidor.
IP elástica de la máquina servidor: 34.72.7.237
Nombre de dominio: asarangog.tk
Dominio con certificación ssl: https://www.asarangog.tk

## Una mini guia de como un usuario utilizaría el software o la aplicación
El usuario puede acceder desde cualquier navegador al link https://www.asarangog.tk y disfrutar de la aplicación.

## Resultados o pantallazos
![App](https://user-images.githubusercontent.com/37346028/191159573-394807f6-c804-4dfe-9089-1c98ef1cb0ba.PNG)

# 5. Otra información que considere relevante para esta actividad.

# Referencias:
## https://github.com/st0263eafit/st0263-2022-2/tree/main/docker-nginx-wordpress-ssl-letsencrypt

#### versión README.md -> 1.0 (2022-septiembre)
