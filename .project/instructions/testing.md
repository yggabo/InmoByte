# Instrucciones para testing

## Principios
*   **Mínimo de ejecución:**: El proyecto debe contar con al menos 5 tests que midan diferentes contextos de ejecución.

*   **Unitarios con el código:**: Los tests unitarios se escriben junto al archivo que prueban para facilitar el mantenimiento.

*   **Nomenclatura clara**: Usa el sufijo `.test.js` (o .`test.js`)para identificar los archivos de prueba.

## Estructura de Carpetas

### Tests Unitarios
Siguiendo la modularización de Vue 3, los tests de componentes y composables se ubican en su respectiva carpeta dentro de `src/.`
```
src/
├── components/
│   └── atoms/
│       ├── BaseButton.vue
│       └── BaseButton.test.ts  # Test del componente atómico
├── composables/
│   ├── useApi.ts               # Composable obligatorio 
│   └── useApi.test.ts          # Test de lógica reactiva
└── stores/
    ├── counter.ts
    └── counter.test.ts         # Test de estado de Pinia
```

### Tests E2E y Globales
Todos los demás tests se organizan dentro de la carpeta `/tests/` en la raíz del proyecto.

```
proyecto/
├── src/                # Código fuente
├── tests/              # Carpeta dedicada a tests globales
│   ├── integration/    # Tests de integración
│   ├── e2e/            # Flujos de usuario (ej: navegación, CRUD)
│   └── fixtures/       # Datos JSON de prueba para simular la API
└── ...
```

## Contextos de Prueba Obligatorios

Para cumplir con los criterios de rendimiento, los 5 tests deben cubrir:

* 1. **Renderizado de componentes:** Verificar que los datos de la API se visualicen correctamente en la interfaz.

* 2.   **Lógica de Composables:** Probar el funcionamiento del composable obligatorio.

* 3.  **Interactividad:** Validar comportamientos de selección, mostrar y ocultar elementos (`v-show`, `v-if`).

* 4. **Gestión de Estado:** Pruebas sobre los estados de Pinia si se utiliza.

* 5. **Operaciones CRUD:** Si se implementa Json-Server, probar la integración de Get, Post, Put o Delete.



## Comando para Ejecutar Tests

Para asegurar que el código funciona sin bugs antes de la entrega:

```
# Ejecutar suite de pruebas
npm run test:unit
# Ejecutar tests E2E (si se usa Cypress)
npm run test:e2e
```
