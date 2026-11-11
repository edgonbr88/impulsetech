# Plan de Implementación: [IT-01] Setup de Repositorios, Docker Compose y Entorno Local

**ID Tarea:** IT-01  
**Tarjeta Trello:** [https://trello.com/c/O0FaipCe](https://trello.com/c/O0FaipCe) (ID: `6af3542292c6d43d3a6079c6`)  
**Fecha:** 2026-11-10  
**Estado del Plan:** LISTO PARA IMPLEMENTACIÓN  
**Agente Revisor/Planificador:** trello_planner  

---

## 1. Contexto de Negocio y Justificación
ImpulseTech requiere una infraestructura de desarrollo local estandarizada, reproducible y contenerizada para que los desarrolladores y agentes de IA puedan trabajar de manera desacoplada en los tres componentes fundamentales de la plataforma (Backend FastAPI, Frontend Angular y Migraciones dbmate), sin discrepancias de entorno entre máquinas y garantizando persistencia de base de datos local en PostgreSQL 16.

---

## 2. Alcance Técnico y Arquitectura
- **Repositorio Raíz (`impulsetech`):**
  - Orquestación con `docker-compose.yml`.
  - Configuración de variables de entorno (`.env.example` y `.env`).
  - Clonación / inicialización de los 3 subrepositorios independientes como subdirectorios.
- **Repositorio Backend (`impulsetech-be`):**
  - Esqueleto FastAPI (Python 3.12+).
  - Endpoint de healthcheck: `GET /api/v1/health` retornando estado de servicio y versión.
  - `requirements.txt` con FastAPI, Uvicorn, SQLAlchemy, Pydantic v2, pytest y httpx.
  - `Dockerfile` optimizado para desarrollo con hot-reload (`uvicorn --reload`).
- **Repositorio Frontend (`impulsetech-fe`):**
  - Proyecto Angular 18+ con Standalone Components.
  - Configuración inicial de Tailwind CSS conforme a la skill `frontend-design`.
  - `Dockerfile` para desarrollo con `@angular/cli` sirviendo en el puerto 4200 (`ng serve --host 0.0.0.0 --poll 2000`).
- **Repositorio Migraciones (`impulsetech-migration`):**
  - Directorio `db/migrations/`.
  - Configuración `dbmate` apuntando a `DATABASE_URL` de PostgreSQL local.
  - Script o servicio dockerizado para correr migraciones automáticas.

---

## 3. Modelo de Datos y Migraciones (PostgreSQL / dbmate)
- Para esta tarea `IT-01`, se verifica la conectividad del motor PostgreSQL 16 a través del healthcheck de Docker (`pg_isready -U impulsetech -d impulsetech_dev`).
- El servicio `migration` utilizará la imagen oficial `amacneil/dbmate` para verificar conectividad y preparar el directorio de migraciones.

---

## 4. Backend: FastAPI (Python 3.12+)
- **Estructura en `impulsetech-be/`:**
  ```
  impulsetech-be/
  ├── Dockerfile
  ├── requirements.txt
  ├── .gitignore
  ├── README.md
  └── src/
      ├── __init__.py
      ├── main.py
      └── core/
          ├── __init__.py
          └── config.py
  ```
- **Endpoint a implementar:**
  - `GET /api/v1/health` -> `{"status": "ok", "app": "ImpulseTech Backend API", "version": "1.0.0"}`

---

## 5. Frontend: Angular 18+
- **Estructura en `impulsetech-fe/`:**
  ```
  impulsetech-fe/
  ├── Dockerfile
  ├── package.json
  ├── angular.json
  ├── tsconfig.json
  ├── tailwind.config.js
  ├── .gitignore
  └── src/
      ├── index.html
      ├── main.ts
      ├── styles.scss
      └── app/
          ├── app.config.ts
          ├── app.routes.ts
          ├── app.component.ts
          ├── app.component.html
          └── app.component.scss
  ```
- **Directivas visuales (`frontend-design`):**
  - Separación obligatoria de plantillas: `templateUrl: './app.component.html'`.
  - Landing / Splash inicial sobrio: Identidad visual de ImpulseTech (Slate `#0F172A`, Sky `#0284C7`, tipografía limpia, sin elementos decorativos cliché).

---

## 6. Pruebas y Verificación
- **Prueba 1: Docker Compose Up**
  - Comando: `docker compose up -d`
  - Verificación: `docker compose ps` muestra `postgres`, `migration`, `backend` y `frontend` en estado `healthy` o `running`.
- **Prueba 2: Backend Healthcheck**
  - Comando: `curl -s http://localhost:8000/api/v1/health`
  - Esperado: HTTP 200 con JSON `{"status": "ok", ...}`.
- **Prueba 3: Frontend Web UI**
  - Comando: `curl -I http://localhost:4200`
  - Esperado: HTTP 200 OK.
- **Prueba 4: Persistencia PostgreSQL**
  - Comando: `docker compose exec postgres psql -U impulsetech -d impulsetech_dev -c "SELECT 1;"`
  - Esperado: Retorna fila `1`.

---

## 7. Checklist Paso a Paso (Para trello_implementer)
- [x] Clonar e inicializar los 3 subrepositorios en el workspace (`impulsetech-be`, `impulsetech-fe`, `impulsetech-migration`).
- [x] Configurar `.env.example` y `.env` en la raíz de `impulsetech/`.
- [x] Crear el esqueleto de `impulsetech-be` con `requirements.txt`, `src/main.py` y `Dockerfile`.
- [x] Crear el esqueleto de `impulsetech-fe` con Angular 18, Tailwind CSS, `app.component` (plantilla `.html` separada) y `Dockerfile`.
- [x] Configurar el directorio `db/migrations/` en `impulsetech-migration` con su `.env.example`.
- [x] Crear `docker-compose.yml` en la raíz integrando los 4 servicios (`postgres`, `migration`, `backend`, `frontend`).
- [x] Levantar el entorno con `docker compose up -d` y esperar healthchecks.
- [x] Validar endpoints y respuestas de cada servicio.
- [x] Generar el Plan de Pruebas en `test/IT-01-test-plan-setup-repositorios-docker.md`.
- [x] Crear ramas `feature/IT-01-setup-repos-docker` en los repositorios, hacer commit y push a GitHub.
- [x] Crear Pull Requests hacia `main` en GitHub.
- [x] Mover tarjeta en Trello a `in testing` mediante script auxiliar.

---

## 8. Criterios de Aceptación (Definition of Done - DoD)
- [x] Los 3 subrepositorios (`impulsetech-be`, `impulsetech-fe`, `impulsetech-migration`) están clonados localmente y vinculados a sus remotos de GitHub.
- [x] `docker compose up -d` arranca sin errores ni conflictos de puertos.
- [x] Endpoint `GET /api/v1/health` responde 200 OK en `http://localhost:8000`.
- [x] Frontend Angular responde en `http://localhost:4200`.
- [x] Contenedor PostgreSQL 16 listo y accesible en puerto 5433 (host) / 5432 (interno).
- [x] Plan de pruebas generado y documentado en `test/`.
- [x] PRs creados en GitHub y tarjeta en Trello movida a `in testing`.
