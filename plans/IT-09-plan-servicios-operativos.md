# Plan de Implementación: [IT-09] Módulo de Servicios Operativos: DDL, Hitos de Entrega y Ciclo de Vida Independiente por Cliente

**ID de Tarjeta en Trello:** `6af354256f60320cc74dd125`  
**Rama Base:** `feature/IT-08-kanban-leads-conversion` (o `main`)  
**Ramas de Trabajo:**
- `impulsetech`: `feature/IT-09-modulo-servicios-operativos`
- `impulsetech-migration`: `feature/IT-09-modulo-servicios-operativos`
- `impulsetech-be`: `feature/IT-09-modulo-servicios-operativos`
- `impulsetech-fe`: `feature/IT-09-modulo-servicios-operativos`

---

## 1. Contexto de Negocio y Reglas (`STARTUP_CANVAS.md`)
- **Entidad `servicios`:** Contratos operativos suscritos entre ImpulseTech y sus clientes.
- **Tipos de Servicio:**
  - `LEGAL_SAREN`: Trámites registrales y notariales.
  - `IA_AUTOMATIZACION`: Soluciones de agentes de IA y automatización.
  - `SOFTWARE_MEDIDA`: Desarrollo de software y aplicaciones web.
  - `RETAINER_MENSUAL`: Soporte continuo, mantenimiento o igualas legales/tecnológicas mensuales.
- **Modalidades de Contratación:**
  - `PROYECTO_UNICO`: Tiene fecha estimada de entrega y culmina con hito final.
  - `RECURRENTE_MENSUAL`: Servicios tipo iguala con `dia_corte_mensual` (1 al 31) para facturación y renovación periódica.
- **Ciclo de Vida Operativo (`estado_operativo`):**
  - `EN_ESPERA` (esperando anticipo o recaudos iniciales)
  - `EN_DESARROLLO` (ejecución técnica o gestiones ante registro)
  - `EN_REVISION` (validación interna o revisión con cliente)
  - `ACTIVO_PRODUCCION` (operativo para retainers o software en vivo)
  - `FINALIZADO` (servicio entregado formalmente)
  - `PAUSADO` (bloqueado por falta de recaudos, morosidad o solicitud del cliente)
- **Regla de Negocio Canónica:**
  - **Un cliente puede tener múltiples servicios activos en paralelo.**
  - Cada servicio tiene su especialista asignado (texto libre para gestor de campo, abogado o desarrollador), cronograma independiente y monto pactado en USD.

---

## 2. Especificación Técnica

### A. Base de Datos y Migración (`impulsetech-migration`)
Archivo: `db/migrations/20261111091500_create_servicios_table.sql`

```sql
-- migrate:up
CREATE TYPE tipo_servicio_enum AS ENUM ('LEGAL_SAREN', 'IA_AUTOMATIZACION', 'SOFTWARE_MEDIDA', 'RETAINER_MENSUAL');
CREATE TYPE modalidad_servicio_enum AS ENUM ('PROYECTO_UNICO', 'RECURRENTE_MENSUAL');
CREATE TYPE estado_operativo_servicio_enum AS ENUM ('EN_ESPERA', 'EN_DESARROLLO', 'EN_REVISION', 'ACTIVO_PRODUCCION', 'FINALIZADO', 'PAUSADO');

CREATE TABLE IF NOT EXISTS servicios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    tipo tipo_servicio_enum NOT NULL,
    nombre_servicio VARCHAR(200) NOT NULL,
    modalidad modalidad_servicio_enum NOT NULL DEFAULT 'PROYECTO_UNICO',
    estado_operativo estado_operativo_servicio_enum NOT NULL DEFAULT 'EN_ESPERA',
    especialista_responsable VARCHAR(150) NOT NULL,
    monto_pactado_usd NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    fecha_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_entrega_estimada DATE NULL,
    dia_corte_mensual SMALLINT NULL CHECK (dia_corte_mensual BETWEEN 1 AND 31),
    notas TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_servicios_cliente_id ON servicios(cliente_id);
CREATE INDEX idx_servicios_tipo ON servicios(tipo);
CREATE INDEX idx_servicios_modalidad ON servicios(modalidad);
CREATE INDEX idx_servicios_estado_operativo ON servicios(estado_operativo);

CREATE TRIGGER update_servicios_updated_at
BEFORE UPDATE ON servicios
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- migrate:down
DROP TRIGGER IF EXISTS update_servicios_updated_at ON servicios;
DROP TABLE IF EXISTS servicios;
DROP TYPE IF EXISTS estado_operativo_servicio_enum;
DROP TYPE IF EXISTS modalidad_servicio_enum;
DROP TYPE IF EXISTS tipo_servicio_enum;
```

