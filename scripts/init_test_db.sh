#!/bin/bash
set -e

echo "Inicializando base de datos de test..."

# Create test database
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
        cursor.execute(f'DROP DATABASE IF EXISTS {DB_TEST_NAME}')
        cursor.execute(f'CREATE DATABASE {DB_TEST_NAME}')
    conn.commit()
    print(f'Base de datos {DB_TEST_NAME} recreada')
finally:
    conn.close()
"

# Create tables directly from models (no migrations needed for tests)
cd /app
export SQLALCHEMY_DATABASE_URI="mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:3306/${DB_TEST_NAME}"
python3 -c "
from app import create_app
from app.core.extensions import db
app = create_app('test')
with app.app_context():
    db.create_all()
    print('Tablas creadas desde los modelos')
"

# Seed the database
python3 -c "
from app import create_app
from app.core.extensions import db
app = create_app('test')
with app.app_context():
    from app.api.statusOffers.seeds import seed_offer_status
    from app.api.propertyStatus.seeds import seed_property_statuses
    seed_offer_status()
    seed_property_statuses()
    print('Seeds ejecutados correctamente')
"