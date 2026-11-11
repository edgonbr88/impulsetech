# Plan de Implementación: [IT-08] Vistas Kanban de Embudos de Venta y Acción de Conversión Lead -> Cliente en Angular

**ID de Tarjeta en Trello:** `6af35425e01d867c7da63c99`  
**Rama Base:** `feature/IT-07-modulo-leads-embudos` (o `main`)  
**Ramas de Trabajo:**
- `impulsetech`: `feature/IT-08-kanban-leads-conversion`
- `impulsetech-be`: `feature/IT-08-kanban-leads-conversion`
- `impulsetech-fe`: `feature/IT-08-kanban-leads-conversion`

---

## 1. Contexto de Negocio y Reglas (`STARTUP_CANVAS.md`)
- **Tablero Kanban por Embudo:** Los leads se visualizan en columnas por etapa comercial:
  1. `NUEVO`
  2. `DIAGNOSTICO`
  3. `PROPUESTA`
  4. `NEGOCIACION`
  5. `GANADO`
  6. `PERDIDO`
- Cada tarjeta en el Kanban muestra: Contacto, Empresa/Proyecto, Valor Estimado (USD), WhatsApp directo, Ejecutivo asignado y botones de avance rápido entre etapas.
- **Acción de Conversión (`Lead -> Cliente`):**
  - Cuando un lead alcanza la etapa `GANADO` o el usuario pulsa **"Convertir en Cliente"**:
    - Se despliega un modal / se ejecuta la acción que recopila o confirma los datos de persona jurídica/natural: Razón Social (pre-llenada con `empresa_o_proyecto`), RIF/Identificación fiscal, Contacto, Teléfono, Email, Ejecutivo y notas.
    - Se crea el registro en la tabla `clientes`.
    - Se actualiza el `cliente_id` en el `lead` y su etapa pasa a `GANADO`.
    - Retorna el cliente creado y actualiza el estado comercial.

---

## 2. Especificación Técnica

### A. Backend (`impulsetech-be`)
1. **Esquema de Conversión (`src/modules/leads/schemas.py`):**
   - `LeadConvertToClientRequest`:
     - `rif_identificacion`: str (obligatorio para la creación de la empresa en BD).
     - `razon_social`: str | None (si no se envía, toma `lead.empresa_o_proyecto`).
     - `direccion_ciudad`: str | None.
     - `notas_adicionales`: str | None.
   - `LeadConvertToClientResponse`:
     - `lead`: `LeadResponse`
     - `cliente_id`: UUID
     - `razon_social`: str
     - `message`: str
2. **Servicio (`src/modules/leads/service.py`):**
   - `convert_lead_to_client(db, lead_id, convert_in, current_user)`:
     - Valida que el lead exista.
     - Si el lead ya tiene `cliente_id`, valida que no se duplique innecesariamente.
     - Valida unicidad del RIF contra la tabla `clientes`.
     - Crea la entidad `Cliente` asignada al mismo ejecutivo (`ejecutivo_asignado_id`).
     - Actualiza el lead con `cliente_id = nuevo_cliente.id` y `etapa = 'GANADO'`.
     - Realiza el commit y retorna respuesta unificada.
3. **Router (`src/modules/leads/router.py`):**
   - `POST /api/v1/leads/{lead_id}/convert-to-client`: Endpoint de conversión.
4. **Tests en Pytest (`tests/test_leads.py`):**
   - Test del flujo de conversión: crear lead -> llamar `convert-to-client` -> verificar que se crea el cliente, que el lead tiene `cliente_id` y etapa `GANADO`.

### B. Frontend (`impulsetech-fe`)
1. **Vista Kanban (`modules/leads/lead-kanban/` o vista dual Lista/Kanban en `lead-list`):**
   - Selector de vista en la cabecera: **[ Vista Tabla ]** / **[ Tablero Kanban ]**.
   - Selector de Embudo activo (`Legal SAREN`, `IA & Automatización`, `Software a Medida`).
   - Columnas del Kanban correspondientes a las 6 etapas:
     - `NUEVO` (Azul)
     - `DIAGNOSTICO` (Púrpura)
     - `PROPUESTA` (Ámbar)
     - `NEGOCIACION` (Cian)
     - `GANADO` (Esmeralda)
     - `PERDIDO` (Rosa/Rojo)
   - Resumen en el encabezado de cada columna: número de oportunidades y monto total acumulado en USD.
   - Botones rápidos en la tarjeta para mover a la siguiente etapa o marcar como perdido.
2. **Modal de Conversión a Cliente:**
   - Si se pulsa "Convertir en Cliente" o se mueve a "GANADO", se abre modal solicitando el RIF fiscal de la empresa.
   - Al confirmar, llama a `leadService.convertLeadToClient(leadId, data)`.
   - Notificación de éxito con enlace directo a la ficha del nuevo cliente.
3. **Integración con Servicios (`lead.service.ts`):**
   - Método `convertLeadToClient(leadId, data)`.

---

## 3. Pruebas y Criterios de Aceptación (DoD)
- [x] Backend: Endpoint `POST /api/v1/leads/{id}/convert-to-client` implementado y probado con pytest.
- [x] Frontend: Vista Kanban interactiva con las 6 etapas y métricas de monto por columna.
- [x] Frontend: Selector de vista Dual (Tabla / Kanban) persistente o reactivo.
- [x] Frontend: Modal de conversión a cliente con prellenado de datos y validación de RIF.
- [x] Compilación limpia con `npm run build`.
- [x] Plan de pruebas documentado en `test/IT-08-test-plan-kanban-conversion.md`.
- [x] PRs creados en GitHub y tarjeta movida a `in testing`.
