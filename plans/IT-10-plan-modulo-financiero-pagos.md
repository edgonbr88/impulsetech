# Plan de Implementación: [IT-10] Módulo Financiero Multimoneda: DDL de Pagos, Métodos Locales (Zelle, Pago Móvil, USDT) y Cuentas por Cobrar

- **ID de la Historia:** `IT-10`
- **Trello Card ID:** `6af35426532b5210014919ae`
- **Fase:** Fase 5 - Módulo Financiero Multimoneda y Cobranzas
- **Responsable:** ImpulseTech Engineering Team
- **Fecha:** 2026-11-11

---

## 1. Contexto y Objetivos

En el ecosistema B2B de Venezuela (definido en `STARTUP_CANVAS.md`), la gestión financiera exige operar en un esquema multimoneda riguroso:
- Facturación y precios de referencia en dólares americanos (`USD`).
- Cobros en bolívares (`VES`) vinculados a la tasa oficial del Banco Central de Venezuela (`tasa_cambio_bcv`).
- Criptoactivos estables (`USDT` / Binance).
- Métodos locales imprescindibles: `PAGO_MOVIL`, `TRANSFERENCIA_VES`, `ZELLE`, `USDT_BINANCE`, `EFECTIVO_USD`.
- Estados de conciliación: `PENDIENTE`, `VERIFICADO`, `RECHAZADO`.
- Conceptos de pago: `ANTICIPO_50`, `FINIQUITO`, `CUOTA_RETAINER`, `OTRO`.
- Vinculación opcional a un contrato operativo (`servicio_id`) y obligatoria al cliente (`cliente_id`).

### Criterios de Aceptación (DoD):
1. **Migración DDL (`dbmate`):**
   - Enums: `moneda_pago_enum` (`USD`, `VES`, `USDT`), `medio_pago_enum` (`ZELLE`, `PAGO_MOVIL`, `USDT_BINANCE`, `EFECTIVO_USD`, `TRANSFERENCIA_VES`), `concepto_pago_enum` (`ANTICIPO_50`, `FINIQUITO`, `CUOTA_RETAINER`, `OTRO`), `estado_pago_enum` (`PENDIENTE`, `VERIFICADO`, `RECHAZADO`).
   - Tabla `pagos` con claves foráneas indexadas a `clientes` y `servicios`.
2. **Backend (FastAPI):**
   - Modelo SQLAlchemy `Pago` con relaciones hacia `Cliente` y `Servicio`.
   - Esquemas Pydantic con validación: si la moneda es `VES`, `tasa_cambio_bcv` debe ser mayor a 0; cálculo del equivalente en USD (`monto_equivalente_usd`).
   - Endpoints:
     - `POST /api/v1/payments`: Registrar nuevo pago.
     - `GET /api/v1/payments`: Listado con filtros por cliente, servicio, moneda, estado, rango de fechas y paginación.
     - `GET /api/v1/payments/{id}`: Detalle de pago.
     - `PATCH /api/v1/payments/{id}/status`: Actualizar estado de verificación (`VERIFICADO`, `RECHAZADO`, `PENDIENTE`) con notas de conciliación.
     - `GET /api/v1/payments/summary/balance`: Métricas resumidas de cobranza (total verificado USD, total pendiente USD, desglose por moneda).
   - Pruebas automatizadas con pytest en verde (mínimo 18 tests acumulados en backend).
3. **Frontend (Angular 18):**
   - Modelos e interfaces TypeScript (`Payment`, enums).
   - Servicio `PaymentService` consumiendo API REST.
   - Componente `PaymentListComponent` bajo directrices de `frontend-design`:
     - Pestañas por estado / moneda.
     - Tarjetas KPI: Total Recaudado (USD), Pagos Pendientes por Conciliar, Cobranzas del Mes.
     - Tabla con badges de método de pago, moneda, tasa BCV y estado.
     - Modal para registrar nuevo pago con validaciones condicionales (tasa BCV si moneda es VES).
     - Modal de verificación rápida (Aprobar / Rechazar con motivo).
     - Separación estricta de plantilla HTML y estilos SCSS.
4. **Verificación y PRs:**
   - Compilación exitosa en Angular (`npm run build`).
   - Plan de pruebas documentado en `test/IT-10-test-plan-modulo-financiero-pagos.md`.
   - Creación de ramas y PRs en GitHub.
   - Movimiento de la tarjeta a `in testing` en Trello.

---

## 2. Plan Paso a Paso de Ejecución

### Paso 1: Migración DDL en `impulsetech-migration`
- Crear rama `feature/IT-10-modulo-financiero-pagos`.
- Crear migración `db/migrations/20261111100000_create_pagos_table.sql`.
- Aplicar con `dbmate up` y verificar en base de datos.
- Commit, push y PR en GitHub.

### Paso 2: Backend en `impulsetech-be`
- Crear rama `feature/IT-10-modulo-financiero-pagos`.
- Definir enums y modelo `Pago` en `src/modules/payments/models.py`.
- Crear esquemas Pydantic en `src/modules/payments/schemas.py`.
- Crear capa de servicio en `src/modules/payments/service.py` con lógica de cálculo de equivalentes USD y conciliación.
- Crear router en `src/modules/payments/router.py` e incluirlo en `src/main.py`.
- Escribir suite de pruebas en `tests/test_payments.py`.
- Ejecutar `pytest` y verificar cobertura de reglas de negocio.
- Commit, push y PR en GitHub.

### Paso 3: Frontend en `impulsetech-fe`
- Crear rama `feature/IT-10-modulo-financiero-pagos`.
- Crear interfaces en `src/app/core/models/payment.model.ts`.
- Crear servicio `src/app/core/services/payment.service.ts`.
- Crear componente `src/app/modules/payments/payment-list/` con HTML y SCSS separados.
- Integrar enrutamiento en `app.routes.ts` y enlace de navegación en `navbar.component.html`.
- Ejecutar `npm run build` y corregir cualquier error.
- Commit, push y PR en GitHub.

### Paso 4: Cierre, Documentación y Trello
- Crear `test/IT-10-test-plan-modulo-financiero-pagos.md`.
- Actualizar checklist en este plan.
- Crear PR en el repositorio orquestador `impulsetech`.
- Mover tarjeta a `in testing` con script de Trello.

---

## 3. Checklist de Control

- [x] Migración DDL de tabla `pagos` y enums ejecutada con dbmate.
- [x] Endpoints REST en FastAPI testeados con pytest (18+ tests en verde).
- [x] Frontend Angular 18 con vista financiera, KPIs, filtros y modales de registro/conciliación.
- [x] Componente integrado con plantillas HTML/SCSS separadas cumpliendo `frontend-design`.
- [x] Compilación limpia con `npm run build`.
- [x] Plan de pruebas documentado en `test/IT-10-test-plan-modulo-financiero-pagos.md`.
- [x] PRs creados en GitHub y tarjeta movida a `in testing`.
