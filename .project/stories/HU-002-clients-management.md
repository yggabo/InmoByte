# Historia de Usuario

## ID

HU-002

## Título

Gestión de clientes

## Descripción

**Como** agente inmobiliario

**Quiero** registrar y gestionar clientes

**Para** administrar su información y dar seguimiento a oportunidades de negocio

---

## Criterios de Aceptación

### Escenario 1: Registro de cliente

```gherkin
Dado que el agente envía una solicitud válida
Cuando realiza POST /clients con full_name y email
Entonces el sistema guarda el cliente
Y retorna 201
```

### Escenario 2: Validación de duplicados

```gherkin
Dado que ya existe un email registrado
Cuando se intenta crear otro cliente con el mismo email
Entonces el sistema retorna 409
```

### Escenario 3: Consulta de cliente

```gherkin
Dado que existe un cliente
Cuando se realiza GET /clients/{id}
Entonces el sistema retorna 200 con los datos
```

### Escenario 4: Listado de clientes

```gherkin
Dado que existen clientes
Cuando se realiza GET /clients
Entonces el sistema retorna una lista
```

### Escenario 5: Actualización de cliente

```gherkin
Dado que existe un cliente
Cuando se realiza PUT /clients/{id}
Entonces el sistema actualiza los datos
Y retorna 200
```

---

## Notas

* Entidad principal del sistema
* Email único
* Base para otras funcionalidades (ej: preferencias)
* Datos para modelo
    * name 
    * email
    * telephone
    * type 
    * create_at
    * update_at
    * id

---

## Estimación

5 puntos

## Prioridad

Alta

---

## Tareas

| Código | Nombre                     | Responsable |
| :----- | :------------------------- | :---------- |
| T1     | Modelo `Client`            | Backend     |
| T2     | Endpoint POST /clients     | Backend     |
| T3     | Endpoint GET /clients/{id} | Backend     |
| T4     | Endpoint GET /clients      | Backend     |
| T5     | Endpoint PUT /clients/{id} | Backend     |
| T6     | Validaciones y errores     | Backend     |
| T7     | Testing                    | QA          |
| T8     | Documentación API          | Backend     |

