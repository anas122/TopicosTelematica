# Info de la materia: ST0263 Tópicos Especiales en Telemática
#
# Estudiante(s): Ana Sofia Arango Gonzalez, asarangog@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# Laboratorio 6
#
# 1. Breve descripción de la actividad
Manejo de 'pyspark' y JupyterHub Notebooks en EMR con datos en HDFS y S3 usando un clúster vía ssh en el nodo master.

## 1.1. Qué aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Ejecutar el wordcount por línea de comando 'pyspark' INTERACTIVO en EMR con datos en HDFS vía ssh en el nodo master.  
Ejecutar el wordcount por línea de comando 'pyspark' INTERACTIVO en EMR con datos en S3 (tanto de entrada como de salida) vía ssh en el nodo master.  
Ejecutar el wordcount en JupyterHub Notebooks EMR con datos en S3 (tanto datos de entrada como de salida) usando un clúster EMR.  
Replique, ejecute y entienda el notebook Data_processing_using_PySpark.ipynb con los datos respectivos y ejecutelo en AWS EMR.  
Gestionar datos vía SQL con HIVE y SparkSQL.

## 1.2. Qué aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Todos los aspectos se cumplieron y desarrollaron.

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se utilizaron los servicios de EMR y S3 en AWS. También HUE y JupyterHub Notebooks.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
EMR en AWS  
S3 en AWS  
HUE, Hive, SparkSQL  
JupyterHub Notebooks, pyspark

## Detalles del desarrollo.
1. Creamos un clúster en el servicio EMR de AWS.

2. Creamos un bucket en el servicio S3 de AWS asociado al clúster creado anteriormente.

3. Nos conectamos al nodo master del clúster vía ssh.

4. Para comenzar se ejecuta el siguiente comando:
```
sudo yum install git -y
```

5. Clonamos el repositorio de donde se cargarán los datasets en el nodo:
```
git clone https://github.com/st0263eafit/st0263-2022-2.git
```

6. Creamos la carpeta /user/hadoop/datasets en Hue con hdfs:
```
hdfs dfs -mkdir /user/hadoop/datasets
```

