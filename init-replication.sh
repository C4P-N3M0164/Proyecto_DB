#!/bin/bash

# Esperar a que MySQL esté listo
until mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT 1" >/dev/null 2>&1; do
  echo "Esperando a que MySQL esté listo..."
  sleep 1
done

# Crear usuario para replicación
mysql -u root -p"$MYSQL_ROOT_PASSWORD" << EOF
CREATE USER 'repl'@'%' IDENTIFIED BY 'repl_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%';
FLUSH PRIVILEGES;
EOF

# Si es el slave, configurar la replicación
if [ "$MYSQL_SERVER_ID" = "2" ]; then
  # Esperar a que el master esté listo
  until mysql -h mysql-master -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT 1" >/dev/null 2>&1; do
    echo "Esperando a que el master esté listo..."
    sleep 1
  done

  # Obtener la posición del binlog del master
  MASTER_STATUS=$(mysql -h mysql-master -u root -p"$MYSQL_ROOT_PASSWORD" -e "SHOW MASTER STATUS\G")
  MASTER_LOG_FILE=$(echo "$MASTER_STATUS" | grep "File:" | awk '{print $2}')
  MASTER_LOG_POS=$(echo "$MASTER_STATUS" | grep "Position:" | awk '{print $2}')

  # Configurar el slave
  mysql -u root -p"$MYSQL_ROOT_PASSWORD" << EOF
CHANGE MASTER TO
  MASTER_HOST='mysql-master',
  MASTER_USER='repl',
  MASTER_PASSWORD='repl_password',
  MASTER_LOG_FILE='$MASTER_LOG_FILE',
  MASTER_LOG_POS=$MASTER_LOG_POS;
START SLAVE;
EOF
fi 