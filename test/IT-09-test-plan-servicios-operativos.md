# Plan de Pruebas: [IT-09] Módulo de Servicios Operativos

- **ID de la Historia:** `IT-09`
- **Trello Card ID:** `6af354256f60320cc74dd125`
- **Módulo:** Servicios Operativos (Lifecycle, Proyectos vs Retainers)
- **Fecha de Ejecución:** 2026-11-11
- **Responsable:** ImpulseTech Core Platform Team / AI Assistant

---

## 1. Alcance y Objetivos de la Prueba

Verificar la correcta implementación del modelo de datos de servicios operativos, el soporte de modalidades (`PROYECTO` con hitos de entrega vs `RETAINER` recurrente mensual con día de corte), la posibilidad de que un cliente tenga múltiples servicios paralelos activos, y el cambio de estado de ciclo de vida (`PLANIFICACION`, `EN_PROCESO`, `PAUSADO`, `ENTREGADO`, `CANCELADO`).

---

## 2. Pruebas Automatizadas de Backend (FastAPI + Pytest)

Se ejecutó la suite de pruebas unitarias y de integración sobre la base de datos PostgreSQL local en Docker.

### Comando ejecutado:
```bash
docker compose exec backend pytest -v
```

### Resultados:
```text
tests/test_auth.py::test_login_success PASSED                            [  6%]
tests/test_auth.py::test_login_invalid_password PASSED                  [ 13%]
tests/test_auth.py::test_login_user_not_found PASSED                    [ 20%]
tests/test_auth.py::test_get_current_user_profile PASSED                [ 26%]
tests/test_clients.py::test_create_and_list_clients PASSED              [ 33%]
tests/test_clients.py::test_duplicate_rif_validation PASSED            [ 40%]
tests/test_clients.py::test_reassign_client_executive PASSED            [ 46%]
tests/test_clients.py::test_filter_mi_cartera PASSED                    [ 53%]
tests/test_leads.py::test_create_and_list_leads PASSED                  [ 60%]
tests/test_leads.py::test_patch_lead_stage_and_loss_reason PASSED       [ 66%]
tests/test_leads.py::test_convert_lead_to_client_success PASSED         [ 73%]
tests/test_leads.py::test_convert_lead_duplicate_rif_error PASSED       [ 80%]
tests/test_services.py::test_create_and_list_services PASSED            [ 86%]
tests/test_services.py::test_retainer_requires_dia_corte PASSED         [ 93%]
tests/test_services.py::test_patch_service_status PASSED                [100%]

============================== 15 passed in 2.14s ==============================
```

- **Total Tests:** 15
- **Passed:** 15
- **Failed:** 0
- **Validaciones Clave:**
  1. `test_create_and_list_services`: Creación de un servicio en modalidad `PROYECTO`, validación de hitos estructurados en JSONB y listado filtrado por `cliente_id`.
  2. `test_retainer_requires_dia_corte`: Regla de negocio que exige `dia_corte_mensual` entre 1 y 31 para servicios `RETAINER` recurrente, arrojando error HTTP 422 si falta.
  3. `test_patch_service_status`: Transición de estados del ciclo de vida (`PLANIFICACION` -> `EN_PROCESO` -> `ENTREGADO`) y validación de trazabilidad.

---

## 3. Pruebas de Compilación y Frontend (Angular 18)

Se validó la compilación de producción en el contenedor de Angular para garantizar ausencia de errores sintácticos, de tipado en TypeScript o de plantillas HTML.

### Comando ejecutado:
```bash
docker compose exec frontend npm run build
```

### Resultados:
```text
Application bundle generation complete. [22.209 seconds]
Output location: /app/dist/impulsetech-fe

Initial chunk files | Names         |  Raw size | Estimated transfer size
main-EZU7W27Z.js     | main          | 434.90 kB |               108.99 kB
styles-O2S436F2.css  | styles        |  18.72 kB |                 3.89 kB

Application bundle generated successfully with 0 errors.
```

- **Componentes Verificados:**
  - `ServiceListComponent` (`src/app/modules/services/service-list/`)
  - Plantilla HTML y estilos SCSS desacoplados.
  - Pestañas de filtrado: *Todos*, *Proyectos*, *Retainers*.
  - Filtro por estado: `PLANIFICACION`, `EN_PROCESO`, `PAUSADO`, `ENTREGADO`, `CANCELADO`.
  - Modal reactivo de creación de servicios con selector dinámico de modalidad (revela `dia_corte_mensual` únicamente en Retainers).
  - Modal de actualización rápida de estado.
  - Indicador de estado con microinteracciones y paleta sobria B2B de acuerdo al estándar `frontend-design`.

---

## 4. Estado de Pull Requests

- **Migraciones DDL:** `impulsetech-migration` -> PR #5 (`feature/IT-09-modulo-servicios-operativos`)
- **Backend FastAPI:** `impulsetech-be` -> PR #7 (`feature/IT-09-modulo-servicios-operativos`)
- **Frontend Angular:** `impulsetech-fe` -> PR #7 (`feature/IT-09-modulo-servicios-operativos`)
- **Repositorio Orquestador:** `impulsetech` -> PR en proceso.

---

## 5. Conclusión y Veredicto

**Veredicto:** **APROBADO PARA QA / IN TESTING**  
Todas las pruebas de integración, contratos de datos y reglas de negocio pasaron satisfactoriamente.
