# Historia de Usuario

## ID

HU-005

## Título

Gestión de ofertas de compra y alquiler

## Descripción

**Como** agente inmobiliario
**Quiero** registrar y gestionar ofertas de compra y alquiler de propiedades
**Para** darle seguimiento a las oportunidades de negocio y cerrar transacciones

## Criterios de Aceptación

### Escenario 1: Registrar oferta de compra

```gherkin
Dado un cliente comprador y una propiedad en estado DISPONIBLE o ASIGNADA
Cuando se realiza POST /offers con type=COMPRA y offered_price
Entonces:
  La API responde con 201 Created
  La oferta queda registrada con estado PENDIENTE
```

### Escenario 2: Registrar oferta de alquiler

```gherkin
Dado un cliente inquilino y una propiedad en estado DISPONIBLE o ASIGNADA
Cuando se realiza POST /offers con type=ALQUILER y offered_price
Entonces:
  La API responde con 201 Created
  La oferta queda registrada con estado PENDIENTE
```

### Escenario 3: Validar propiedad disponible para oferta

```gherkin
Dado una propiedad en estado VENDIDA o ALQUILADA
Cuando se intenta crear una oferta
Entonces:
  La API responde con 409 Conflict
  Se informa que la propiedad no está disponible
```

### Escenario 4: Consultar ofertas por propiedad

```gherkin
Dado una propiedad con ofertas registradas
Cuando se realiza GET /properties/{id}/offers
Entonces:
  La API retorna lista de ofertas con datos completos
```

### Escenario 5: Aceptar oferta de compra (cambia propiedad a VENDIDA)

```gherkin
Dado una oferta de compra en estado PENDIENTE
Cuando se realiza PATCH /offers/{id}/status con estado ACEPTADA
Entonces:
  La API responde con 200 OK
  La oferta cambia a estado ACEPTADA
  La propiedad asociada cambia a estado VENDIDA
```

### Escenario 6: Aceptar oferta de alquiler (cambia propiedad a ALQUILADA)

```gherkin
Dado una oferta de alquiler en estado PENDIENTE
Cuando se realiza PATCH /offers/{id}/status con estado ACEPTADA
Entonces:
  La API responde con 200 OK
  La oferta cambia a estado ACEPTADA
  La propiedad asociada cambia a estado ALQUILADA
```

### Escenario 7: Rechazar o cancelar oferta

```gherkin
Dado una oferta en estado PENDIENTE
Cuando se realiza PATCH /offers/{id}/status con estado RECHAZADA o CANCELADA
Entonces:
  La API responde con 200 OK
  La oferta cambia al nuevo estado
  La propiedad mantiene su estado actual
```

## Notas

* Relación N:1 (offer → property)
* Relación N:1 (offer → client)
* Relación N:1 (offer → agent)
* Solo propiedades en estado DISPONIBLE o ASIGNADA aceptan ofertas
* Cambio de estado automático al aceptar oferta:
  * COMPRA aceptada → propiedad: VENDIDA
  * ALQUILER aceptada → propiedad: ALQUILADA
* Campos:
  * id
  * type (COMPRA | ALQUILER)
  * offered_price
  * status (PENDIENTE | ACEPTADA | RECHAZADA | CANCELADA)
  * property_id
  * client_id
  * agent_id
  * created_at
  * updated_at

## Estimación

5 puntos

## Prioridad

Alta

## Tareas

| Código | Nombre | Responsable |
|:-------|:-------|:-----------|
| HU-005-01 |Modelo Offer | Backend |
| HU-005-02 |Endpoint POST /offers | Backend |
| HU-005-03 |Endpoint GET /properties/{id}/offers | Backend |
| HU-005-04 |Endpoint PATCH /offers/{id}/status | Backend |
| HU-005-05 |Validación de estado de propiedad | Backend |
| HU-005-06 |Lógica de cambio de estado automático | Backend |
| HU-005-07 |Testing | QA |