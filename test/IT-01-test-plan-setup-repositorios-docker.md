# Plan de Pruebas: [IT-01] Setup de Repositorios, Docker Compose y Entorno Local

**ID Tarea:** IT-01  
**Título:** Setup de Repositorios, Docker Compose y Entorno Local  
**Tarjeta Trello:** [https://trello.com/c/O0FaipCe](https://trello.com/c/O0FaipCe)  
**Fecha de Ejecución:** 2026-11-10  
**Estado:** SUPERADO (PASS)  
**Agente Evaluador / Implementador:** trello_implementer  

---

## 1. Alcance de Pruebas
- **Repositorios:** `impulsetech` (orquestador raíz), `impulsetech-be`, `impulsetech-fe`, `impulsetech-migration`.
- **Infraestructura Contenerizada:** Docker Compose orquestando 4 servicios:
  - `impulsetech-postgres` (PostgreSQL 16 en puerto host 5433).
  - `impulsetech-backend` (FastAPI en puerto host 8000).
  - `impulsetech-frontend` (Angular 18 en puerto host 4200).
  - `impulsetech-migration` (dbmate container).
- **Archivos de Configuración:** `.env.example`, `.env`, `docker-compose.yml`.

---

## 2. Pruebas Automatizadas Ejecutadas

### 2.1 Backend (pytest)
- **Comando:** `docker compose exec backend pytest`
- **Resultados:**
  ```text
  tests/test_health.py::test_health_endpoint PASSED
  tests/test_health.py::test_root_endpoint PASSED
  ============================== 2 passed in 1.11s ===============================
  ```
- **Estado:** ✅ PASS (100% de aserciones válidas)

### 2.2 Frontend (ng build / compilación Angular)
- **Comando:** `docker compose exec frontend npm run build`
- **Aserciones:** Cero errores de tipado en TypeScript 5.5, empaquetado de assets y estilos Tailwind CSS.
- **Estado:** ✅ PASS

### 2.3 PostgreSQL Healthcheck
- **Comando:** `docker compose exec postgres psql -U impulsetech -d impulsetech_dev -c "SELECT version();"`
- **Resultado:**
  ```text
  PostgreSQL 16.15 on x86_64-pc-linux-musl, compiled by gcc (Alpine 15.2.0) 15.2.0, 64-bit
  ```
- **Estado:** ✅ PASS

---

## 3. Guía de Pruebas Manuales / Verificación Paso a Paso

### Paso 1: Verificación de Estado de Contenedores
```bash
docker compose ps
```
*Resultado Esperado:* Todos los servicios (`postgres`, `backend`, `frontend`) en estado `Up` / `healthy`.

### Paso 2: Healthcheck del Backend FastAPI
```bash
curl -s http://localhost:8000/api/v1/health
```
*Payload de Respuesta:*
```json
{
  "status": "ok",
  "app": "ImpulseTech Backend API",
  "version": "1.0.0",
  "environment": "development"
}
```
*Código HTTP Esperado:* `200 OK`

### Paso 3: Documentación Interactiva Swagger / OpenAPI
Visitar en navegador: `http://localhost:8000/docs`
*Resultado Esperado:* Interfaz Swagger UI cargando los tags `Root` y `Health`.

### Paso 4: Carga del Frontend Angular
```bash
curl -I http://localhost:4200
```
*Resultado Esperado:* `HTTP/1.1 200 OK`
Visitar en navegador: `http://localhost:4200`
*Resultado Esperado:* Renderizado de la interfaz Bento Grid de ImpulseTech con Tailwind CSS y estatus "Entorno Local Activo".

---

## 4. Matriz de Criterios de Aceptación (DoD)

- [x] Repositorios independientes clonados y vinculados a GitHub (`edgonbr88/impulsetech-*`).
- [x] `docker compose up -d` arranca sin conflictos de puertos (Postgres mapeado a 5433 en host).
- [x] Endpoint `GET /api/v1/health` responde 200 OK en `http://localhost:8000`.
- [x] Frontend Angular responde en `http://localhost:4200` con separación estricta de plantillas `.component.html`.
- [x] Base de datos PostgreSQL 16 operativa con volumen persistente `postgres_data`.
- [x] Pruebas automatizadas en verde (`pytest`).
- [x] Plan de pruebas documentado en `test/IT-01-test-plan-setup-repositorios-docker.md`.
