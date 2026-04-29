# Swagger Implementation - HU-005

## Date: Fri Apr 24 2026

---

## Summary

Implementation of Swagger/OpenAPI documentation for the Offers endpoints (HU-005).

---

## Decisions Made

| # | Decision | Detail |
|---|----------|---------|
| 1 | Library | flasgger (Flask wrapper for Swagger-UI) |
| 2 | Version | 0.9.7.2.dev2 (already configured) |
| 3 | Format | YAML docstrings in route functions |
| 4 | Status | Uses FK to offer_status table |

---

## Implementation Details

### Files Modified

| File | Change |
|------|-------|
| `app/api/offers/routes.py` | Added Swagger docstrings to 3 endpoints |
| `app/api/offers/models.py` | Added status_id FK to OfferStatus |
| `app/api/offers/services.py` | Uses status_id integers |
| `app/api/offers/schemas.py` | Uses status_id for updates |
| `app/api/roles/seeds.py` | Added seed_offer_status() |

### Documentation Format

```python
@bp.route("/endpoint", methods=["METHOD"])
def handler():
    """
    Description
    ---
    tags:
      - TagName
    summary: Short summary
    description: Detailed description
    parameters:
      - name: param_name
        in: path|body|query
        required: true|false
        schema:
          type: type
    responses:
      200:
        description: Success
      400:
        description: Bad request
      404:
        description: Not found
    """
```

---

## Documented Endpoints

### 1. POST /offers

- **Summary:** Create a new offer
- **Tags:** Offers
- **Request Body:**
  - type (string, required): COMPRA or ALQUILER
  - offered_price (number, required)
  - property_id (integer, required)
  - client_id (integer, required)
  - agent_id (integer, optional)
- **Responses:**
  - 201: Created
  - 400: Invalid data
  - 409: Property not available
  - 500: Server error

### 2. GET /properties/{id}/offers

- **Summary:** Get property offers
- **Tags:** Offers
- **Parameters:**
  - property_id (integer, path)
- **Responses:**
  - 200: List of offers
  - 404: Property not found

### 3. PATCH /offers/{id}/status

- **Summary:** Update offer status
- **Tags:** Offers
- **Parameters:**
  - offer_id (integer, path)
  - status_id (integer, body): 2 (ACEPTADA), 3 (RECHAZADA), or 4 (CANCELADA)
- **Responses:**
  - 200: Updated
  - 400: Invalid data
  - 404: Offer not found
  - 500: Server error

---

## Database Schema

### Tables

| Table | Description |
|------|-------------|
| `offer_status` | Status lookup (PENDIENTE, ACEPTADA, RECHAZADA, CANCELADA) |
| `offer_type` | Type lookup (COMPRA, ALQUILER) |
| `offers` | Main offer table with FK to offer_status |

### offer_status seeds

| id | name |
|----|------|
| 1 | PENDIENTE |
| 2 | ACEPTADA |
| 3 | RECHAZADA |
| 4 | CANCELADA |

---

## Access

- **Swagger UI:** `http://localhost:7070/apidocs/`
- **JSON Spec:** `http://localhost:7070/apidocs/swagger.json`

---

## Verification

All files verified syntactically:

| File | Status |
|------|--------|
| routes.py | Syntax OK |
| models.py | Syntax OK |
| services.py | Syntax OK |
| schemas.py | Syntax OK |

---

## Notes

- All endpoints follow the existing pattern from preferences/routes.py
- Documentation uses Flasgger YAML format
- Status uses integer FK (status_id) instead of string