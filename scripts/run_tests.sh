#!/bin/bash
set -e

COMPOSE_FILE="docker-compose.dev.yaml"
REQUIRED_SERVICES=3
MAX_RETRIES=30
RETRY_INTERVAL=2

echo "=== Test Runner for InmoByte ==="

echo "[1/5] Verificando servicios en ejecución..."
RUNNING=$(docker compose -f $COMPOSE_FILE ps --services --filter "status=running" 2>/dev/null | wc -l)

if [ "$RUNNING" -lt "$REQUIRED_SERVICES" ]; then
    echo "[2/5] Levantando contenedores (servicios no están completos: $RUNNING/$REQUIRED_SERVICES)..."
    docker compose -f $COMPOSE_FILE up --force-recreate --build
    echo "     Esperando a MariaDB..."
    sleep 5
else
    echo "[2/5] Contenedores ya están corriendo ($RUNNING/$REQUIRED_SERVICES)"
fi

echo "[3/5] Verificando/Creando base de datos de test..."
docker compose -f $COMPOSE_FILE exec -T backend bash -c "chmod +x /app/scripts/init_test_db.sh && /app/scripts/init_test_db.sh"

echo "[4/5] Ejecutando tests..."
docker compose -f $COMPOSE_FILE exec -T -w /app backend bash -c "PYTHONPATH=/app pytest tests/ -v"

echo ""
echo "=== Tests completados ==="