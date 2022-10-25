# Info de la materia: ST0263 Tópicos Especiales en Telemática
#
# Estudiante(s): Ana Sofia Arango Gonzalez, asarangog@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# Laboratorio 4
#
# 1. Breve descripción de la actividad
Despliegue de una aplicación Wordpress con Docker y nginx en una instancia GCP y asignación de un dominio con certificado SSL. Además, la implementación y conexión de un balanceador de cargas, una base de datos y un servidor de archivos en otras instancias de GCP.

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Despliegue de la aplicación Wordpress con Docker y nginx en la instancia de GCP. Asignación de un dominio propio con certificado SSL válido con Let's Encrypt.  
Implementación de un balanceador de cargas con Docker y nginx en una instancia de GCP, en la capa de aplicación del Wordpress.  
Implementación de un servidor de base de datos con Docker en una instancia de GCP, conectado al Wordpress.  
Implementación de un servidor para archivos con Docker en una instancia de GCP, conectado al Wordpress.

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Se puede acceder al Wordpress desde su dirección IP pública, pero no se logra acceder desde el dominio, aún así teniendo el certificado SSL.

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se utilizaron contenedores en Docker para la ejecución del proyecto, nginx y MySQL.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Docker, Nginx y MySQL.

## Detalles del desarrollo.
1. Para comenzar se crean 5 máquinas virtuales en GCP de tipo ec2-micro y se habilita el tráfico HTTP y HTTPS para cada una.

