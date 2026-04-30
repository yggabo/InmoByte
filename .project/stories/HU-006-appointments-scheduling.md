# Historia de Usuario

## ID

HU-006

## Título

Agendar y gestionar citas para interesados en propiedades (CRUD)

## Descripción

**Como** agente inmobiliario
**Quiero** realizar un CRUD completo de citas para los clientes interesados en visitar una propiedad
**Para** organizar las visitas de manera eficiente, mantener un historial íntegro mediante borrado lógico y asegurar la consistencia de los estados de las citas

## Criterios de Aceptación

### Escenario 1: Agendar una nueva cita

```gherkin
Dado un cliente interesado y una propiedad disponible
Cuando el agente realiza una petición POST /appointments con fecha, hora, cliente y propiedad
Entonces:
  La API responde con 201 Created
  La cita queda registrada en el sistema con un estado inicial (ej. PROGRAMADA)
  Se asocia la cita al agente responsable de la propiedad
```

### Escenario 2: Validación de disponibilidad (Conflicto de horario)

```gherkin
Dado una cita ya agendada para un agente en un horario específico
Cuando se intenta agendar otra cita para el mismo agente en el mismo horario
Entonces:
  La API responde con 409 Conflict
  Se informa que el agente ya tiene una cita en ese horario
```

### Escenario 3: Edición de una cita existente

```gherkin
Dado una cita registrada previamente
Cuando el agente realiza una petición PUT o PATCH /appointments/{id} con nuevos datos (ej. cambio de fecha o notas)
Entonces:
  La API responde con 200 OK
  Los datos de la cita se actualizan correctamente
```

### Escenario 4: Borrado lógico (Soft Delete) de una cita

```gherkin
Dado una cita registrada
Cuando el agente realiza una petición DELETE /appointments/{id}
Entonces:
  La API responde con 200 OK o 204 No Content
  El registro no se elimina físicamente de la base de datos (is_active: false)
  La cita ya no aparece en los listados activos de la API
```

### Escenario 5: Validación de Estados mediante Tabla Independiente

```gherkin
Dado que los estados de cita están predefinidos en una tabla maestra
Cuando se intenta asignar un estado inexistente o manual
Entonces:
  La API responde con 400 Bad Request
  Solo se permiten estados que existan en la relación con la tabla de estados (FK)
```

### Escenario 6: Listado de citas por propiedad

```gherkin
Dado que existen varias citas agendadas para una propiedad
Cuando se realiza una petición GET /properties/{id}/appointments
Entonces:
  La API responde con 200 OK
  Se devuelve la lista de todas las citas programadas (is_active: true) para esa propiedad
```

## Notas

* **Modelo de Datos:**
    * Relación N:1 (Cita → Propiedad)
    * Relación N:1 (Cita → Cliente)
    * Relación N:1 (Cita → Agente)
    * **Relación N:1 (Cita → AppointmentStatus):** Los estados (PROGRAMADA, REALIZADA, CANCELADA, etc.) residen en su propia tabla para evitar errores de sintaxis y centralizar la gestión.
* **Borrado Lógico:** Incluir un campo booleano `is_active` o `deleted_at` para mantener la integridad referencial y el histórico.
* **Campos mínimos:** appointment_date, start_time, end_time, clientId, propertyId, agentId, statusId, notes, is_active.
* Validar que la propiedad esté en estado DISPONIBLE o ASIGNADA antes de agendar.

## Estimación

10 puntos (debido a la complejidad del CRUD completo y gestión de estados)

## Prioridad

Alta

## Tareas

| Código | Nombre | Responsable |
| :--- | :--- | :--- |
| HU-006-01 | Crear modelo `AppointmentStatus` y semillas (seeds) de estados | Backend |
| HU-006-02 | Crear modelo `Appointment` con soporte para Soft Delete (is_active) | Backend |
| HU-006-03 | Implementar Endpoint POST /appointments (Creación) | Backend |
| HU-006-04 | Implementar lógica de validación de conflictos de horario | Backend |
| HU-006-05 | Implementar Endpoint GET /appointments (Listado con filtros) | Backend |
| HU-006-06 | Implementar Endpoint PUT/PATCH /appointments/{id} (Edición) | Backend |
| HU-006-07 | Implementar Endpoint DELETE /appointments/{id} (Soft Delete) | Backend |
| HU-006-08 | Pruebas de integración para el ciclo de vida completo de la cita | Backend/QA |
| HU-006-09 | Realizar pruebas unitarias e integración con Pytest para validar el CRUD completo | Backend/QA |
