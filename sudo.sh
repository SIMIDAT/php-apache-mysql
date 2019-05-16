#!/bin/sh
echo emunIt19 | sudo -S docker start -a app
echo emunIt19 | sudo -S docker cp app:/app/Brutos ./php-apache-mysql/app/ 
echo emunIt19 | sudo -S docker exec mariadb /usr/bin/mysqldump --databases -u root --password=$PASSWORD predicciones > ./php-apache-mysql/predicciones.sql
