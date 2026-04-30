#!/bin/bash
set -e

COMPOSE_FILE="docker-compose.dev.yaml"
REQUIRED_SERVICES=3
MAX_RETRIES=30
RETRY_INTERVAL=2

echo "=== InmoByte Demo Data Seeder ==="

echo "[1/3] Verificando servicios en ejecución..."
RUNNING=$(docker compose -f $COMPOSE_FILE ps --services --filter "status=running" 2>/dev/null | wc -l)

if [ "$RUNNING" -lt "$REQUIRED_SERVICES" ]; then
    echo "[2/3] Servicios no están corriendo completamente ($RUNNING/$REQUIRED_SERVICES). Levantando servicios..."
    docker compose -f $COMPOSE_FILE up -d --force-recreate --build
    
    echo "     Esperando a que los servicios estén listos..."
    for i in $(seq 1 $MAX_RETRIES); do
        RUNNING=$(docker compose -f $COMPOSE_FILE ps --services --filter "status=running" 2>/dev/null | wc -l)
        if [ "$RUNNING" -ge "$REQUIRED_SERVICES" ]; then
            echo "     Servicios listos ($RUNNING/$REQUIRED_SERVICES)"
            break
        fi
        echo "     Esperando... ($i/$MAX_RETRIES)"
        sleep $RETRY_INTERVAL
    done
    
    echo "     Esperando a que MariaDB esté saludable..."
    sleep 5
else
    echo "[2/3] Contenedores ya están corriendo ($RUNNING/$REQUIRED_SERVICES)"
fi

echo "[3/3] Ejecutando seeder dentro del contenedor backend..."
docker compose -f $COMPOSE_FILE exec -T -w /app backend bash -c "PYTHONPATH=/app python scripts/seed_demo_data.py"

echo ""
echo "=== Datos de demo insertados exitosamente ==="
