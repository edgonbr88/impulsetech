# Plan de Implementación: [IT-11] Dashboard Gerencial y Operativo: KPIs de Leads, Clientes, Servicios Activos y Cobranzas

- **ID de la Historia:** `IT-11`
- **Trello Card ID:** `6af35426318625db501afb78`
- **Fase:** Fase 5 - Panel de Control Unificado y Métricas Ejecutivas
- **Responsable:** ImpulseTech Engineering Team
- **Fecha:** 2026-11-11

---

## 1. Contexto y Objetivos

El sistema de gestión de ImpulseTech cuenta con sus módulos core operativos:
1. `clientes`: Cartera de clientes activos, inactivos y morosos.
2. `leads`: Embudos de venta especializados (`LEGAL_SAREN`, `IA_AUTOMATIZACION`, `SOFTWARE_MEDIDA`) con métricas de conversión.
3. `servicios`: Contratos operativos con modalidades (`PROYECTO_UNICO` vs `RECURRENTE_MENSUAL`) y estados de ejecución (`EN_ESPERA`, `EN_DESARROLLO`, `EN_REVISION`, `ACTIVO_PRODUCCION`, `FINALIZADO`, `PAUSADO`).
4. `pagos`: Recaudación multimoneda (`USD`, `VES`, `USDT`), tasa BCV y conciliación bancaria (`VERIFICADO`, `PENDIENTE`, `RECHAZADO`).

**Objetivo de `IT-11`:**
Construir el **Dashboard Gerencial y Operativo** consolidado en FastAPI y Angular 18, presentando:
- **KPIs Comerciales**: Total Leads, Tasa de Conversión (Leads Ganados vs Totales), Pipeline Activo en USD.
- **KPIs Operativos**: Clientes Activos, Servicios en Producción/Desarrollo, Retainers Mensuales Activos (MRR recurrente estimado).
- **KPIs Financieros**: Total Recaudado Verificado (USD), Cuentas por Conciliar (USD), Cobranzas en Bolívares y Cripto.
- **Actividad Reciente y Alertas de Cartera**: Últimos pagos registrados, servicios próximos a entrega y leads calificados.
- Cumplimiento riguroso de la directriz de interfaz sobria B2B `frontend-design`.

### Criterios de Aceptación (DoD):
1. **Backend (FastAPI):**
   - Endpoint `GET /api/v1/dashboard/metrics`:
     - Retorna KPIs consolidados: `leads` (total, ganados, tasa conversión, pipeline USD), `clientes` (total, activos, morosos), `servicios` (total activos, proyectos en curso, retainers activos, MRR estimado), `finanzas` (total verificado USD, total pendiente USD, desglose multimoneda).
     - Retorna listas de actividad reciente: últimos 5 pagos, últimos 5 leads y servicios activos.
   - Pruebas automatizadas en `tests/test_dashboard.py` (suite total de backend superando los 17 tests).
2. **Frontend (Angular 18):**
   - Servicio `DashboardService` para consultar métricas.
   - Actualización completa de `DashboardHomeComponent` (`src/app/modules/dashboard/home/`):
     - Plantilla `dashboard-home.component.html` y estilos `dashboard-home.component.scss` desacoplados.
     - Sección de métricas estratégicas con diseño intencional y tarjetas de alta densidad de información.
     - Gráficos o barras de distribución de embudos y monedas usando SVG y Tailwind CSS.
     - Tablas de actividad reciente con enlaces de navegación rápida a clientes, leads, servicios y finanzas.
   - Compilación limpia sin errores (`npm run build`).
3. **Documentación y Entrega:**
   - Plan de pruebas en `test/IT-11-test-plan-dashboard-gerencial.md`.
   - PRs en backend, frontend y repositorio orquestador.
   - Tarjeta movida a `in testing` en Trello.

---

## 2. Plan Paso a Paso de Ejecución

### Paso 1: Backend en `impulsetech-be`
- Crear rama `feature/IT-11-dashboard-gerencial`.
- Diseñar módulo `src/modules/dashboard/` con esquemas `schemas.py`, servicio `service.py` y router `router.py`.
- Integrar router en `src/main.py` (`/api/v1/dashboard`).
- Crear pruebas en `tests/test_dashboard.py`.
- Ejecutar suite completa con pytest y verificar verde.
- Commit, push y crear PR en GitHub.

### Paso 2: Frontend en `impulsetech-fe`
- Crear rama `feature/IT-11-dashboard-gerencial`.
- Diseñar interfaces en `src/app/core/models/dashboard.model.ts`.
- Crear servicio `src/app/core/services/dashboard.service.ts`.
- Rediseñar `DashboardHomeComponent` con HTML/SCSS separados, visualización de MRR, pipeline, embudos y accesos directos.
- Ejecutar `npm run build` y validar ausencia de errores.
- Commit, push y crear PR en GitHub.

### Paso 3: Orquestador y Cierre
- Crear `test/IT-11-test-plan-dashboard-gerencial.md`.
- Actualizar checklist en este plan.
- Commit y push en repositorio principal `impulsetech` y abrir PR.
- Ejecutar script de movimiento a `in testing` en Trello.

---

## 3. Checklist de Control

- [x] Endpoint REST `GET /api/v1/dashboard/metrics` en FastAPI testeado con pytest.
- [x] Suite de backend con 17+ tests unitarios y de integración en verde.
- [x] Interfaz del Dashboard en Angular 18 rediseñada con `frontend-design`, métricas B2B, MRR y actividad reciente.
- [x] Componente con plantillas HTML y estilos SCSS separados.
- [x] Compilación limpia con `npm run build`.
- [x] Plan de pruebas documentado en `test/IT-11-test-plan-dashboard-gerencial.md`.
- [x] PRs creados en GitHub y tarjeta movida a `in testing`.
