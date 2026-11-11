# Plan de Implementación: [IT-07] Módulo de Leads: DDL y Embudos Especializados (Legal SAREN, IA/Automatización, Software a Medida)

**ID de Tarjeta en Trello:** `6af35425c5a30765656667e2`  
**Rama Base:** `feature/IT-06-asignacion-ejecutivos-cartera` (o `main`)  
**Ramas de Trabajo:**
- `impulsetech`: `feature/IT-07-modulo-leads-embudos`
- `impulsetech-migration`: `feature/IT-07-modulo-leads-embudos`
- `impulsetech-be`: `feature/IT-07-modulo-leads-embudos`
- `impulsetech-fe`: `feature/IT-07-modulo-leads-embudos`

---

## 1. Contexto de Negocio y Reglas (`STARTUP_CANVAS.md`)
- **Entidad `leads`:** Registra las oportunidades comerciales entrantes antes de ser clientes formalizados.
- **3 Embudos Especializados:**
  1. `LEGAL_SAREN`: Constitución de empresas, actas de asambleas, poderes, trámites registrales y notariales.
  2. `IA_AUTOMATIZACION`: Agentes de atención/ventas, chatbots para WhatsApp, automatización de flujos B2B.
  3. `SOFTWARE_MEDIDA`: Desarrollo de plataformas web a medida, CRMs, ERPs e integraciones cloud.
- **Etapas Comerciales:**
  - `NUEVO`
  - `DIAGNOSTICO`
  - `PROPUESTA`
  - `NEGOCIACION`
  - `GANADO` (habilitará la conversión a cliente en IT-08)
  - `PERDIDO` (con `motivo_perdida`)
- **Asignación y Cartera:**
  - Cada lead tiene un ejecutivo asignado (`ejecutivo_asignado_id` FK a `usuarios.id`).
  - Cada lead tiene un `valor_estimado_usd` (decimal).
  - Puede vincularse opcionalmente a un `cliente_id` existente (para venta cruzada o nuevos servicios).

---

## 2. Especificación Técnica

### A. Base de Datos y Migración (`impulsetech-migration`)
Archivo: `db/migrations/20261111084500_create_leads_table.sql`

```sql
-- migrate:up
CREATE TYPE embudo_lead_enum AS ENUM ('LEGAL_SAREN', 'IA_AUTOMATIZACION', 'SOFTWARE_MEDIDA');
CREATE TYPE etapa_lead_enum AS ENUM ('NUEVO', 'DIAGNOSTICO', 'PROPUESTA', 'NEGOCIACION', 'GANADO', 'PERDIDO');

CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre_contacto VARCHAR(150) NOT NULL,
    empresa_o_proyecto VARCHAR(200) NOT NULL,
    telefono_whatsapp VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    embudo embudo_lead_enum NOT NULL,
    etapa etapa_lead_enum NOT NULL DEFAULT 'NUEVO',
    motivo_perdida TEXT NULL,
    valor_estimado_usd NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    ejecutivo_asignado_id UUID NOT NULL REFERENCES usuarios(id) ON DELETE RESTRICT,
    cliente_id UUID NULL REFERENCES clientes(id) ON DELETE SET NULL,
    notas TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_leads_embudo ON leads(embudo);
CREATE INDEX idx_leads_etapa ON leads(etapa);
CREATE INDEX idx_leads_ejecutivo_asignado_id ON leads(ejecutivo_asignado_id);
CREATE INDEX idx_leads_cliente_id ON leads(cliente_id);

CREATE TRIGGER update_leads_updated_at
BEFORE UPDATE ON leads
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- migrate:down
DROP TRIGGER IF EXISTS update_leads_updated_at ON leads;
DROP TABLE IF EXISTS leads;
DROP TYPE IF EXISTS etapa_lead_enum;
DROP TYPE IF EXISTS embudo_lead_enum;
```

### B. Backend (`impulsetech-be`)
1. **Modelos SQLAlchemy (`src/modules/leads/models.py`):**
   - Mapeo ORM con enums `embudo_lead_enum` y `etapa_lead_enum`.
   - Relación con `Usuario` (`ejecutivo_asignado`) y `Cliente` (`cliente`).
2. **Esquemas Pydantic (`src/modules/leads/schemas.py`):**
   - `LeadBase`, `LeadCreate`, `LeadUpdate`, `LeadResponse`, `LeadStageUpdate`.
3. **Servicios (`src/modules/leads/service.py`):**
   - `get_leads(db, skip, limit, embudo, etapa, ejecutivo_id, search, solo_mi_cartera)`
   - `get_lead_by_id(db, lead_id)`
   - `create_lead(db, lead_in)`
   - `update_lead(db, lead_id, lead_in)`
   - `update_lead_stage(db, lead_id, etapa, motivo_perdida)`
   - `delete_lead(db, lead_id)`
4. **Router (`src/modules/leads/router.py`):**
   - `GET /api/v1/leads`: Lista y filtros por embudo, etapa, ejecutivo y búsqueda.
   - `GET /api/v1/leads/{id}`: Detalle de lead.
   - `POST /api/v1/leads`: Registro de nuevo lead.
   - `PUT /api/v1/leads/{id}`: Actualización completa.
   - `PATCH /api/v1/leads/{id}/stage`: Cambio rápido de etapa comercial.
   - `DELETE /api/v1/leads/{id}`: Eliminación (Solo Admin).
5. **Registro en `src/main.py`:**
   - Registrar `leads_router` bajo `/api/v1`.
6. **Tests Automatizados (`tests/test_leads.py`):**
   - Creación en cada uno de los 3 embudos.
   - Transición de etapas (`NUEVO` -> `DIAGNOSTICO` -> `PERDIDO` con motivo).
   - Filtrado por embudo (`embudo=LEGAL_SAREN`).

### C. Frontend (`impulsetech-fe`)
1. **Modelos TypeScript (`core/models/lead.model.ts`):**
   - Interfaces `Lead`, `LeadCreate`, `LeadUpdate`, `EmbudoLead`, `EtapaLead`.
2. **Servicio (`core/services/lead.service.ts`):**
   - Métodos HTTP reactivos para leads con soporte de filtros.
3. **Directorio y Gestión de Leads (`modules/leads/lead-list/`):**
   - Pestañas superiores para segmentar por los 3 Embudos Especializados:
     - ⚖️ Legal SAREN
     - 🤖 IA & Automatización
     - 💻 Software a Medida
   - Badges estilizados por Etapa comercial y valor estimado en USD.
   - Modal para crear y editar Leads (formulario con Reactive Forms y selección de embudo/ejecutivo).
4. **Navegación:**
   - Activar enlace "Leads & Embudos" en el Sidebar del Shell privado.
   - Configurar ruta `/leads` en `app.routes.ts`.

---

## 3. Pruebas y Criterios de Aceptación (DoD)
- [x] Migración DDL ejecutada con dbmate (`leads`, `embudo_lead_enum`, `etapa_lead_enum`).
- [x] Endpoints REST y CRUD de Leads en FastAPI con filtros por los 3 embudos probados con pytest.
- [x] Componente en Angular 18 con separación de plantillas HTML/SCSS, tabs de embudos y modal de captura de leads.
- [x] Compilación de producción `npm run build` limpia.
- [x] Plan de pruebas documentado en `test/IT-07-test-plan-modulo-leads.md`.
- [x] PRs creados en GitHub y tarjeta movida a `in testing`.