![1](https://user-images.githubusercontent.com/37346028/197830952-8b523158-ba18-4d2e-8af0-fd9e1306106e.PNG)

2. Se asignan las IP elásticas a cada máquina virtual, reservando la dirección estática externa con la versión de IP como IPv4.

![2](https://user-images.githubusercontent.com/37346028/197831988-310c0fab-e425-4b00-8faa-b36872167068.PNG)

3. Luego, se configura el archivo de zona y los registros DNS en GCP, agregando los registros A y CNAME, más adelante se agregará el registro TXT.

![3](https://user-images.githubusercontent.com/37346028/197833038-b5f3d014-8598-4fdf-b163-76c7856617c4.PNG)

Para el registro A se le asigna la dirección IP elástica de la instancia asignada al balanceador de cargas.

4. Luego, accedemos al dominio en Freenom, en herramientas de gestión, servidores de nombres, seleccionamos la opción "Usar nameservers personalizados (introducir abajo)" y agregamos todos los NS que nos provee GCP en el archivo de zona.

![4](https://user-images.githubusercontent.com/37346028/197835553-73e73278-0dec-414b-9279-99685b4e63f0.PNG)

### 1. Balanceador de cargas
1. Para crear el balanceador de cargas se conecta a la instancia de GCP dando click en la opción SSH de la máquina asignada a este mismo.

2. Se instala certbot, letsencrypt y nginx. Para esto, se ejecutan los siguientes comandos:
```
sudo apt update  
sudo apt install snapd  
sudo snap install certbot --classic  
sudo apt install letsencrypt -y  
sudo apt install nginx -y
```

3. Se ingresa al archivo nginx.conf y se configura:
```
sudo nano /etc/nginx/nginx.conf
```
Se reemplaza todo el contenido por lo siguiente:
```
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections  1024;  ## Default: 1024
}
http {
    server {
        listen  80 default_server;
        server_name _;
        location ~ /\.well-known/acme-challenge/ {
            allow all;
            root /var/www/letsencrypt;
            try_files $uri = 404;
            break;
        }
    }
}
```

4. Se guarda la configuración de nginx con los siguientes comandos:
```
sudo mkdir -p /var/www/letsencrypt
sudo nginx -t
sudo service nginx reload
```

5. Para pedir los certificados SSL se ejecutan los siguientes comandos:
```
sudo letsencrypt certonly -a webroot --webroot-path=/var/www/letsencrypt -m asarangog@eafit.edu.co --agree-tos -d lab4.asarangog.tk
sudo certbot --server https://acme-v02.api.letsencrypt.org/directory -d *.asarangog.tk --manual --preferred-challenges dns-01 certonly
```
Este último comando nos va a generar el código que debemos ingresar en el registro TXT del archivo de zona en GCP.

6. Creamos carpetas para los certificados:
```
mkdir /home/asarangog/nginx
mkdir /home/asarangog/nginx/ssl
```

7. Para hacer los registros se ejecutan los siguientes comandos:
```
sudo su
cp /etc/letsencrypt/live/lab4.asarangog.tk/* /home/asarangog/nginx/ssl/
cp /etc/letsencrypt/live/asarangog.tk/* /home/asarangog/nginx/ssl/
exit
```

8. Se instala docker, docker-compose y git con los siguientes comandos:
```
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt install git -y
```

9. Ponemos a funcionar docker:
```
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker asarangog
sudo reboot
```

10. Clonamos el repositorio del curso de donde usaremos un archivo de configuración:
```
git clone https://github.com/st0263eafit/st0263-2022-2.git
cd st0263-2022-2/docker-nginx-wordpress-ssl-letsencrypt
sudo cp ssl.conf /home/asarangog/wordpress
cd
```

11. Ingresamos a la carpeta y creamos los siguientes archivos:
```
cd nginx
sudo touch docker-compose.yml
sudo touch nginx.conf
```

12. Entramos al archivo nginx.conf con el siguiente comando:
```
sudo nano nginx.conf
```
Añadimos el siguiente contenido, teniendo en cuenta que las direcciones IP de las líneas 10 y 11 corresponden a las instancias del wordpress 1 y 2:
```
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
  worker_connections  1024;  ## Default: 1024
}
http {
  upstream loadbalancer{
    server 10.128.0.56:80 weight=5;
    server 10.128.0.57:80 weight=5;
  }
  server {
    listen 80;
    listen [::]:80;
    server_name _;
    rewrite ^ https://$host$request_uri permanent;
  }
  server {
    listen 443 ssl http2 default_server;
    listen [::]:443 ssl http2 default_server;
    server_name _;
    # enable subfolder method reverse proxy confs
    #include /config/nginx/proxy-confs/*.subfolder.conf;
    # all ssl related config moved to ssl.conf
    include /etc/nginx/ssl.conf;
    client_max_body_size 0;
    location / {
      proxy_pass http://loadbalancer;
      proxy_redirect off;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Host $host;
      proxy_set_header X-Forwarded-Server $host;
      proxy_set_header X-Forwarded-Proto $scheme;
    }
  }
}
```

13. Ingresamos al archivo docker-compose.yml con el siguiente comando:
```
sudo nano docker-compose.yml
```
Añadimos el siguiente contenido:
```
version: '3.1'
services:
  nginx:
    container_name: nginx
    image: nginx
    volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
    - ./ssl:/etc/nginx/ssl
    - ./ssl.conf:/etc/nginx/ssl.conf
    ports:
    - 80:80
    - 443:443
```

14. Detenemos nginx con los siguientes comandos:
```
ps ax | grep nginx
netstat -an | grep 80
sudo systemctl disable nginx
sudo systemctl stop nginx
```

15. Por último, iniciamos Docker:
```
cd /home/asarangog/nginx
docker-compose up --build -d
```

### 2. Servidor de base de datos
1. Para crear el servidor de base de datos se conecta a la instancia de GCP dando click en la opción SSH de la máquina asignada a este mismo.

2. Se instala docker y docker-compose. Para esto, se ejecutan los siguientes comandos:
```
sudo apt install docker.io -y
sudo apt install docker-compose -y
```

3. Creamos un directorio para el docker container y accedemos a este:
```
mkdir docker
cd docker
```

4. Creamos los archivos de configuración con los siguientes comandos:
```
sudo touch Dockerfile
sudo touch docker-compose.yaml
```

5. Ingresamos al archivo Dockerfile:
```
sudo nano Dockerfile
```
Añadimos el siguiente contenido al archivo:
```
FROM mysql:8.0
```

6. Ingresamos al docker-compose.yaml:
```
sudo nano docker-compose.yaml
```
Añadimos el siguiente contenido al archivo:
```
version: "3.7"
services:
  mysql:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: dbserver
    restart: always
    ports:
      - 3306:3306
    environment:
      MYSQL_ROOT_PASSWORD: "1234"
      MYSQL_DATABASE: "wordpressdb"
    volumes:
      - ./schemas:/var/lib/mysql:rw
volumes:
  schemas: {}
```

7. Ponemos a funcionar docker:
```
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker asarangog
sudo reboot
```

8. Corremos el contenedor docker y accedemos a MySQL:
```
cd docker
sudo docker-compose up --build -d
sudo docker exec -it dbserver mysql -p
```
Ingresamos a MySQL con la contraseña creada anteriormente.

9. Creamos la base de datos:
```
CREATE DATABASE wpdb;
```
![7](https://user-images.githubusercontent.com/37346028/197864801-8ec1dd74-71e6-4a95-9730-0916f672d967.PNG)

10. Creamos un usuario para la base de datos y le otorgamos todos los privilegios:
```
CREATE USER 'asarangog' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON *.* TO 'asarangog'@'%';
exit
```

### 3. Servidor NFS
1. Para crear el servidor NFS se conecta a la instancia de GCP dando click en la opción SSH de la máquina asignada a este mismo.

2. Se instala nfs-kernel-server. Para esto, se ejecutan los siguientes comandos:
```
sudo apt update
sudo apt install nfs-kernel-server
sudo apt install ufw
```

3. Se crea una carpeta para compartir archivos en el servidor NFS:
```
sudo mkdir -p /mnt/nfs_share
```

4. Ingresamos al archivo /etc/exports:
```
sudo nano /etc/exports
```
Agregamos el siguiente comando al final del archivo:
```
/mnt/nfs_share 10.128.0.0/20(rw,sync,no_subtree_check)
```

5. Exportamos el nuevo NFS:
```
sudo exportfs
```

6. Actualizamos las nuevas reglas del firewall:
```
sudo systemctl restart nfs-kernel-server
sudo ufw allow from 10.128.0.0/20 to any port nfs
sudo ufw enable
sudo ufw status
sudo ufw allow 22
```

### 4. Servidores de Wordpress
Estos pasos se deben realizar para las dos instancias del Wordpress.

1. Para crear el servidor de Wordpress se conecta a la instancia de GCP dando click en la opción SSH de la máquina asignada a este mismo.

2. Se instala nfs-common, docker y docker-compose. Para esto, se ejecutan los siguientes comandos:
```
sudo apt update
sudo apt install nfs-common -y
sudo apt install docker.io -y
sudo apt install docker-compose -y
```

3. Ingresamos al archivo /etc/fstab:
```
sudo nano /etc/fstab
```
Agregamos el siguiente comando al archivo, teniendo en cuenta que la dirección IP es la correspondiente a la instancia asignada al servidor NFS:
```
10.128.0.58:/mnt/nfs_share /var/www/html nfs auto 0 0
```

4. Para conectar el Wordpress al servidor NFS se crea el directorio donde se compartirán los archivos:
```
sudo mkdir -p /mnt/nfs_clientshare
```
Luego, se ejecuta el siguiente comando, teniendo en cuenta que la dirección IP es la correspondiente a la instancia asignada al servidor NFS:
```
sudo mount 10.128.0.58:/mnt/nfs_share /mnt/nfs_clientshare
```

5. Para verificar que la conexión funciona desde la instancia del servidor NFS se ejecutan los siguientes comandos:
```
cd /mnt/nfs_share/
sudo touch sample1.text sample2.text
```
Luego, se regresa a la instancia del Wordpress y se ejecuta el siguiente comando:
```
ls -l /mnt/nfs_clientshare/
```
El resultado es el siguiente:  
![8](https://user-images.githubusercontent.com/37346028/197872967-8356a2f1-b33d-4c84-8a80-fd8b1628b2a4.PNG)
![9](https://user-images.githubusercontent.com/37346028/197872992-db75f212-7170-449d-96b5-c306f0deaad5.PNG)

6. Ponemos a funcionar docker:
```
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker asarangog
sudo reboot
```

7. Creamos un directorio para el docker container y accedemos a este:
```
mkdir docker
cd docker
```

8. Creamos un archivo docker-compose.yaml e ingresamos a este:
```
sudo touch docker-compose.yaml
sudo nano docker-compose.yaml
```
Agregamos el siguiente contenido al archivo, teniendo en cuenta que la dirección IP es la correspondiente a la instancia asignada al servidor de base de datos y el usuario, la contraseña y el nombre de la base de datos son los creados anteriormente:
```
version: '3.7'
services:
  wordpress:
    container_name: wordpress
    image: wordpress:latest
    restart: always
    environment:
      WORDPRESS_DB_HOST: 10.128.0.59:3306
      WORDPRESS_DB_USER: asarangog
      WORDPRESS_DB_PASSWORD: 1234
      WORDPRESS_DB_NAME: wpdb
    volumes:
      - /var/www/html:/var/www/html
    ports:
      - 80:80
volumes:
  wordpress:
```

9. Ponemos a funcionar el contenedor con el siguiente comando:
```
sudo docker-compose up --build -d
```

## Detalles técnicos
Se usó GCP para desplegar las máquinas virtuales.  
Se usaron contenedores de Docker.  
Se usó Cerbot y Let's Encrypt para asignar un certificado SSL válido.  
Se usó Nginx como servidor web HTTP.  
Se usó NFS kernel server para hacer el servidor NFS.

## Resultados o pantallazos 
Resultados y obtención del certificado SSL válido. 

![5](https://user-images.githubusercontent.com/37346028/197877880-1dc3fa29-f3ec-4784-b0df-64f9e8bc2c43.PNG)
![6](https://user-images.githubusercontent.com/37346028/197877907-af064330-1999-4f27-aebb-ed4b453eeaca.PNG)

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Docker, Nginx y MySQL.

# IP o nombres de dominio en nube o en la máquina servidor.
IP elástica de la máquina servidor del Wordpress 1: 34.135.73.96  
IP elástica de la máquina servidor del Wordpress 2: 35.202.39.170  
IP elástica de la máquina servidor del NFS: 34.171.49.44  
IP elástica de la máquina servidor de la base de datos: 34.72.7.237  
IP elástica de la máquina servidor del balanceador de cargas: 34.70.26.201  
Nombre de dominio: asarangog.tk  
Dominio con certificación ssl: https://lab4.asarangog.tk

## Una mini guia de como un usuario utilizaría el software o la aplicación
El usuario puede acceder desde cualquier navegador al link https://lab4.asarangog.tk y disfrutar de la aplicación.

# Referencias:
## https://github.com/st0263eafit/st0263-2022-2.git 
## https://www.youtube.com/watch?v=N3xWxZt8x2s
## https://www.serverlab.ca/tutorials/linux/web-servers-linux/how-to-scale-wordpress-sites-using-nfs/
## https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/How-to-setup-an-Nginx-load-balancer-example
## https://www.letscloud.io/community/how-to-set-up-an-nginx-with-certbot-on-ubuntu
## https://geekrewind.com/setup-lets-encrypt-wildcard-on-ubuntu-20-04-18-04/
## https://linuxhint.com/install-and-configure-nfs-server-ubuntu-22-04/

#### versión README.md -> 1.0 (2022-octubre)