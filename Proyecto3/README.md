# Info de la materia: ST0263 Tópicos Especiales en Telemática
#
# Estudiante(s): Ana Sofia Arango Gonzalez, asarangog@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# Proyecto 3
#
# 1. Breve descripción de la actividad
Almacenar, cargar y analizar datos con 2 tipos de procesamiento Spark: Dataframes y SparkSQL.

## 1.1. Qué aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Teniendo en cuenta el dataset con datos de ejemplo:  
- Almacenar datos en AWS S3 y en Google Drive (en ambos)
- Cargar datos desde AWS S3 y desde Google Drive
- Análisis exploratorio del dataframe
- Contestar preguntas sobre los datos
- Salvar los datos en un bucket público

## 1.2. Qué aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Todos los aspectos se cumplieron y desarrollaron.

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se utilizó el servicio de S3 en AWS, Google Drive, Google Colab, Spark, PySpark y SparkSQL.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
S3 en AWS  
Google Drive  
Google Colab  
Spark, PySpark y SparkSQL  
openjdk  
os  
findspark  
UDF

## Cómo se compila y ejecuta.
Para ejecutar el Notebook de Google Drive "Proyecto3_asarangog_GoogleDrive.ipynb", se accede a este desde el link https://colab.research.google.com/drive/1sa-U4v2WfL4waqT3FbEQ66BGvfKEmoo2?usp=sharing y se accede a la opción "Entorno de ejecución" y se selecciona la opción "Ejecutar todas".

Para ejecutar el Notebook de AWS S3 "Proyecto3_asarangog_AWS.ipynb", se accede a este desde el link https://colab.research.google.com/drive/16TnFnh58Ynf8b2T_Hyt0IK5kyA31WwlR?usp=sharing y en la línea 3 de configuración se cambian las variables 'fs.s3a.access.key', 'fs.s3a.secret.key' y 'fs.s3a.session.token' por las correspondientes a la sesión activa en AWS, luego se accede a la opción "Entorno de ejecución" y se selecciona la opción "Ejecutar todas".

## Detalles del desarrollo.
- URI datos de entrada en S3: s3://p3asarangog/datasets/
- URI datos de salida en S3: s3://p3asarangog/punto3/
- Datos de entrada en Google Drive: https://drive.google.com/drive/folders/1gwZgkBn6WVRuhec6YFKCQVGvpyMiFKjs?usp=sharing
- Notebook Google Drive: https://colab.research.google.com/drive/1sa-U4v2WfL4waqT3FbEQ66BGvfKEmoo2?usp=sharing
- Notebook AWS S3: https://colab.research.google.com/drive/16TnFnh58Ynf8b2T_Hyt0IK5kyA31WwlR?usp=sharing
## Detalles técnicos
## Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o nombres de dominio en nube o en la máquina servidor.

## Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

## Como se lanza el servidor.

## Una mini guia de como un usuario utilizaría el software o la aplicación

# Referencias:
## https://github.com/st0263eafit/st0263-2022-2/

#### versión README.md -> 1.0 (2022-noviembre)