# Usa la imagen oficial de MySQL
FROM mysql:8.0

# Copia los scripts de inicialización
COPY init-db/ /docker-entrypoint-initdb.d/

# Copia los archivos de configuración
COPY my.cnf /etc/mysql/conf.d/
COPY my-slave.cnf /etc/mysql/conf.d/

# Variables de entorno para la replicación
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=energia

# Puerto para MySQL
EXPOSE 3306

# Script de inicialización para la replicación
# COPY init-replication.sh /docker-entrypoint-initdb.d/
# RUN chmod +x /docker-entrypoint-initdb.d/init-replication.sh
