# Historia de Usuario

## ID

HU-003

## Título

Gestión de preferencias de clientes

## Descripción

**Como** agente inmobiliario

**Quiero** registrar y gestionar las preferencias de un cliente

**Para** ofrecerle propiedades adecuadas a sus intereses

---

## Criterios de Aceptación

### Escenario 1: Registrar preferencias

```gherkin
Dado que existe un cliente
Cuando se realiza POST /clients/{id}/preferences
Entonces el sistema guarda las preferencias
Y retorna 201
```

### Escenario 2: Consultar preferencias

```gherkin
Dado que un cliente tiene preferencias
Cuando se realiza GET /clients/{id}/preferences
Entonces el sistema retorna las preferencias
```

### Escenario 3: Actualizar preferencias

```gherkin
Dado que existen preferencias
Cuando se realiza PUT /clients/{id}/preferences
Entonces el sistema actualiza los datos
Y retorna 200
```

### Escenario 4: Validación de datos

```gherkin
Dado que los datos son inválidos
Cuando se intenta guardar preferencias
Entonces el sistema retorna 400
```

---

## Notas

* Depende de HU-002
* Relación 1:N (cliente → preferencias)
* Campos:

  * Property type
  * Price range
  * Location
  * Number of bedrooms
  * Number of bathrooms
  * Additional features
  * living space range


---

## Estimación

3 puntos

## Prioridad

Media

---

## Tareas

| Código | Nombre                                  | Responsable |
| :----- | :-------------------------------------- | :---------- |
| T1     | Modelo `Preference`                     | Backend     |
| T2     | Relación Client–Preference              | Backend     |
| T3     | Endpoint POST /clients/{id}/preferences | Backend     |
| T4     | Endpoint GET /clients/{id}/preferences  | Backend     |
| T5     | Endpoint PUT /clients/{id}/preferences  | Backend     |
| T6     | Validaciones                            | Backend     |
| T7     | Testing                                 | QA          |
| T8     | Documentación API                       | Backend     |

