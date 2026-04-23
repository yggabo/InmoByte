#!/bin/bash
set -e

COMPOSE_FILE="docker-compose.dev.yaml"
REQUIRED_SERVICES=3
MAX_RETRIES=30
RETRY_INTERVAL=2

echo "=== Test Runner for InmoByte ==="

echo "[1/4] Verificando servicios en ejecución..."
RUNNING=$(docker compose -f $COMPOSE_FILE ps --services --filter "status=running" 2>/dev/null | wc -l)

if [ "$RUNNING" -lt "$REQUIRED_SERVICES" ]; then
    echo "[2/4] Levantando contenedores (servicios no están completos: $RUNNING/$REQUIRED_SERVICES)..."
    docker compose -f $COMPOSE_FILE up --force-recreate --build
    echo "     Esperando a MariaDB..."
    sleep 5
else
    echo "[2/4] Contenedores ya están corriendo ($RUNNING/$REQUIRED_SERVICES)"
fi

echo "[3/4] Verificando que backend esté disponible..."
COUNTER=0
STATUS=$(docker compose -f $COMPOSE_FILE ps backend --format "{{.Status}}" 2>/dev/null)
until echo "$STATUS" | grep -q "Up"; do
    COUNTER=$((COUNTER + 1))
    if [ "$COUNTER" -ge "$MAX_RETRIES" ]; then
        echo "     ERROR: Backend no disponible después de $MAX_RETRIES intentos"
        exit 1
    fi
    echo "     Esperando backend... (intento $COUNTER/$MAX_RETRIES)"
    sleep $RETRY_INTERVAL
    STATUS=$(docker compose -f $COMPOSE_FILE ps backend --format "{{.Status}}" 2>/dev/null)
done
echo "     Backend disponible"

echo "[4/4] Ejecutando tests..."
docker compose -f $COMPOSE_FILE exec -T -w /app backend bash -c "PYTHONPATH=/app pytest tests/ -v"

echo ""
echo "=== Tests completados ==="