#!/bin/bash
set -e

echo "Inicializando base de datos de test..."

python3 -c "
import os
import sys
import time

import pymysql

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_TEST_NAME = os.environ.get('DB_TEST_NAME')

max_retries = 30
retry_interval = 2

for attempt in range(max_retries):
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=5
        )
        print(f'Conexión exitosa a MariaDB (intento {attempt + 1})')
        break
    except pymysql.Error as e:
        print(f'Esperando MariaDB... (intento {attempt + 1}/{max_retries})')
        time.sleep(retry_interval)
else:
    print(f'Error: No se pudo conectar a MariaDB después de {max_retries} intentos', file=sys.stderr)
    sys.exit(1)

try:
    with conn.cursor() as cursor:
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_TEST_NAME}')
    conn.commit()
    print(f'Base de datos {DB_TEST_NAME} lista')
finally:
    conn.close()
"