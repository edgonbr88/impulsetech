# Plan de Pruebas: [IT-11] Dashboard Gerencial y Operativo

- **ID de la Historia:** `IT-11`
- **Trello Card ID:** `6af35426318625db501afb78`
- **Módulo:** Dashboard Unificado, KPIs Ejecutivos y Reportes Operativos
- **Fecha de Ejecución:** 2026-11-11
- **Responsable:** ImpulseTech Core Platform Team / AI Assistant

---

## 1. Alcance y Objetivos de la Prueba

Validar el panel de control centralizado (Dashboard Gerencial y Operativo) integrando todos los subsistemas desarrollados en las Fases 1 a 5:
1. Métricas comerciales: Total de leads, tasa de conversión (%) y valor consolidado del pipeline en USD.
2. Salud de cartera de clientes: Cartera total, desglose de clientes activos, morosos e inactivos.
3. Desempeño de servicios: Proyectos únicos en curso, retainers recurrentes mensuales activos y cálculo de **MRR (Monthly Recurring Revenue)**.
4. Finanzas multimoneda: Recaudación verificada en USD, fondos pendientes por conciliar y desglose por divisas (USD, VES, USDT).
5. Actividad reciente: Feeds de últimos pagos, prospectos captados y servicios en desarrollo.

---

## 2. Pruebas Automatizadas de Backend (FastAPI + Pytest)

Se ejecutó la suite completa de pruebas unitarias y de integración sobre PostgreSQL local en Docker.

### Comando ejecutado:
```bash
docker compose exec backend pytest
```

### Resultados:
```text
tests/test_auth.py ........                                              [ 47%]
tests/test_clients.py ..                                                 [ 58%]
tests/test_dashboard.py .                                                [ 64%]
tests/test_health.py ..                                                  [ 76%]
tests/test_leads.py ..                                                   [ 88%]
tests/test_payments.py .                                                 [ 94%]
tests/test_services.py .                                                 [100%]

======================= 17 passed, 7 warnings in 18.07s ========================
```

- **Total Tests:** 17
- **Passed:** 17
- **Failed:** 0
- **Validaciones Clave en `test_dashboard.py`:**
  - Consulta exitosa de `GET /api/v1/dashboard/metrics` con token JWT de usuario autenticado.
  - Comprobación de tipos de datos: enteros para conteos, decimales/flotantes para MRR y pipeline, y arreglos para actividad reciente.

---

## 3. Pruebas de Compilación y Frontend (Angular 18)

Se ejecutó la compilación de producción en el contenedor de Angular para garantizar ausencia de errores sintácticos, de tipado en TypeScript o de plantillas HTML.

### Comando ejecutado:
```bash
docker compose exec frontend npm run build
```

### Resultados:
```text
Application bundle generation complete. [18.512 seconds]
Output location: /app/dist/impulsetech-fe

Initial chunk files   | Names                    |  Raw size | Estimated transfer size
chunk-U3OC32OD.js     | -                        | 179.15 kB |                51.17 kB
chunk-5TAPVIMW.js     | -                        |  88.83 kB |                22.10 kB
styles-4DYKGIML.css   | styles                   |  31.23 kB |                 5.02 kB

Lazy chunk files      | Names                    |  Raw size | Estimated transfer size
chunk-KKQULA7J.js     | dashboard-home-component |  12.66 kB |                 3.54 kB

Application bundle generated successfully with 0 errors.
```

- **Componentes Verificados:**
  - `DashboardHomeComponent` (`src/app/modules/dashboard/home/`).
  - Separación de `dashboard-home.component.html` y `dashboard-home.component.scss` conforme a `frontend-design`.
  - Tarjetas KPI: Pipeline Activo, MRR Recurrente, Cartera Clientes 360°, Total Recaudado en Caja.
  - Secciones visuales de embudos especializados, desglose multimoneda y feeds de actividad reciente con enlaces de acceso directo.

---

## 4. Estado de Pull Requests

- **Backend FastAPI:** `impulsetech-be` -> PR #9 (`feature/IT-11-dashboard-gerencial`)
- **Frontend Angular:** `impulsetech-fe` -> PR #9 (`feature/IT-11-dashboard-gerencial`)
- **Repositorio Orquestador:** `impulsetech` -> PR en proceso.

---

## 5. Conclusión y Veredicto

**Veredicto:** **APROBADO PARA QA / IN TESTING**  
El Dashboard Gerencial y Operativo proporciona visibilidad ejecutiva sobre las operaciones, finanzas y embudos de venta de ImpulseTech.
