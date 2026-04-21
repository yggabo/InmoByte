# Historia de Usuario

## ID

HU-001

## Título

Registrar y asignar propiedad

## Descripción

**Como** agente inmobiliario
**Quiero** registrar propiedades de vendedores y asignarlas a un agente
**Para** poder gestionarlas y comercializarlas mediante la API

## Criterios de Aceptación

### Escenario 1: Registro de inmueble

```gherkin
Dado un vendedor existente
Cuando se realiza una petición POST /properties con datos válidos
Entonces:
  La API responde con 201 Created
  La propiedad queda registrada
  Su estado es DISPONIBLE
```

### Escenario 2: Validación de datos

```gherkin
Dado una petición de creación de propiedad
Cuando los datos son inválidos o incompletos
Entonces:
  La API responde con 400 Bad Request
  Se devuelve el detalle de los errores
```

### Escenario 3: Asignación de agente

```gherkin
Dado una propiedad registrada
Cuando se realiza una petición PATCH /properties/{id}/assign-agent
Entonces:
  La API responde con 200 OK
  El agente queda asignado como responsable
```

### Escenario 4: Propiedad no asignable

```gherkin
Dado una propiedad no disponible (ej. VENDIDA)
Cuando se intenta asignar un agente
Entonces:
  La API responde con 409 Conflict
  Se informa que la propiedad no puede asignarse
```

## Notas
* Relación 1:N (cliente → propiedades)
* Relación 1:N (status → propiedades)
* Relación 1:N (agente → propiedades)
- Campos mínimos: price, location, meters2, type, statusId, clientId, agentId
- Una propiedad pertenece a un vendedor
- Una propiedad tiene un único agente activo
- Estados: DISPONIBLE, ASIGNADA, VENDIDA, ALQUILADA

## Estimación

5 puntos

## Prioridad

Alta

## Tareas

| Código | Nombre | Responsable |
|--------|--------|-------------|
| HU-001-01 | Endpoint POST /properties | - |
| HU-001-02 | Validaciones de entrada | - |
| HU-001-03 | Endpoint PATCH asignación de agente | - |
| HU-001-04 | Gestión de estados | - |
| HU-001-05 | Tests de API | - |
