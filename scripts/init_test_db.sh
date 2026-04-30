#!/bin/bash
set -e

echo "Inicializando base de datos de test..."

# Create test database using Python script
python3 /app/scripts/init_test_db.py

# Create tables directly from models (no migrations needed for tests)
cd /app
export SQLALCHEMY_DATABASE_URI="mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:3306/${DB_TEST_NAME}"
python3 -c "
from app import create_app
from app.core.extensions import db
app = create_app('test')
with app.app_context():
    db.create_all()
    print('Tables created from models')
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
    print('Seeds executed successfully')
"
