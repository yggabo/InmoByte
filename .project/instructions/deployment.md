# Instrucciones de despliegue

## Objetivo
Este documento explica cómo preparar el proyecto para producción, cumpliendo con los estándares de rendimiento del cliente. Nos enfocamos en la generación del **build** optimizado y el despliegue de la arquitectura frontend.

## Comando para Build
Utilizamos Vite como herramienta de construcción para Vue 3:

```bash
npm run build
```
Este comando crea una carpeta `dist/` con todo listo para pasárselo a un servidor web.

## Contenido de la Carpeta de Build
La carpeta generada contendrá:
*   **`index.html`**: El archivo HTML procesado, con los enlaces a CSS y JS inyectados y optimizados.

*   **`assets/`**: Una subcarpeta con todos los archivos JavaScript y CSS minificados y renombrados.

*   Copias optimizadas de los archivos estáticos de la carpeta `public/`.

## Consideración de Datos (API y JSON-Server)

El despliegue debe contemplar dos fuentes de datos según el proyecto:

*    **APIs Públicas:** Asegurarse de que las API Keys estén configuradas correctamente en variables de entorno para producción.

*   **Servidor Fake (Json-Server):** Al ser una herramienta de desarrollo, para el despliegue final se recomienda usar servicios como MockAPI o desplegar el db.json en un servicio compatible para que el CRUD siga funcionando en la versión en vivo.

## Regla de Despliegue
* **Solo se despliega el contenido de la carpeta `dist/``.** Nunca se suben la carpeta `src/`, `node_modules/` o los archivos de configuración del entorno de desarrollo.

**Repositorio:** El código fuente debe estar disponible en GitHub con ramas diferenciadas (main/producción y developer).

* **Plataforma:** Se recomienda el uso de Netlify o similares para el despliegue del frontend.

## Verificación Local
Antes de desplegar, puedes verificar que el build funciona correctamente localmente con:
```bash
npm run preview
```
* Que no existan errores de renderización ni bugs visibles.

* Que el diseño sea totalmente responsive en el entorno de producción (Mobile, Tablet, Desktop).

* Que el sitio sea accesible y legible.