### B. Backend (`impulsetech-be`)
1. **Modelos SQLAlchemy (`src/modules/services/models.py`):**
   - Mapeo ORM con enums `tipo_servicio_enum`, `modalidad_servicio_enum`, `estado_operativo_servicio_enum`.
   - Relación ForeignKey con `Cliente`.
2. **Esquemas Pydantic (`src/modules/services/schemas.py`):**
   - `ServicioBase`, `ServicioCreate`, `ServicioUpdate`, `ServicioStatusUpdate`, `ServicioResponse`.
3. **Servicios (`src/modules/services/service.py`):**
   - CRUD de servicios con filtros por `cliente_id`, `tipo`, `modalidad`, `estado_operativo` y búsqueda.
   - Validación de existencia de cliente y consistencia de `dia_corte_mensual` en modalidad recurrente.
4. **Router (`src/modules/services/router.py`):**
   - `GET /api/v1/services`: Matriz operativa global.
   - `GET /api/v1/services/{id}`: Detalle de servicio.
   - `POST /api/v1/services`: Contratar/abrir nuevo servicio para un cliente.
   - `PUT /api/v1/services/{id}`: Actualización técnica y contractual.
   - `PATCH /api/v1/services/{id}/status`: Transición de estado operativo.
   - `DELETE /api/v1/services/{id}`: Eliminación (Solo Admin).
5. **Registro en `src/main.py`:**
   - Registrar `services_router` bajo `/api/v1`.
6. **Tests Automatizados (`tests/test_services.py`):**
   - Creación de servicio para cliente existente.
   - Filtrado por modalidad (`PROYECTO_UNICO` vs `RECURRENTE_MENSUAL`).
   - Transición de estado (`EN_ESPERA` -> `EN_DESARROLLO` -> `ACTIVO_PRODUCCION`).

### C. Frontend (`impulsetech-fe`)
1. **Modelos TypeScript (`core/models/service.model.ts`):**
   - Interfaces `Servicio`, `ServicioCreate`, `ServicioUpdate`, `TipoServicio`, `ModalidadServicio`, `EstadoOperativoServicio`.
2. **Servicio (`core/services/service-contracts.service.ts`):**
   - Métodos HTTP reactivos para `getServices()`, `createService()`, `updateService()`, `updateServiceStatus()`, `deleteService()`.
3. **Módulo de Servicios Operativos (`modules/services/service-list/`):**
   - Matriz de seguimiento operativo de servicios activos con badges de estado y modalidad.
   - Filtros por Modalidad (Todos, Proyectos Únicos, Retainers Mensuales) y Estado Operativo.
   - Modal accesible para aperturar o editar contratos de servicio asociados a clientes.
4. **Integración con la Ficha 360° del Cliente (`modules/clients/`):**
   - En el Drawer 360° de Clientes, habilitar la sección de servicios mostrando los contratos vinculados al cliente seleccionado y botón para agregar nuevo servicio.
5. **Navegación:**
   - Activar el enlace "Servicios" en el Sidebar del Shell privado (`layout/shell`).
   - Configurar ruta `/services` en `app.routes.ts`.

---

## 3. Pruebas y Criterios de Aceptación (DoD)
- [x] Migración DDL de tabla `servicios` y enums ejecutada con dbmate.
- [x] Endpoints REST en FastAPI testeados con pytest (15+ tests en verde).
- [x] Frontend Angular 18 con vista de matriz de servicios, filtros y formulario modal reactivo.
- [x] Componente integrado con plantillas HTML/SCSS separadas cumpliendo `frontend-design`.
- [x] Compilación limpia con `npm run build`.
- [x] Plan de pruebas documentado en `test/IT-09-test-plan-servicios-operativos.md`.
- [x] PRs creados en GitHub y tarjeta movida a `in testing`.
