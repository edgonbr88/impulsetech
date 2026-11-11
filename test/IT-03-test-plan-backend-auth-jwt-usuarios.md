# Plan de Pruebas: [IT-03] Backend: Autenticación JWT y Módulo de Usuarios en FastAPI

**ID Tarea:** IT-03  
**Título:** Backend: Autenticación JWT y Módulo de Usuarios en FastAPI  
**Tarjeta Trello:** [https://trello.com/c/PBAG5rhB](https://trello.com/c/PBAG5rhB)  
**Fecha de Ejecución:** 2026-11-10  
**Estado:** SUPERADO (PASS)  
**Agente Evaluador / Implementador:** trello_implementer  

---

## 1. Alcance de Pruebas
- **Repositorio Impactado:** `impulsetech-be`
- **Módulos y Componentes Probados:**
  - `src/core/security.py`: Hashing bcrypt y generación/decodificación de tokens JWT (HS256).
  - `src/core/database.py`: Conexión asíncrona SQLAlchemy 2.0 (`asyncpg` con `NullPool`).
  - `src/core/dependencies.py`: Inyección de dependencias `get_db`, `get_current_user` y `require_admin`.
  - `src/modules/users/models.py`: Mapeo ORM de tabla `usuarios` y tipo ENUM `rol_usuario_enum`.
  - `src/modules/auth/router.py`: Endpoints `POST /api/v1/auth/login` y `GET /api/v1/auth/me`.
  - `src/modules/users/router.py`: Endpoints `GET /api/v1/users/ejecutivos`, `GET /api/v1/users`, `POST /api/v1/users`.

---

## 2. Pruebas Automatizadas Ejecutadas (pytest)

- **Comando:** `docker compose exec backend pytest`
- **Resultados:**
  ```text
  tests/test_auth.py::test_login_success_admin PASSED
  tests/test_auth.py::test_login_invalid_password PASSED
  tests/test_auth.py::test_login_nonexistent_email PASSED
  tests/test_auth.py::test_get_me_authenticated PASSED
  tests/test_auth.py::test_get_me_unauthorized PASSED
  tests/test_auth.py::test_get_me_invalid_token PASSED
  tests/test_auth.py::test_get_active_ejecutivos PASSED
  tests/test_auth.py::test_admin_create_and_login_new_user PASSED
  tests/test_health.py::test_health_endpoint PASSED
  tests/test_health.py::test_root_endpoint PASSED
  ============================== 10 passed in 5.55s ==============================
  ```
- **Estado:** ✅ PASS (10 de 10 tests aprobados, 100% de éxito).

---

## 3. Guía de Pruebas Manuales / Comandos cURL Reproducibles

### Paso 1: Login de Administrador
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@impulsetech.com",
    "password": "Admin2026*!"
  }'
```
*Código HTTP Esperado:* `200 OK`  
*Respuesta:* Retorna objeto con `access_token`, `token_type: "bearer"` y objeto `user` con rol `ADMIN`.

### Paso 2: Consulta del Perfil Autenticado (`/me`)
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <TOKEN>"
```
*Código HTTP Esperado:* `200 OK`  
*Respuesta:* Retorna datos del usuario en sesión (`admin@impulsetech.com`).

### Paso 3: Consulta sin Token (Verificación de Seguridad)
```bash
curl -i -X GET http://localhost:8000/api/v1/auth/me
```
*Código HTTP Esperado:* `401 Unauthorized`

### Paso 4: Consulta de Ejecutivos Disponibles para Asignación
```bash
curl -X GET http://localhost:8000/api/v1/users/ejecutivos \
  -H "Authorization: Bearer <TOKEN>"
```
*Código HTTP Esperado:* `200 OK`  
*Respuesta:* Lista de usuarios activos.

---

## 4. Matriz de Criterios de Aceptación (DoD)

- [x] Suite completa de `pytest` pasando al 100% (10 tests en verde).
- [x] Endpoint `POST /api/v1/auth/login` autentica al usuario semilla con verificación bcrypt.
- [x] Token JWT contiene claims requeridos (`sub`, `email`, `rol`, `nombre`) y expiración.
- [x] Endpoints protegidos rechazan peticiones no autenticadas con código HTTP 401.
- [x] Endpoint `GET /api/v1/users/ejecutivos` activo y retornando lista de personal.
- [x] Endpoint de creación de usuarios restringido a rol `ADMIN`.
- [x] Documentación Swagger en `/docs` actualizada y funcional.
- [ ] PRs generados en GitHub y tarjeta en Trello movida a `in testing`.
