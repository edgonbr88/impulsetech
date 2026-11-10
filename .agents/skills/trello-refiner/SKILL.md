---
name: trello-refiner
description: >-
  Lee tarjetas crudas de la columna 'To Refine' en el tablero de ImpulseTech en Trello,
  las analiza frente a la biblia del proyecto (STARTUP_CANVAS.md), entrevista al usuario para resolver dudas,
  las formatea con especificaciones técnicas rigurosas (PostgreSQL, FastAPI, Angular, dbmate),
  criterios de aceptación (DoD), nomenclatura [IT-XX], y las mueve a la columna 'To Do'.
---

# Trello Refiner Skill — ImpulseTech

Esta skill guía al agente en la ejecución del rol de **`trello_refiner`** para ImpulseTech.

## Objetivo
Tomar requerimientos crudos o ideas desde la columna **`To Refine`** del tablero de Trello de ImpulseTech, analizarlos exhaustivamente contrastándolos con la Biblia del proyecto ([STARTUP_CANVAS.md](file:///home/edgar/impulsetech/STARTUP_CANVAS.md)), consultar al usuario ante cualquier duda o ambigüedad, formatear la tarjeta con especificación técnica estándar de producción (`[IT-XX]`) y moverla a la columna **`To Do`**.

---

## Fuente Única de Verdad (Obligatorio Consultar)
* [STARTUP_CANVAS.md](file:///home/edgar/impulsetech/STARTUP_CANVAS.md): Biblia técnica, arquitectónica y de negocio del proyecto.
* Migraciones DDL existentes en `impulsetech-migration/db/migrations/`.

---

## Parámetros de Conexión a Trello
* **Tablero:** `ImpulseTech` (`https://trello.com/b/VNgiLVB1/impulsetech`)
* **ID del Tablero:** `6af3491a15ab3c1f1efcdaeb`
* **ID de Columna `To Refine`:** `6af3492b027d6403a9386500`
* **ID de Columna `To Do`:** `6af3493282d4285b6d65437d`
* **ID de Columna `in development`:** `6af34946f6c528d1ce0ca173`
* **ID de Columna `in testing`:** `6af34951ba4dbf8771921ef8`
* **ID de Columna `done`:** `6af34960104d1fb5aae275ee`
* **Credenciales:** Variables `TRELLO_API_KEY` y `TRELLO_TOKEN` o configuradas en los scripts auxiliares.

---

## Procedimiento Paso a Paso

### 1. Obtener Tarjetas Pendientes de Refinamiento
Ejecutar el script auxiliar:
```bash
python3 .agents/skills/trello-refiner/scripts/fetch_to_refine.py
```
*Si no hay tarjetas en `To Refine`, informa al usuario inmediatamente.*

### 2. Análisis Técnico y de Negocio
Para la tarjeta objetivo:
1. Examinar el título y descripción inicial.
2. Cruzar requerimientos con [STARTUP_CANVAS.md](file:///home/edgar/impulsetech/STARTUP_CANVAS.md):
   * ¿Afecta a Leads, Clientes, Servicios o Pagos?
   * ¿Requiere cambios DDL en PostgreSQL (dbmate)?
   * ¿Endpoints en FastAPI (rutas, esquemas Pydantic v2, autenticación JWT)?
   * ¿Componentes en Angular 18+ (Standalone, Signals, plantillas `.html` separadas)?

### 3. Puerta de Clarificación: Preguntar al Usuario (OBLIGATORIO)
**Nunca asumas decisiones críticas de negocio, flujos o arquitectura.**
Si hay cualquier duda:
* Formula preguntas directas, estructuradas y con opciones claras.
* Espera la respuesta del usuario antes de proceder a mover la tarjeta.

### 4. Determinar el Siguiente ID (`[IT-XX]`)
Ejecutar el script auxiliar:
```bash
python3 .agents/skills/trello-refiner/scripts/get_next_it_id.py
```

### 5. Formatear la Tarjeta Refinada
Estructura estándar de la tarjeta en Trello:
* **Título:** `[IT-XX] <Título Descriptivo y Claro>`
* **Cuerpo de la Descripción:**
```markdown
* **Lista en Trello:** `To Do`
* **Etiquetas:** `Backend`, `Frontend`, `Database`, `Fase X`
* **Contexto de Negocio:**
  * <Problema operativo que resuelve y valor para la operación de ImpulseTech.>
* **Especificación Técnica:**
  1. Base de datos: Tablas impactadas, nuevas columnas o migraciones DDL con dbmate.
  2. Backend (FastAPI): Endpoints REST (métodos, URLs), esquemas Pydantic v2, servicios y validación JWT.
  3. Frontend (Angular 18+): Componentes standalone, servicios HTTP, interceptores, directrices de `frontend-design`.
* **Criterios de Aceptación (DoD):**
  * [ ] Criterio 1 medible y verificable.
  * [ ] Criterio 2 medible y verificable.
  * [ ] Tests automatizados pasando y sin errores de compilación.
* **Dependencias:** `IT-YY` (si requiere tareas previas).
```

### 6. Mover la Tarjeta a `To Do`
```bash
python3 .agents/skills/trello-refiner/scripts/refine_card.py <CARD_ID> \
  --title "[IT-XX] <Nuevo Título>" \
  --desc-file path/to/temp_desc.md \
  --comment "Tarjeta refinada por trello_refiner y movida a 'To Do'."
```
