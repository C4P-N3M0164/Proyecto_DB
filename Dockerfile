# Usa la imagen oficial de MySQL
FROM mysql:8.0

# Copia los scripts de inicialización
COPY init-db/ /docker-entrypoint-initdb.d/
