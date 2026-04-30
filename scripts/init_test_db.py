#!/usr/bin/env python3
"""Initialize test database with proper permissions."""
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
            user='root',
            password=DB_PASSWORD,
            connect_timeout=5
        )
        print(f'Connected to MariaDB (attempt {attempt + 1})')
        break
    except pymysql.Error as e:
        print(f'Waiting for MariaDB... (attempt {attempt + 1}/{max_retries})')
        time.sleep(retry_interval)
else:
    print(f'Error: Could not connect to MariaDB after {max_retries} attempts', file=sys.stderr)
    sys.exit(1)

try:
    with conn.cursor() as cursor:
        cursor.execute(f'DROP DATABASE IF EXISTS {DB_TEST_NAME}')
        cursor.execute(f'CREATE DATABASE {DB_TEST_NAME}')
        grant_sql = f"GRANT ALL PRIVILEGES ON {DB_TEST_NAME}.* TO '{DB_USER}'@'%'"
        cursor.execute(grant_sql)
        cursor.execute('FLUSH PRIVILEGES')
    conn.commit()
    print(f'Database {DB_TEST_NAME} recreated and privileges granted')
finally:
    conn.close()
