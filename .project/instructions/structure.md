# Instrucciones sobre la estructura

## Principios
* **Modularización:** Se deben crear componentes para albergar los datos de visualización en módulos replicables.

* **Atomic Web Design:** Los componentes deben aplicar la filosofía de diseño atómico (átomos, moléculas, organismos).

* **Naming Semántico:** Los nombres de vistas y componentes deben expresar qué son o qué hacen, nunca el nombre de los desarrolladores.

## Estructura Básica
```
proyecto/
├── public/              # Archivos estáticos que no se procesan (favicon, robots) 
├── src/                 # Código fuente principal
│   ├── assets/          # Imágenes, fuentes y estilos globales
│   ├── components/      # Componentes siguiendo Atomic Design 
│   │   ├── atoms/       # Componentes básicos (botones, inputs)
│   │   ├── molecules/   # Uniones de átomos (tarjetas, buscadores)
│   │   └── organisms/   # Estructuras complejas (listas en bucle, headers) 
│   ├── composables/     # Lógica reutilizable y hooks personalizados 
│   ├── router/          # Configuración de rutas (index.ts) 
│   ├── services/        # Gestión de peticiones API (fetch/axios) y Json-Server 
│   ├── stores/          # Gestión de estado con Pinia (counter.ts, etc.) 
│   ├── views/           # Vistas o páginas principales del website 
│   ├── App.vue          # Componente raíz
│   └── main.ts          # Punto de entrada y configuración inicial 
├── test/                # Mínimo 5 tests con librerías como Vitest/Cypress 
├── server/              # Servidor Fake (Json-Server) para operaciones 
├── package.json         # Dependencias y scripts del proyecto
└── vite.config.ts       # Configuración del entorno Vite 
 Configuración del entorno (Vite)
```

## Reglas Simples
* **Modularización Replicable:** Los componentes deben estar diseñados para mostrar datos en bucle (usando `v-for`).

* **Comunicación:** Se deben usar props para pasar datos de padre a hijo y emit para eventos de hijo a padre.

* **Reactividad:** El uso de ref,  reactive y toRef es obligatorio para gestionar la reactividad de los datos.

* **Asincronía:** Se recomienda el uso de etiquetas <suspense/> para gestionar estados de carga de la API.