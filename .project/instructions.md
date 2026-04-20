# Instrucciones Generales del Proyecto

## **Propósito y Alcance**
Este documento establece las directrices fundamentales que **cualquier agente de IA** debe seguir al colaborar en este proyecto. Considera esta información como el contexto base para todas las interacciones.

## **Normas de Comportamiento Esperado**

### **Prioridades en Orden de Importancia:**
1. **Seguridad primero** - Nunca sugerir código con vulnerabilidades conocidas
2. **Calidad sobre velocidad** - Soluciones robustas antes que rápidas
3. **Alineación con objetivos** - Cada aporte debe avanzar los objetivos del proyecto

### **Estilo de Comunicación:**
- **Claro y conciso** - Explicaciones directas, sin florituras
- **Práctico** - Enfocado en implementación real
- **Proactivo** - Anticipar problemas y sugerir mejoras
- **Humilde** - Reconocer limitaciones cuando existan

## **Arquitectura de Decisiones**

### **Jerarquía de Autoridad:**
```
1. Requerimientos del negocio (historias de usuario)
2. Instrucciones técnicas específicas (/instructions/[área].md)
3. Mejores prácticas de la industria
4. Preferencias del mantenedor humano
```

### **Cuando encuentres ambigüedad:**
1. **Consultar primero** - Preguntar en lugar de asumir
2. **Documentar la decisión** - Explicar el razonamiento
3. **Sugerir estandarización** - Proponer actualizar las instrucciones

## **Flujo de Trabajo Esperado**

### **Para cada tarea:**
1. **Contextualizar** - Leer la historia de usuario relevante en `/stories/`
2. **Verificar estado** - Revisar progreso en `/kanban.md`
3. **Consultar instrucciones** - Leer los archivos pertinentes en `/instructions/`
4. **Planificar** - Planificar según las pautas
5. **Validar** - Iterar la definición del plan hasta su validación por el humano
6. **Ejecutar** - Implementar según el plan validado

### **Formato de entregables:**
- **Código**: Comentado, testeado, siguiendo convenciones
- **Documentación**: En Markdown, con ejemplos prácticos
- **Decisiones**: Justificadas con referencia a requisitos

## **Restricciones Críticas**

### **Lo que NO debes hacer:**
- Leer o modificar archivos fuera del directorio del proyecto
- Leer o modificar variables de entorno que no sean específicas del CLI del agente
- Modificar la estructura de archivos sin consultar
- Introducir dependencias no aprobadas
- Saltarse procesos de testing definidos
- Asumir contextos no documentados
- Crear soluciones over-engineered

### **Límites técnicos:**
## **Límites de Compatibilidad**
- **Navegadores**: Chrome 90+, Firefox 88+, Safari 14+ (no soporte IE)
<!-- Límites de ejemplo, no definidos
- **Sistemas operativos**: Linux Ubuntu 20.04+, macOS 10.15+, Windows 10+
- **Dispositivos móviles**: Responsive hasta 320px de ancho
- **APIs externas**: Solo versión 2.x de [Nombre API], no migrar a v3
- **Legado**: Mantener compatibilidad con archivos formato .legacy v1
--> 
## Límites de Rendimiento
- **Tiempo de carga**: < 3 segundos en conexión 3G
- **Tamaño de bundle**: < 500KB inicial, < 2MB total
<!-- Límites de ejemplo, no definidos
- **Uso de memoria**: < 100MB en cliente, < 512MB en servidor
- **Consultas a DB**: < 50ms por query en producción
- **Concurrencia**: Soporte para 1000 usuarios simultáneos
-->
## Límites de Seguridad
- **Dependencias**: Solo paquetes con auditoría de seguridad mensual
<!-- Límites de ejemplo, no definidos
- **Autenticación**: JWT con expiración de 24h máximo
- **Contraseñas**: Hash bcrypt con salt de 10 rondas mínimo
- **APIs**: Rate limiting de 100 requests/ip/minuto
- **Datos sensibles**: Nunca loggear PII (emails, documentos)
-->

## **Cómo Usar esta Estructura**

### **Para desarrolladores humanos:**
Estas instrucciones están diseñadas para ser leídas por personas y ejecutadas por agentes de IA. Mantén una versión actualizada.

### **Para agentes de IA:**
1. Esta es tu fuente de verdad inicial
2. Los conflictos se resuelven jerárquicamente (este archivo > específicos)
3. La falta de claridad es una oportunidad para mejorar la documentación

## **Relación con Otros Componentes**

```
instructions.md (este archivo)
    ├── Estado del proyecto → /kanban.md
    ├── Historias de usuario → /stories/
    |   ├── Plantilla → /template.md
    |   └── Nomenclatura → [Codigo] [Título].md
    └── Instrucciones específicas → /instructions/[temática].md
        ├── Estructura → /structure.md
        ├── Despliegue → /deployment.md
        ├── Estilo de codigo → /coding_style.md
        ├── Testing → /testing.md
        └── Workflow → /workflow.md
```

## **Filosofía del Proyecto**
- **Iterativo** - Mejora continua, no perfección inicial
- **Colaborativo** - Humanos y IA trabajando complementariamente
- **Pragmático** - Soluciones que funcionan hoy, escalan mañana
- **Documentado** - El conocimiento debe ser explícito y accesible


> **Nota para agentes**: Si alguna instrucción parece conflictiva o incompleta, pregunta antes de proceder. La comunicación clara previene errores costosos.