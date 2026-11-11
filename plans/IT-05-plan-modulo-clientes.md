# Plan de Implementación: [IT-05] Módulo de Clientes: Modelo DDL, CRUD en FastAPI y Directorio en Angular (Ficha 360°)

**ID de Tarjeta en Trello:** `6af35424b752e3751879fecc`  
**Rama Base:** `main` (con features de IT-01 a IT-04 integradas)  
**Ramas de Trabajo:**
- `impulsetech`: `feature/IT-05-modulo-clientes`
- `impulsetech-migration`: `feature/IT-05-modulo-clientes`
- `impulsetech-be`: `feature/IT-05-modulo-clientes`
- `impulsetech-fe`: `feature/IT-05-modulo-clientes`

---

## 1. Contexto de Negocio y Reglas (`STARTUP_CANVAS.md`)
- **Entidad `clientes`:** Representa a las personas jurídicas o naturales que contratan servicios con ImpulseTech.
- **Relación con Ejecutivos:** Cada cliente tiene **exactamente un único Ejecutivo Responsable asignado** (`ejecutivo_id` FK a `usuarios.id`).
- **Estados del Cliente:** `ACTIVO`, `INACTIVO`, `MOROSO`.
- **Ficha 360° en Frontend:** Directorio B2B con búsqueda por razón social o RIF, filtrado por estado y por ejecutivo asignado, modal/formulario para crear y editar cliente, y drawer/panel de detalle 360° con datos de contacto rápido (WhatsApp, Email, RIF, Notas y resumen de ejecutivo).

---

## 2. Especificación Técnica

### A. Base de Datos y Migración (`impulsetech-migration`)
Archivo: `db/migrations/20261110231500_create_clientes_table.sql`

```sql
-- migrate:up
CREATE TYPE estado_cliente_enum AS ENUM ('ACTIVO', 'INACTIVO', 'MOROSO');

CREATE TABLE IF NOT EXISTS clientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    razon_social VARCHAR(255) NOT NULL,
    rif_identificacion VARCHAR(50) NOT NULL UNIQUE,
    contacto_principal VARCHAR(150) NOT NULL,
    telefono_whatsapp VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    direccion_ciudad VARCHAR(255) NULL,
    ejecutivo_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE RESTRICT,
    estado estado_cliente_enum NOT NULL DEFAULT 'ACTIVO',
    notas TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clientes_ejecutivo_id ON clientes(ejecutivo_id);
CREATE INDEX idx_clientes_estado ON clientes(estado);
CREATE INDEX idx_clientes_rif ON clientes(rif_identificacion);

CREATE TRIGGER update_clientes_updated_at
BEFORE UPDATE ON clientes
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- migrate:down
DROP TRIGGER IF EXISTS update_clientes_updated_at ON clientes;
DROP TABLE IF EXISTS clientes;
DROP TYPE IF EXISTS estado_cliente_enum;
```

### B. Backend (`impulsetech-be`)
1. **Modelo SQLAlchemy** (`src/modules/clients/models.py`):
   - Mapeo de `clientes` con `SQLEnum('ACTIVO', 'INACTIVO', 'MOROSO', name='estado_cliente_enum', create_type=False)`.
   - Relación Many-to-One con `Usuario` (`ejecutivo`).
2. **Esquemas Pydantic** (`src/modules/clients/schemas.py`):
   - `ClienteBase`, `ClienteCreate`, `ClienteUpdate`, `ClienteResponse`, `ClienteDetailResponse` (incluyendo datos básicos del ejecutivo: `id`, `nombre`, `email`).
3. **Servicio y Repositorio** (`src/modules/clients/service.py`):
   - `get_clientes(db, skip, limit, search, estado, ejecutivo_id)`: búsqueda por `razon_social` o `rif_identificacion`, filtrado y paginación.
   - `get_cliente_by_id(db, cliente_id)`
   - `create_cliente(db, cliente_in, current_user)`
   - `update_cliente(db, cliente_id, cliente_in, current_user)`
   - `delete_cliente(db, cliente_id, current_user)` (o cambio a inactivo).
4. **Router REST** (`src/modules/clients/router.py`):
   - `GET /api/v1/clients`: Lista filtrable y paginada.
   - `GET /api/v1/clients/{id}`: Ficha 360° individual.
   - `POST /api/v1/clients`: Crear nuevo cliente (Admin o Ejecutivo).
   - `PUT /api/v1/clients/{id}`: Actualizar datos de cliente.
   - `DELETE /api/v1/clients/{id}`: Eliminar cliente (Solo Admin).
5. **Registro en FastAPI**:
   - Incluir `clients_router` en `src/main.py`.

### C. Frontend (`impulsetech-fe`)
1. **Modelos TypeScript** (`core/models/client.model.ts`):
   - Interfaces `Cliente`, `ClienteCreate`, `ClienteUpdate`, `EstadoCliente`.
2. **Servicio Angular** (`core/services/client.service.ts`):
   - Métodos HTTP reactivos para `getClients(params)`, `getClientById(id)`, `createClient(data)`, `updateClient(id, data)`, `deleteClient(id)`.
3. **Módulo de Clientes**:
   - `modules/clients/client-list/`:
     - Tabla B2B densa y limpia (Razón Social, RIF, Contacto, Teléfono con link directo a WhatsApp, Ejecutivo asignado, Estado con badge semáforo).
     - Buscador reactivo en tiempo real y selector de filtro por estado.
     - Botón de acción destacado "Nuevo Cliente".
   - `modules/clients/client-form-modal/`:
     - Modal accesible para crear o editar cliente con Reactive Forms.
     - Dropdown para seleccionar el Ejecutivo Responsable (cargado desde `/api/v1/users`).
   - `modules/clients/client-detail/`:
     - Drawer / Panel lateral Ficha 360° con desglose de datos, notas operativas, accesos rápidos y secciones preparadas para próximos servicios y pagos.
4. **Actualización de Navegación**:
   - Activar el enlace "Clientes" en el Sidebar del Shell privado (`layout/shell`).
   - Agregar rutas en `app.routes.ts` (`/clients`).

---

## 3. Pruebas y Verificación
- **Migración DDL:**
  - Ejecutar `docker compose run --rm migration up` y verificar creación correcta de tabla `clientes` y triggers.
- **Backend Tests (`pytest`):**
  - Test de creación de cliente con asignación de ejecutivo.
  - Test de listado y filtros (por búsqueda de RIF/razón social y por estado).
  - Test de validación de RIF duplicado.
  - Test de actualización y eliminación.
- **Frontend Build (`npm run build`):**
  - Compilación limpia sin errores de tipos ni estilos.
  - Verificación visual de tabla, modal y drawer según `frontend-design`.

---

## 4. Checklist de Ejecución
- [x] Crear ramas `feature/IT-05-modulo-clientes` en los 4 repositorios.
- [x] Escribir y aplicar migración DDL `20261110231500_create_clientes_table.sql`.
- [x] Desarrollar modelos, esquemas, servicios y router de Clientes en `impulsetech-be`.
- [x] Escribir tests unitarios/integración en `impulsetech-be/tests/test_clients.py` y validar con pytest.
- [x] Desarrollar componentes de Directorio y Ficha 360° en `impulsetech-fe` con plantillas HTML separadas.
- [x] Enlazar ruta `/clients` en el Shell y validar con `npm run build`.
- [x] Generar Plan de Pruebas `test/IT-05-test-plan-modulo-clientes.md`.
- [x] Crear Pull Requests en GitHub y mover tarjeta a `in testing`.
