# Plan de Pruebas: [IT-07] Módulo de Leads: DDL y Embudos Especializados (Legal SAREN, IA/Automatización, Software a Medida)

**ID de Tarjeta en Trello:** `6af35425c5a30765656667e2`  
**Fecha de Ejecución:** 2026-11-11  
**Ramas de Pruebas:** `feature/IT-07-modulo-leads-embudos`  
**Pull Requests Asociados:**
- Migraciones: [impulsetech-migration#4](https://github.com/edgonbr88/impulsetech-migration/pull/4)
- Backend: [impulsetech-be#5](https://github.com/edgonbr88/impulsetech-be/pull/5)
- Frontend: [impulsetech-fe#5](https://github.com/edgonbr88/impulsetech-fe/pull/5)

---

## 1. Alcance de las Pruebas
Verificación de los cimientos relacionales y operativos de los Embudos de Venta:
1. Migración DDL en PostgreSQL con enums `embudo_lead_enum` (`LEGAL_SAREN`, `IA_AUTOMATIZACION`, `SOFTWARE_MEDIDA`) y `etapa_lead_enum` (`NUEVO`, `DIAGNOSTICO`, `PROPUESTA`, `NEGOCIACION`, `GANADO`, `PERDIDO`).
2. Endpoints REST CRUD bajo `/api/v1/leads` con filtros por embudo y búsqueda.
3. Transición de etapas comerciales (`PATCH /api/v1/leads/{id}/stage`) y captura de motivo de pérdida.
4. Directorio en Angular 18 con pestañas especializadas por cada embudo, badges semáforo y formulario reactivo.

---

## 2. Matriz de Casos de Prueba

| ID | Componente | Descripción de la Prueba | Entrada / Acción | Resultado Esperado | Estado |
|---|---|---|---|---|---|
| **CP-01** | Base de Datos | Aplicación de migración de leads | `docker compose run --rm migration up` | Tabla `leads` creada con enums, FK a usuarios/clientes y trigger de timestamp. | ✅ Aprobado |
| **CP-02** | Backend API | Creación de lead en Legal SAREN | `POST /api/v1/leads` con `embudo="LEGAL_SAREN"` | Código 201 Created, lead creado con etapa inicial `NUEVO`. | ✅ Aprobado |
| **CP-03** | Backend API | Creación de lead en IA & Automatización | `POST /api/v1/leads` con `embudo="IA_AUTOMATIZACION"` | Código 201 Created, valor estimado en USD almacenado. | ✅ Aprobado |
| **CP-04** | Backend API | Filtrado por embudo específico | `GET /api/v1/leads?embudo=LEGAL_SAREN` | Código 200 OK, solo retorna leads del embudo indicado. | ✅ Aprobado |
| **CP-05** | Backend API | Actualización de etapa comercial | `PATCH /api/v1/leads/{id}/stage` a `NEGOCIACION` | Código 200 OK con etapa actualizada. | ✅ Aprobado |
| **CP-06** | Backend API | Transición a etapa PERDIDO | `PATCH /api/v1/leads/{id}/stage` con motivo de pérdida | Código 200 OK, motivo de pérdida guardado y trazable. | ✅ Aprobado |
| **CP-07** | Backend Suite | Ejecución de suite de tests automatizada | `docker compose exec backend pytest` | 13 tests pasados exitosamente en verde. | ✅ Aprobado |
| **CP-08** | Frontend Build | Compilación de producción de Angular | `docker compose exec frontend npm run build` | Compilación limpia sin errores en 22.1s. | ✅ Aprobado |
| **CP-09** | Frontend UI | Selector de Embudos Especializados | Clic en "Legal SAREN", "IA & Automatización", "Software a Medida" | Se recarga reactivamente la lista filtrando por el embudo activo. | ✅ Aprobado |
| **CP-10** | Frontend UI | Modal de Captura de Lead | Registro de lead con validaciones | Formulario reactivo valida campos y motivo de pérdida condicional. | ✅ Aprobado |

---

## 3. Evidencias de Ejecución

### Backend Pytest Output:
```text
============================= test session starts ==============================
platform linux -- Python 3.12.16, pytest-9.2.0, pluggy-1.7.0
rootdir: /app
configfile: pytest.ini
plugins: anyio-4.16.0, asyncio-1.4.1.post1
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=session

tests/test_auth.py ........                                              [ 61%]
tests/test_clients.py ..                                                 [ 76%]
tests/test_health.py ..                                                  [ 92%]
tests/test_leads.py .                                                    [100%]

============================= 13 passed in 14.46s ==============================
```

### Frontend Build Output:
```text
> impulsetech-fe@1.0.0 build
> ng build

✔ Building...
Initial chunk files   | Names                    |  Raw size | Estimated transfer size
chunk-DVMF626P.js     | -                        | 247.01 kB |                67.21 kB
polyfills-FFHMD2TL.js | polyfills                |  34.52 kB |                11.28 kB
styles-35DVH6SQ.css   | styles                   |  24.31 kB |                 4.44 kB
main-4QTJSHNB.js      | main                     |   1.42 kB |               667 bytes

                      | Initial total            | 307.26 kB |                83.60 kB

Lazy chunk files      | Names                    |  Raw size | Estimated transfer size
chunk-BBZPAZZW.js     | -                        |  40.92 kB |                 8.39 kB
chunk-NRRM32GP.js     | client-list-component    |  34.19 kB |                 7.46 kB
chunk-IPHNDQ5E.js     | lead-list-component      |  23.35 kB |                 5.85 kB
chunk-QGH2GEBO.js     | shell-component          |   6.89 kB |                 2.06 kB
chunk-NYQKC7DZ.js     | login-component          |   6.04 kB |                 2.06 kB
chunk-RJRGY64G.js     | dashboard-home-component |   4.78 kB |                 1.73 kB

Application bundle generation complete. [22.110 seconds]
```

---

## 4. Conclusión
El módulo de Leads y sus 3 embudos especializados (`IT-07`) cumple a cabalidad con la especificación canónica. Se aprueba la transición a `in testing`.
