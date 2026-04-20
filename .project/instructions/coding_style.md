# Instrucciones sobre el estilo del código

## Principios
*   **Claro > Inteligente**: La legibilidad es fundamental.
*   **Consistente**: Mantén las mismas convenciones en todo el proyecto.
*   **Inglés**: Todo el código (variables, funciones, clases y comentarios) se escribe en inglés.

## Convenciones
*   **Variables/Constantes**: `camelCase` (`userCount`). Constantes: `UPPER_SNAKE_CASE` (`API_BASE_URL`).
*   **Funciones/Métodos**: `camelCase` (`calculateTotal()`, `getUserById()`).
*   **Clases/Componentes**: `PascalCase` (`UserProfile`, `LoginService`).
*   **Archivos/Carpetas**: `kebab-case` (`user-service.js`, `components/`).
*   **Booleanos**: Usa prefijos como `is`, `has`, `should` (`isLoading`, `hasPermission`).

## Estructura
*   **Archivos**: Máximo 300-400 líneas. Divide si es más largo.
*   **Funciones**: Máximo 20-30 líneas. Haz una sola cosa.

## Estructura de Componentes (Vue 3)
* **Composition API:** Es obligatorio el uso de `<script setup>` y Composition API.
* **Reactividad:** Utilizar de forma precisa `ref`, `reactive` y `toRef` según el caso de uso.
* **Modularización:** Aplicar la filosofía de Atomic Web Design. Divide la interfaz en componentes pequeños y reutilizables.
* **Props/Emits:** Comunicación clara: props para bajar datos, emits para subir eventos.



## Calidad
*   **Sin console.log en prod**: No debe haber logs en la rama main. Para depurar, usa un envoltorio (wrapper) que se desactive en producción.
*   **Sin números mágicos**: Cualquier valor estático (como IDs o tiempos de espera) debe ser una constante con nombre descriptivo.
*   **DRY (Don't Repeat Yourself)**: La lógica compartida debe ir en Composables o archivos de utilidad.

## Comentarios
*   Explica el **"por qué"** (la intención o razón compleja), no el **"qué"** (el código obvio).

* **Tipado:** Se considera una mejora el uso de TypeScript.