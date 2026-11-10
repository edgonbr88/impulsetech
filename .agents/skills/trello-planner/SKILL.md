---
name: trello-planner
description: >-
  Lee tarjetas activas de la columna 'in development' en el tablero de ImpulseTech en Trello,
  las contextualiza con la biblia técnica (STARTUP_CANVAS.md) y genera un plan exhaustivo de implementación
  en formato markdown dentro de la carpeta plans/IT-XX-plan-*.md.
---

# Trello Planner Skill — ImpulseTech

Esta skill guía al agente en la ejecución del rol de **`trello_planner`** para ImpulseTech.

## Objetivo
Inspeccionar la columna **`in development`** del tablero de Trello de ImpulseTech, analizar la(s) tarjeta(s) activa(s) contra la Biblia técnica del proyecto ([STARTUP_CANVAS.md](file:///home/edgar/impulsetech/STARTUP_CANVAS.md)), resolver cualquier duda con el usuario y redactar un plan de implementación técnico completo, exhaustivo y sin ambigüedades dentro de `plans/` para el agente **`trello_implementer`**.

---

## Archivo de Contexto Obligatorio
* [STARTUP_CANVAS.md](file:///home/edgar/impulsetech/STARTUP_CANVAS.md): Biblia técnica, arquitectónica y de negocio del proyecto.

---

## Parámetros de Conexión a Trello
* **Tablero:** `ImpulseTech` (`https://trello.com/b/VNgiLVB1/impulsetech`)
* **ID de Lista `in development`:** `6af34946f6c528d1ce0ca173`
* **ID de Lista `To Do`:** `6af3493282d4285b6d65437d`
* **Credenciales:** Variables `TRELLO_API_KEY` y `TRELLO_TOKEN`.

---

## Procedimiento Paso a Paso

### 1. Obtener Tarjetas en Desarrollo
Ejecutar el script auxiliar:
```bash
python3 .agents/skills/trello-planner/scripts/fetch_in_dev.py
```
*Si no hay tarjetas en `in development`, informa al usuario inmediatamente y lista las candidatas en `To Do`.*

### 2. Contextualización Técnica Profunda
Para cada tarjeta en `in development`:
1. Extraer ID, título (`[IT-XX] ...`) y descripción técnica.
2. Cruzar con las secciones relevantes de [STARTUP_CANVAS.md](file:///home/edgar/impulsetech/STARTUP_CANVAS.md):
   * **Base de datos (dbmate / PostgreSQL):** Cambios DDL exactos, tipos de datos, constraints, índices y nombre de archivo de migración `impulsetech-migration/db/migrations/YYYYMMDDHHMMSS_*.sql`.
   * **Backend (FastAPI):** Rutas REST, modelos SQLAlchemy Async, esquemas Pydantic v2, servicios, middlewares y seguridad JWT.
   * **Frontend (Angular 18+):** Componentes Standalone, signals, servicios HTTP, interceptores, directrices de `frontend-design` (paleta, tipografía, cero plantillas genéricas) y separación estricta de plantillas `.component.html`.

### 3. Puerta de Clarificación: Preguntar al Usuario (OBLIGATORIO)
**Nunca asumas decisiones críticas.** Si detectas dudas sobre contratos de API, comportamiento de la interfaz o reglas de negocio:
* Pregunta al usuario antes de redactar el plan definitivo.

### 4. Generar Plan de Implementación
Crear un nuevo archivo markdown en la carpeta `plans/`:
* **Formato:** `plans/IT-XX-plan-<slug-tarea>.md` (ejemplo: `plans/IT-01-plan-setup-repositorios-docker.md`).

#### Estructura Estándar del Plan:
```markdown
# Plan de Implementación: [IT-XX] <Título de la Tarea>

**ID Tarea:** IT-XX  
**Tarjeta Trello:** <URL de la tarjeta>  
**Fecha:** <Fecha actual>  
**Estado del Plan:** LISTO PARA IMPLEMENTACIÓN  
**Agente Revisor/Planificador:** trello_planner  

---

## 1. Contexto de Negocio y Justificación
- ¿Qué problema operativo resuelve esta tarea en ImpulseTech?
- Impacto para los ejecutivos, administradores o clientes.

## 2. Alcance Técnico y Arquitectura
- Componentes y repositorios afectados (`impulsetech-be`, `impulsetech-fe`, `impulsetech-migration`, `impulsetech`).
- Dependencias con otras tareas.

## 3. Modelo de Datos y Migraciones (PostgreSQL / dbmate)
- Script SQL DDL exacto.
- Nombre del archivo de migración: `impulsetech-migration/db/migrations/YYYYMMDDHHMMSS_*.sql`.

## 4. Backend: FastAPI (Python 3.12+)
- Módulos a crear o modificar en `impulsetech-be/src/`:
  - Modelos SQLAlchemy Async
  - Esquemas Pydantic v2 (Request / Response)
  - Servicios / Lógica de negocio
  - Router REST y dependencias de autenticación JWT

## 5. Frontend: Angular 18+ (Standalone Components)
- Directiva de Diseño: Seguir `frontend-design` (paleta intencional, tipografía, cero plantillas genéricas).
- Separación Obligatoria de Plantillas: Todo componente con archivos `.ts` y `.html` independientes.
- Componentes, servicios HTTP y rutas en `impulsetech-fe/src/app/`.

## 6. Pruebas y Verificación
- Tests unitarios backend con `pytest`.
- Verificación frontend (`ng build` / `npm run build`).
- Comandos cURL de prueba con payloads y respuestas esperadas.

## 7. Checklist Paso a Paso (Para trello_implementer)
- [ ] Paso 1: ...
- [ ] Paso 2: ...
- [ ] Paso 3: ...

## 8. Criterios de Aceptación (Definition of Done - DoD)
- [ ] Compilación limpia en backend y frontend.
- [ ] Tests automatizados en verde.
- [ ] Docker Compose levanta y responde sin errores.
```

### 5. Notificación al Usuario
Reporta que el plan ha sido generado con enlace directo y resumen de las decisiones arquitectónicas.
