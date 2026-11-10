---
name: trello-implementer
description: >-
  Lee un plan de implementación desde plans/, ejecuta el checklist paso a paso (código FastAPI,
  Angular 18+ con frontend-design, migraciones dbmate), valida compilación y pruebas,
  genera un plan de pruebas en test/IT-XX-test-plan-*.md, crea ramas/PRs en GitHub y mueve la tarjeta a 'in testing' en Trello.
---

# Trello Implementer Skill — ImpulseTech

Esta skill guía al agente en la ejecución del rol de **`trello_implementer`** para ImpulseTech.

## Objetivo
Leer el plan de implementación aprobado por `trello_planner` dentro de `plans/IT-XX-plan-*.md`, escribir el código requerido (FastAPI en `impulsetech-be`, Angular 18 en `impulsetech-fe`, migraciones SQL en `impulsetech-migration`), verificar compilación y pruebas automatizadas, generar el documento de prueba obligatorio en `test/`, crear Pull Requests en GitHub y mover la tarjeta de Trello de **`in development`** a **`in testing`**.

---

## Directivas Obligatorias de Diseño y Arquitectura

### 🎨 Frontend UI/UX Design (Obligatorio para tareas de Frontend)
* **Skill de Referencia:** [.agents/skills/frontend-design/SKILL.md](file:///home/edgar/impulsetech/.agents/skills/frontend-design/SKILL.md).
* **Propósito:** Dotar al CRM de ImpulseTech de una identidad visual sobria, moderna y de alta densidad para la operación de consultoría legal y tecnológica en Venezuela.
* **Prohibición estricta de templates genéricos:** Cero fondos crema con terracota, cero temas oscuros con verde neón genérico, cero "SaaS-card kit" idéntico.
* **Separación Obligatoria de Plantillas:** Todo componente de Angular **DEBE** separar su plantilla HTML en un archivo independiente (`.component.html`) y su hoja de estilos en (`.component.scss` / `.component.css`). **PROHIBIDO** el uso de `template` inline en el archivo `.ts`.

### 🛡️ Base de Datos y Migraciones (dbmate)
* **PROHIBICIÓN ESTRICTA:** Queda terminantemente **PROHIBIDO ejecutar migraciones directamente en bases de datos productivas**. Todas las migraciones DDL de dbmate deben ejecutarse y validarse primero en el entorno de desarrollo local (PostgreSQL en Docker).

---

## Procedimiento Paso a Paso

### 1. Identificar y Leer el Plan Activo
1. Localizar el archivo de plan en `plans/` (ej. `plans/IT-01-plan-setup-repositorios-docker.md`).
2. Leer el contenido completo para entender:
   * Esquema DDL y nombre de migración dbmate.
   * Modelos, esquemas y endpoints de FastAPI.
   * Componentes, servicios e interfaces de Angular.
   * Criterios de Aceptación (DoD) y checklist paso a paso.

### 2. Ejecutar la Implementación
* **Base de Datos (`impulsetech-migration`):**
  * Crear nueva migración con dbmate: `YYYYMMDDHHMMSS_nombre.sql`.
  * Definir bloque `-- migrate:up` y `-- migrate:down`.
  * Ejecutar localmente con `dbmate up` y verificar esquema.
* **Backend (`impulsetech-be`):**
  * Seguir arquitectura modular: `core/`, `modules/<nombre>/` (`router.py`, `service.py`, `models.py`, `schemas.py`).
  * Validar esquemas con Pydantic v2 y seguridad con JWT en dependencias (`get_current_user`).
  * Ejecutar tests con `pytest`.
* **Frontend (`impulsetech-fe`):**
  * Crear componentes Standalone con Angular 18+.
  * Respetar separación de `.ts` y `.html`.
  * Integrar tokens y directrices de `frontend-design`.
  * Verificar compilación con `ng build` / `npm run build`.

### 3. Verificación y Pruebas Automatizadas
Antes de marcar cualquier tarea como completada:
1. Backend: Ejecutar `pytest` y asegurar 0 errores.
2. Frontend: Ejecutar `ng build` y asegurar 0 errores de tipado o compilación.
3. Docker Compose: Verificar que `docker compose up` levante los servicios sin caídas.

### 4. Documentar Plan de Pruebas en `test/`
El agente implementador **DEBE** generar obligatoriamente un archivo de Plan de Pruebas en:
`test/IT-XX-test-plan-<slug-tarea>.md` (ejemplo: `test/IT-01-test-plan-setup-repositorios-docker.md`).

**Estructura obligatoria del Plan de Pruebas:**
1. **Identificación:** ID Tarea, Título, Enlace a Trello y fecha.
2. **Alcance:** Módulos, tablas o componentes impactados.
3. **Pruebas Automatizadas Ejecutadas:** Comandos, tests ejecutados y resultado (PASS/FAIL).
4. **Guía de Pruebas Manuales Paso a Paso:** Comandos `cURL` reproducibles con headers `Authorization: Bearer <TOKEN>`, payloads JSON y códigos HTTP esperados. Pasos de interacción en la UI de Angular.
5. **Matriz de Criterios de Aceptación (DoD):** Checkboxes de los criterios verificados.

### 5. Actualizar el Checklist en `plans/`
Marcar cada paso completado con `[x]` en el archivo `plans/IT-XX-plan-*.md`.

### 6. Git Branching, Commit, Push y Creación de PR (GitHub)
1. Crear rama `feature/IT-XX-<slug>` en los repositorios modificados.
2. Hacer commit y push: `git push -u origin feature/IT-XX-<slug>`.
3. Crear Pull Request hacia `main` usando `gh pr create`.

### 7. Mover Tarjeta en Trello a `in testing`
Ejecutar el script auxiliar:
```bash
python3 .agents/skills/trello-implementer/scripts/move_to_testing.py <CARD_ID> "Implementación finalizada con éxito. Plan de pruebas generado en test/IT-XX-test-plan.md. Tests en verde. PRs: <LINKS_PRS>"
```

### 8. Reporte Final al Usuario
Reportar:
* Links directos a los Pull Requests en GitHub.
* Archivos creados y modificados con links markdown clicables.
* Resultado de compilación y tests.
* Enlace al plan de pruebas en `test/IT-XX-test-plan-*.md`.
* Confirmación del cambio de estado en Trello a `in testing`.
