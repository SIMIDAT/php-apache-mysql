Los ficheros que posibilitan la captura y almacenamiento de datos, así como poder visualizarlos y descargarlos a través de la aplicación web se encuentran en el directorio home/gquesada/php-apache-mysql del servidor simidat-apps.ujaen.es. En él se encuentran los archivos:


•	_env: con variables de entorno.

•	docker-compose.yml: archivo que define servicios, redes y volúmenes.

•	predicciones.sql: copia de seguridad de la base de datos.

•	sudo.sh: fichero llamado por el crontab cada tres horas que activa el servicio Docker de captura y almacenamiento de datos, descarga los datos en bruto y realiza la copia de seguridad de la base de datos.


También se encuentran los directorios: apache, app, public_html.

a)	apache


Contiene los ficheros:


•	demo.apache.conf: archivo de configuración de apache.

•	Dockerfile: descarga e instala php y apache en el Docker.



b)	app


Presenta el directorio Brutos con los datos en formato JSON descargados de las distintas fuentes de datos. Además, presenta los siguientes ficheros:


•	DescargaACCUWEATHER: captura y almacena los datos de Accuweather.

•	DescargaAEMET: captura y almacena los datos de AEMET.

•	DescargaOPENWEATHERMAP: captura y almacena los datos de OpenWeatherMap.

•	DescargaTIEMPO: captura y almacena los datos de Tiempo.com.

•	Dockerfile: descarga e instala Python, descarga las librerías que aparecen especificadas en requeriments y ejecuta los archivos anteriores.

•	requirements: librerías necesarias para poder ejecutar los scripts de Python anteriores.



c)	public_html


En él se encuentra la carpeta assets con todos los recursos css, imágenes, archivos de JavaScript, etc. También se encuentran tres archivos php:


•	index.php: interfaz principal de la web con el formulario de selección de la fuente, las variables, fechas, horizontes de predicción y botones de descarga y visualización.

•	descarga.php: código para el acceso a la base de datos con la consulta formada a partir del formulario anterior y descarga de los datos en .csv.

•	visualizacion.php: scripts que accede a la base de datos y muestra en una tabla los datos que concuerdan con los parámetros seleccionados en el formulario.
