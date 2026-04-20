# workflow.md
## Principios

*   **Agilidad y Autonomía:** El equipo trabaja como un grupo autónomo bajo el marco SCRUM.

*    **Calidad Garantizada:** Ninguna funcionalidad se da por terminada sin superar sus tests correspondientes.

*    **Colaboración Humano-IA:** Se utiliza un agente de IA de forma expresa y documentada para la planificación y soporte técnico.

## Proceso para una Historia de Usuario (HU)

### Análisis

Leer la HU y sus **Criterios de Aceptación (CA)**. Identificar los **tests E2E** que validan cada CA.
Estos tests los ha de planficar el agente, presentar al humano, y una vez que éste lo valide, realizarlos.

### Descomposición
Dividir la HU en **Tareas** lógicas e implementables de forma independiente.

Esta descomposición la realiza el humano.

### Ciclo por Tarea 
El humano definirá cuando se ha de comenzar y dar por terminada una tarea.

a. **Análisis**: Entender qué funcionalidad concreta debe entregar esta tarea.

b. **Diseño**: Decidir qué código y tests (unitarios/integración) se necesitan para la funcionalidad de *esta tarea*.

c. **Validación del diseño**: El humano definirá si es válido el diseño propuesto, y podrá realizar modificaciones. Hasta que no lo valide, no se continuará con el siguiente paso.

d. **Implementación:**

     1. Crear/escribir código según `coding_style.md`.
     2. Crear los **tests unitarios** (`.test.js`) co-localizados en la carpeta del componente o servicio.
     3. Crear los **tests de integración** en `/tests/integration/` definidos en el plan.
e. **Validación de los tests**: Ejecutar **solo los tests E2E relacionados con la tarea actual** para verificar que funciona y no rompe lo existente.
f. **Validación final de la tarea**: El humano decide si la tarea es válida o hay que hacer cambios.

### Validación Final de la Historia de Usuario

* **Tests E2E Completos:** Una vez completadas **todas** las tareas, ejecutar los **tests E2E completos** de la HU.
* **Estado "Done":** La HU solo se considera **Done** cuando todos sus tests E2E pasan.

* **Presentación:** El resultado final se demuestra al cliente/formador en el Sprint Review.
