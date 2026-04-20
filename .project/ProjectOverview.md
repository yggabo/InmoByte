# Project Overview - InmoByte - Sistema de gestion de inmobiliaria

## 1. Visión del Proyecto
En InmoByte, el vendedor acude a la inmobiliaria y un agente gestiona su propiedad y los clientes interesados. Se realizan visitas y seguimiento hasta cerrar la operación de venta o alquiler.
En InmoByte, el proceso comienza cuando el vendedor acude a la inmobiliaria para poner su propiedad en venta; un agente se encarga de asesorarle, registrar el inmueble y gestionar clientes interesados. A partir de ahí, se organizan visitas y se realiza el seguimiento hasta encontrar comprador. Finalmente, la operación se cierra con la formalización de la venta o alquiler, quedando registrada como transacción completada.

## 2. Especificaciones Técnicas (Stack Tecnológico)
Siguiendo los requerimientos del documento guía, el proyecto se construirá con:

- **Backend:** python flask - API REST.
- **ORM:** SQLalchemy.
- **Enrutado:** blueprints
- **Calidad de Código:** Testing con pytest, unitarios, feature, integracion.
- **Diseño:** estructura por funcionalidad.

## 3. Arquitectura de Datos y Componentes
Se aplicará la filosofía clean y Modularización.

### Funcionalidades Core:
- **Gestionar propiedades:** Segumiento de propiedades desde que se registra, se agendan visitas, se confirman visitas completadas, se registran propuestas por parte de los clientes, se cambia el estatus.
- **Gestión de clientes (CRUD):** listar, agregar, editar y eliminar registros de clientes.
- **Gestión de propiedades (CRUD):** listar, agregar, editar y eliminar registros de propiedades.
- **Gestión de preferencias de clientes (CRUD):** listar, agregar, editar y eliminar registros de preferencias de clientes.
- **filtrar propiedades:** filtrar propiedades por mutiples campos y preferencias del cliente.

## 4. Organización del Equipo (Metodología Agile)
- **Framework:** SCRUM con sprints de 2 semanas.
- **Roles:** 1 Scrum Master, 1 product owner y 2 Developers (equipo autónomo de 4).
- **Ceremonias:** 
  - Daily cada 2 días con el Product Owner.
  - Sprint Review final con demo técnica y funcional (45 min).
- **Herramientas:** Trello para el tablero Kanban y GitHub para control de versiones (flujo de ramas main, developer, feature).

## 5. Criterios de Éxito y Calidad
- **Naming:** Todo el código (variables, funciones, comentarios) estrictamente en inglés.
- **Accesibilidad:** Cumplimiento de estándares de legibilidad codigo de error y mensaje claro.
- **Despliegue:** Docker orquestar BD MariaDB y backend python flask.
