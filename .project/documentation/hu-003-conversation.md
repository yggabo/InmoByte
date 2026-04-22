# HU-003 - Gestión de preferencias de clientes

## Fecha: Wed Apr 22 2026

---

## Resumen de la conversación

**Usuario inicial:** Implementar HU-003, generar archivos en app/api/preferences siguiendo el esquema de modelos rutas y servicios. Si son necesarios datos de otras tablas simúlalos.

---

## Decisiones tomadas

| # | Decisión | Detalle |
|---|----------|---------|
| 1 | Estructura de archivos | `app/api/preferences/` con `__init__.py`, `models.py`, `services.py`, `routes.py` |
| 2 | Modelo `Preference` | Separar `price_range` → `price_min`, `price_max` |
| 3 | Modelo `Preference` | Separar `living_space_range` → `living_space_min`, `living_space_max` |
| 4 | Campo `property_type` | Almacena ID (`property_type_id`) que relaciona con otra tabla |
| 5 | FK simuladas | Client y PropertyType se implementarán después |
| 6 | Campo `additional_features` | Usar tipo JSON de MariaDB |

---

## Modelo final `Preference`

| Campo | Tipo | Notas |
|-------|------|-------|
| id | Integer | PK |
| client_id | Integer | FK simulada (Client) |
| property_type_id | Integer | FK simulada (property_types) |
| price_min | Float | Precio mínimo |
| price_max | Float | Precio máximo |
| location | String(100) | Ubicación |
| bedrooms | Integer | Número de habitaciones |
| bathrooms | Integer | Número de baños |
| additional_features | JSON | Características adicionales |
| living_space_min | Float | Superficie mínima |
| living_space_max | Float | Superficie máxima |
| created_at | DateTime | Fecha creación |
| updated_at | DateTime | Fecha actualización |

---

## Endpoints

| Método | Endpoint | Código | Descripción |
|--------|----------|--------|-------------|
| POST | `/clients/{id}/preferences` | 201 | Crear preferencias |
| GET | `/clients/{id}/preferences` | 200 | Consultar preferencias |
| PUT | `/clients/{id}/preferences` | 200 | Actualizar preferencias |

---

## JSON request ejemplo

```json
{
  "property_type_id": 1,
  "price_min": 150000,
  "price_max": 300000,
  "location": "Zona Centro",
  "bedrooms": 2,
  "bathrooms": 1,
  "additional_features": {"pool": true, "garage": false},
  "living_space_min": 60,
  "living_space_max": 100
}
```

---

## Archivos creados

- `app/api/preferences/__init__.py`
- `app/api/preferences/models.py`
- `app/api/preferences/services.py`
- `app/api/preferences/routes.py`

## Archivos modificados

- `app/api/__init__.py` - Registrado blueprint
- `app/core/models.py` - Importado modelo

---

## Notas adicionales

- MariaDB soporta tipo JSON desde versión 10.2.7
- El modelo Client será implementado por otro desarrollador
- La tabla property_types será implementada posteriormente
- Código en inglés según convenciones del proyecto
- JWT requerido para todos los endpoints