7. Copiamos los datasets en Hue con hdfs:
```
hdfs dfs -copyFromLocal st0263-2022-2/bigdata/datasets/* /user/hadoop/datasets
```
![1](https://user-images.githubusercontent.com/37346028/204039247-8245d990-6dee-4e7f-a708-b24165b3c671.PNG)

### Ejecutar el wordcount por línea de comando 'pyspark' INTERACTIVO en EMR con datos en HDFS vía ssh en el nodo master
1. Para ejecutar el wordcount se accede a pyspark con el siguiente comando:
```
pyspark
```

2. Una vez se accede a pyspark se ejecutan los siguientes comandos:
```
>>> files_rdd = sc.textFile("hdfs:///user/hadoop/datasets/gutenberg-small/*.txt")
>>> wc_unsort = files_rdd.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
>>> wc = wc_unsort.sortBy(lambda a: -a[1])
>>> for tupla in wc.take(10):
...  print(tupla)
...
```

3. Se guardan los datos de salida con hdfs:
```
>>> wc.saveAsTextFile("hdfs:///tmp/wcout1")
>>> exit()
```

4. Verificamos que los datos de salida hayan quedado guardados:
```
hdfs dfs -ls /tmp
```
![2](https://user-images.githubusercontent.com/37346028/204039249-c95dc68d-96ec-4778-8802-aec6049df154.PNG)

```
hdfs dfs -ls /tmp/wcout1
```
![3](https://user-images.githubusercontent.com/37346028/204039251-60020b79-1e57-4250-bb4e-85881b8ba466.PNG)

### Ejecutar el wordcount por línea de comando 'pyspark' INTERACTIVO en EMR con datos en S3 (tanto de entrada como de salida) vía ssh en el nodo master
1. Cargamos los datasets en el bucket creado anteriormente.
![4](https://user-images.githubusercontent.com/37346028/204039253-e315f1a0-881d-466c-8352-1f3c578211d5.PNG)

2. Para ejecutar el wordcount se accede a pyspark con el siguiente comando:
```
pyspark
```

3. Una vez se accede a pyspark se ejecutan los siguientes comandos:
```
>>> files_rdd = sc.textFile("s3://lab6asarangog/datasets/gutenberg-small/*.txt")
>>> wc_unsort = files_rdd.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
>>> wc = wc_unsort.sortBy(lambda a: -a[1])
>>> for tupla in wc.take(10):
...  print(tupla)
...
```

4. Se guardan los datos de salida con hdfs y en S3:
```
>>> wc.saveAsTextFile("hdfs:///tmp/wcout2")
>>> wc.saveAsTextFile("s3://lab6asarangog/wcout2")
>>> exit()
```

5. Verificamos que los datos de salida hayan quedado guardados:
```
hdfs dfs -ls /tmp
```
![5](https://user-images.githubusercontent.com/37346028/204039255-059407cd-fcd2-498f-8070-f84622efc5f4.PNG)

```
hdfs dfs -ls /tmp/wcout2
```
![6](https://user-images.githubusercontent.com/37346028/204039257-beb4f436-f711-4461-a02e-825859a7bdb4.PNG)

Igualmente en S3
![7](https://user-images.githubusercontent.com/37346028/204039258-5e533273-95bb-4fd5-ad5f-c9be25e921ad.PNG)

### Ejecutar el wordcount en JupyterHub Notebooks EMR con datos en S3 (tanto datos de entrada como de salida) usando un clúster EMR
1. Se ingresa a JupyterHub desde el link generado por el clúster y se crea un Notebook PySpark.

2. Desde el Notebook se ejecutan los siguientes comandos para correr el wordcount:
```
files_rdd = sc.textFile("s3://lab6asarangog/datasets/gutenberg-small/*.txt")
wc_unsort = files_rdd.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
wc = wc_unsort.sortBy(lambda a: -a[1])
for tupla in wc.take(10):
  print(tupla)
```
![8](https://user-images.githubusercontent.com/37346028/204039259-8850a0b8-a80a-4d4a-9b52-6575a8e9f086.PNG)

3. Se guardan los datos de salida con hdfs y en S3 desde el mismo Notebook:
```
wc.saveAsTextFile("hdfs:///tmp/wcout3")
wc.saveAsTextFile("s3://lab6asarangog/wcout3")
```

4. Verificamos que los datos de salida hayan quedado guardados:
```
hdfs dfs -ls /tmp
```
![9](https://user-images.githubusercontent.com/37346028/204039260-d7f661ba-0830-4754-93d4-00cbbe85fff9.PNG)

```
hdfs dfs -ls /tmp/wcout3
```
![10](https://user-images.githubusercontent.com/37346028/204039263-f603f3cf-28ad-424b-9b11-b7a33c2fe38a.PNG)

Igualmente en S3
![11](https://user-images.githubusercontent.com/37346028/204039267-f3d83d34-68d4-41d6-aade-7fe5dbc7b222.PNG)

### Replique, ejecute y entienda el notebook Data_processing_using_PySpark.ipynb con los datos respectivos y ejecutelo en AWS EMR
1. Se ingresa a JupyterHub desde el link generado por el clúster y se crea un Notebook PySpark.

2. Desde el Notebook se replica paso a paso los pasos del archivo Data_processing_using_PySpark.ipynb que se encuentra en https://github.com/st0263eafit/st0263-2022-2/blob/main/bigdata/03-spark/Data_processing_using_PySpark.ipynb
![12](https://user-images.githubusercontent.com/37346028/204039268-f10f5721-0d82-44a4-a412-4d25f3761750.PNG)
![13](https://user-images.githubusercontent.com/37346028/204039270-69a04ac9-a14c-402e-a7ef-42ff609cd398.PNG)
![14](https://user-images.githubusercontent.com/37346028/204039273-78ed108f-9ede-4826-8d7a-3bcba4c182de.PNG)
![15](https://user-images.githubusercontent.com/37346028/204039275-a3997302-2b44-4b41-b539-c26eeb523bdf.PNG)
![16](https://user-images.githubusercontent.com/37346028/204039276-74c0e979-29bf-4a30-91cf-0ca251c36d05.PNG)
![17](https://user-images.githubusercontent.com/37346028/204039278-f678490d-225a-49c0-bcd8-4ceaf786f26c.PNG)
![18](https://user-images.githubusercontent.com/37346028/204039279-264c4fcd-b031-47e2-b570-4f7219911c84.PNG)
![19](https://user-images.githubusercontent.com/37346028/204039280-f3510083-7023-43ec-b5ce-e4e69bb39959.PNG)
![20](https://user-images.githubusercontent.com/37346028/204039281-efe51c9a-4033-4025-be4e-326b475c1b14.PNG)
![21](https://user-images.githubusercontent.com/37346028/204039284-471f6d78-9d47-4446-a851-5c7a24053c72.PNG)
![22](https://user-images.githubusercontent.com/37346028/204039285-4ba6e538-07d7-4cd3-a591-f343d91202b0.PNG)
![23](https://user-images.githubusercontent.com/37346028/204039287-97d274ab-86b1-4d11-a9a2-9409b04112ee.PNG)
![24](https://user-images.githubusercontent.com/37346028/204039289-3b8a0d79-bde5-44f3-931d-1da090acf853.PNG)
![25](https://user-images.githubusercontent.com/37346028/204039290-31eff3c1-c90b-487b-8cca-26cb8c9af448.PNG)
![26](https://user-images.githubusercontent.com/37346028/204039292-d1dd8fd8-4244-4f46-b000-862afac20a1e.PNG)
![27](https://user-images.githubusercontent.com/37346028/204039293-a98c6236-5378-4895-b5a1-77df53abee4f.PNG)
![28](https://user-images.githubusercontent.com/37346028/204039295-77a7e901-4cdc-4138-a64a-cd410cd23e37.PNG)
![29](https://user-images.githubusercontent.com/37346028/204039297-bfaba3da-bfa4-4147-b4fa-246b44e8950f.PNG)
![30](https://user-images.githubusercontent.com/37346028/204039299-555ecabc-7fa9-4d07-a7c9-942f6047af3a.PNG)

3. Resultados de los dataframe guardados como formato csv y parquet.
![31](https://user-images.githubusercontent.com/37346028/204039301-8811b27b-3163-4ad9-9efe-170205f444f7.PNG)
![32](https://user-images.githubusercontent.com/37346028/204039303-e8b4709b-bdea-4d56-a04d-c47953220d02.PNG)

### Gestionar datos vía SQL con HIVE y SparkSQL
1. Se ingresa a HUE desde el link generado por el clúster y seleccionamos el servicio Hive.

2. Creamos la tabla HDI con los siguientes comandos:
```
CREATE EXTERNAL TABLE HDI (id INT, country STRING, hdi FLOAT, lifeex INT, mysch INT, eysch INT, gni INT) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE 
LOCATION 's3://lab6asarangog/datasets/onu/hdi/';
```
![33](https://user-images.githubusercontent.com/37346028/204039304-095ed9ab-a3bd-444e-bde3-55a1a528bfb4.PNG)

3. Consultamos en la tabla HDI los gni mayores a 2000:
```
show tables;
describe hdi;
select * from hdi;
select country, gni from hdi where gni > 2000;
```
![34](https://user-images.githubusercontent.com/37346028/204039307-e0bbb062-9dfe-4f80-a769-36d00899a709.PNG)

4. Creamos la tabla EXPO con los siguientes comandos:
```
CREATE EXTERNAL TABLE EXPO (country STRING, expct FLOAT) 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE 
LOCATION 's3://lab6asarangog/datasets/onu/export/';
```
![35](https://user-images.githubusercontent.com/37346028/204039313-ab2309ac-2a84-47fb-a4ff-547857f356e2.PNG)

5. Ejecutamos el join de las dos tablas:
```
SELECT h.country, gni, expct FROM HDI h JOIN EXPO e ON (h.country = e.country) WHERE gni > 2000;
```
![36](https://user-images.githubusercontent.com/37346028/204039315-eddd7c8f-2301-4f7a-aa39-0898352b2754.PNG)

6. Creamos una tabla para realizar el wordcount con los siguientes comandos:
```
CREATE EXTERNAL TABLE docs (line STRING) 
STORED AS TEXTFILE 
LOCATION 's3://lab6asarangog/datasets/gutenberg-small/';
```
![37](https://user-images.githubusercontent.com/37346028/204039317-60f60979-c9b0-4429-85d2-e1a8e36e69aa.PNG)

7. Ejecutamos el wordcount ordenado por palabra:
```
SELECT word, count(1) AS count FROM (SELECT explode(split(line,' ')) AS word FROM docs) w 
GROUP BY word 
ORDER BY word DESC LIMIT 10;
```
![38](https://user-images.githubusercontent.com/37346028/204039320-0a972b1f-5aac-4f8d-8346-b99768bd3106.PNG)

8. Ejecutamos el wordcount ordenado por frecuencia de menor a mayor:
```
SELECT word, count(1) AS count FROM (SELECT explode(split(line,' ')) AS word FROM docs) w 
GROUP BY word 
ORDER BY count DESC LIMIT 10;
```
![39](https://user-images.githubusercontent.com/37346028/204039321-1eb1e715-6588-47e3-9c80-81555e6997fe.PNG)

# Referencias:
## https://github.com/st0263eafit/st0263-2022-2/

#### versión README.md -> 1.0 (2022-noviembre)