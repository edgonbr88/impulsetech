# Plan de Implementación: [IT-03] Backend: Autenticación JWT y Módulo de Usuarios en FastAPI

**ID Tarea:** IT-03  
**Tarjeta Trello:** [https://trello.com/c/PBAG5rhB](https://trello.com/c/PBAG5rhB) (ID: `6af354233117271855ee8796`)  
**Fecha:** 2026-11-10  
**Estado del Plan:** LISTO PARA IMPLEMENTACIÓN  
**Agente Revisor/Planificador:** trello_planner  

---

## 1. Contexto de Negocio y Justificación
ImpulseTech maneja información sensible de negocios (trámites legales SAREN, datos societarios, cuentas por cobrar multimoneda y flujos de automatización). Es crítico proteger el acceso a la plataforma mediante autenticación robusta:
- Solo usuarios registrados y activos pueden interactuar con los endpoints del sistema.
- Los **Administradores** pueden gestionar altas y bajas de personal y ver toda la operación.
- Los **Ejecutivos** pueden autenticarse para consultar sus clientes y servicios asignados.
- Se requiere exponer el listado de ejecutivos activos (`GET /api/v1/users/ejecutivos`) para que el CRM permita la asignación de 1 ejecutivo por cliente (regla de negocio definida en el Canvas).

---

## 2. Alcance Técnico y Arquitectura
- **Repositorio Impactado:** `impulsetech-be` (y registro en `impulsetech`).
- **Framework:** FastAPI con Python 3.12+.
- **ORM & Driver:** SQLAlchemy 2.0 (Async) + `asyncpg`.
- **Criptografía & Tokens:**
  - Hashing seguro de contraseñas mediante `bcrypt` nativo (`gensalt`, `hashpw`, `checkpw`).
  - Generación y verificación de tokens JWT con `python-jose` (algoritmo `HS256`).
- **Estructura Modular:**
  ```text
  src/
  ├── core/
  │   ├── config.py          (Actualizar con settings JWT y BD)
  │   ├── database.py        (AsyncEngine, async_sessionmaker, Base)
  │   ├── security.py        (Hash, verify, JWT create/decode)
  │   └── dependencies.py    (get_db, get_current_user, require_admin)
  ├── modules/
  │   ├── auth/
  │   │   ├── __init__.py
  │   │   ├── schemas.py     (LoginRequest, TokenResponse)
  │   │   └── router.py      (POST /login, GET /me)
  │   └── users/
  │       ├── __init__.py
  │       ├── models.py      (Entidad Usuario SQLAlchemy)
  │       ├── schemas.py     (UserBase, UserCreate, UserResponse, etc.)
  │       ├── service.py     (Lógica de consulta y creación)
  │       └── router.py      (GET /ejecutivos, GET /, POST /)
  └── main.py                (Inclusión de routers)
  ```

---

## 3. Modelo de Datos y Entidad SQLAlchemy

### Mapeo de la Tabla `usuarios` (`src/modules/users/models.py`)
```python
import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from src.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(
        Enum("ADMIN", "EJECUTIVO", name="rol_usuario_enum", create_type=False),
        default="EJECUTIVO",
        nullable=False
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
```

---

## 4. Endpoints y Contratos de API REST

### Módulo Auth (`/api/v1/auth`)
1. **`POST /api/v1/auth/login`**:
   - *Request:* `{"email": "admin@impulsetech.com", "password": "..."}`
   - *Response:* `{"access_token": "...", "token_type": "bearer", "user": {"id": "...", "nombre": "...", "email": "...", "rol": "ADMIN", "activo": true}}`
   - *Status Codes:* 200 OK, 401 Unauthorized (credenciales inválidas o usuario inactivo).
2. **`GET /api/v1/auth/me`**:
   - *Headers:* `Authorization: Bearer <TOKEN>`
   - *Response:* `UserResponse` del usuario autenticado en sesión.
   - *Status Codes:* 200 OK, 401 Unauthorized.

### Módulo Users (`/api/v1/users`)
1. **`GET /api/v1/users/ejecutivos`**:
   - *Headers:* `Authorization: Bearer <TOKEN>`
   - *Response:* Lista de usuarios con rol `EJECUTIVO` (y `ADMIN` con capacidad operativa) activos para asignación de clientes.
2. **`GET /api/v1/users`**:
   - *Headers:* `Authorization: Bearer <TOKEN>` (Requiere rol `ADMIN`).
   - *Response:* Lista completa de usuarios del sistema.
3. **`POST /api/v1/users`**:
   - *Headers:* `Authorization: Bearer <TOKEN>` (Requiere rol `ADMIN`).
   - *Request:* `UserCreate` (nombre, email, password, rol).
   - *Response:* `UserResponse` creado con status 201 Created.

---

## 5. Pruebas y Verificación

### Tests Automatizados con `pytest` (`tests/test_auth.py`):
1. `test_login_success_admin`: Login con `admin@impulsetech.com` y password correcto -> Retorna token JWT y datos de usuario.
2. `test_login_invalid_password`: Contraseña errónea -> Retorna 401 Unauthorized.
3. `test_login_nonexistent_user`: Email inexistente -> Retorna 401 Unauthorized.
4. `test_get_me_authenticated`: Request con Bearer token válido -> Retorna perfil con rol `ADMIN`.
5. `test_get_me_unauthorized`: Request sin token o con token alterado -> Retorna 401.
6. `test_get_ejecutivos`: Request autenticado -> Retorna lista con status 200 OK.
7. `test_admin_create_user`: Admin crea un nuevo ejecutivo -> Retorna 201 Created y nuevo usuario disponible para login.

---

## 6. Checklist Paso a Paso (Para trello_implementer)
- [x] Implementar configuración de base de datos asíncrona en `src/core/database.py`.
- [x] Implementar funciones de seguridad criptográfica (bcrypt y JWT) en `src/core/security.py`.
- [x] Implementar modelo SQLAlchemy `Usuario` en `src/modules/users/models.py`.
- [x] Implementar esquemas Pydantic v2 en `src/modules/auth/schemas.py` y `src/modules/users/schemas.py`.
- [x] Implementar dependencias de inyección (`get_db`, `get_current_user`, `require_admin`) en `src/core/dependencies.py`.
- [x] Implementar rutas de autenticación en `src/modules/auth/router.py`.
- [x] Implementar servicio y rutas de usuarios en `src/modules/users/service.py` y `src/modules/users/router.py`.
- [x] Registrar los routers en `src/main.py`.
- [x] Escribir suite de pruebas automatizadas en `tests/test_auth.py`.
- [x] Ejecutar `pytest` dentro del contenedor backend y asegurar 100% de tests en verde.
- [x] Probar endpoints manualmente con `curl` verificando emisión y validación de tokens.
- [x] Generar Plan de Pruebas en `test/IT-03-test-plan-backend-auth-jwt-usuarios.md`.
- [ ] Crear rama `feature/IT-03-backend-auth-jwt-usuarios`, hacer commit y push a GitHub.
- [ ] Crear Pull Requests en GitHub para `impulsetech-be` e `impulsetech`.
- [ ] Mover tarjeta en Trello a `in testing` con el reporte final.

---

## 7. Criterios de Aceptación (Definition of Done - DoD)
- [x] Todos los tests de `pytest` pasan exitosamente sin advertencias críticas.
- [x] Endpoint `POST /api/v1/auth/login` autentica al usuario semilla `admin@impulsetech.com`.
- [x] Token JWT contiene `sub` (id de usuario), `email`, `rol` y tiempo de expiración.
- [x] Endpoints protegidos rechazan peticiones sin header `Authorization: Bearer <token>`.
- [x] Listado de ejecutivos (`/api/v1/users/ejecutivos`) responde correctamente.
- [x] Documentación interactiva Swagger en `/docs` refleja los nuevos endpoints y el esquema de seguridad Bearer.
- [ ] PRs generados y tarjeta en Trello movida a `in testing`.
