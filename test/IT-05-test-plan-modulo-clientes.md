# Plan de Pruebas: [IT-05] Módulo de Clientes: Modelo DDL, CRUD en FastAPI y Directorio en Angular (Ficha 360°)

**ID de Tarjeta en Trello:** `6af35424b752e3751879fecc`  
**Fecha de Ejecución:** 2026-11-10  
**Ramas de Pruebas:** `feature/IT-05-modulo-clientes`  
**Pull Requests Asociados:**
- Migraciones: [impulsetech-migration#3](https://github.com/edgonbr88/impulsetech-migration/pull/3)
- Backend: [impulsetech-be#3](https://github.com/edgonbr88/impulsetech-be/pull/3)
- Frontend: [impulsetech-fe#3](https://github.com/edgonbr88/impulsetech-fe/pull/3)

---

## 1. Alcance de las Pruebas
Validación integral del módulo de Clientes:
1. Migración DDL en PostgreSQL mediante `dbmate` (`clientes`, `estado_cliente_enum`, índices y triggers de timestamp).
2. Endpoints CRUD REST bajo `/api/v1/clients` con filtros por búsqueda, estado y ejecutivo.
3. Reglas de negocio: 1 Ejecutivo por cliente, unicidad de RIF, validación de integridad referencial.
4. Compilación e integración visual en Angular 18 con Signals, Reactive Forms, Modal de registro y Drawer de Ficha 360°.

---

## 2. Matriz de Casos de Prueba

| ID | Componente | Descripción de la Prueba | Entrada / Acción | Resultado Esperado | Estado |
|---|---|---|---|---|---|
| **CP-01** | Base de Datos | Aplicación de migración DDL con dbmate | `docker compose run --rm migration up` | Migración `20261110231500_create_clientes_table.sql` aplicada y `schema.sql` actualizado. | ✅ Aprobado |
| **CP-02** | Backend API | Autenticación y creación de cliente | `POST /api/v1/clients` con payload válido y token Bearer | Código 201 Created, cliente retornado con UUID, datos del ejecutivo anidados. | ✅ Aprobado |
| **CP-03** | Backend API | Unicidad de RIF / Identificación | `POST /api/v1/clients` con RIF duplicado | Código 400 Bad Request con detalle explicativo. | ✅ Aprobado |
| **CP-04** | Backend API | Listado y filtros de búsqueda | `GET /api/v1/clients?search=...` | Código 200 OK, lista filtrada por razón social o RIF. | ✅ Aprobado |
| **CP-05** | Backend API | Detalle de cliente por ID | `GET /api/v1/clients/{id}` | Código 200 OK con Ficha 360° y datos de contacto. | ✅ Aprobado |
| **CP-06** | Backend API | Actualización de cliente | `PUT /api/v1/clients/{id}` (cambio a estado `MOROSO`) | Código 200 OK, estado actualizado en base de datos. | ✅ Aprobado |
| **CP-07** | Backend API | Eliminación protegida (solo Admin) | `DELETE /api/v1/clients/{id}` con token de Admin | Código 204 No Content, posterior GET retorna 404. | ✅ Aprobado |
| **CP-08** | Backend Suite | Ejecución de suite de tests automatizada | `docker compose exec backend pytest` | 11 tests aprobados en verde sin regresiones. | ✅ Aprobado |
| **CP-09** | Frontend Build | Compilación de producción de Angular | `docker compose exec frontend npm run build` | Bundle generado en 13s sin advertencias de tipos ni CSS. | ✅ Aprobado |
| **CP-10** | Frontend UI | Navegación y directorio de clientes | Acceso a `/clients` desde el Sidebar | Renderizado de tabla densa, buscador reactivo y badges de estado. | ✅ Aprobado |
| **CP-11** | Frontend UI | Modal de creación / edición | Clic en "Nuevo Cliente" | Modal con Reactive Form y dropdown de ejecutivos disponibles. | ✅ Aprobado |
| **CP-12** | Frontend UI | Drawer lateral Ficha 360° | Clic en fila o botón de ojo en la tabla | Drawer con datos de contacto, enlace a WhatsApp, notas y slots futuros. | ✅ Aprobado |

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

tests/test_auth.py ........                                              [ 72%]
tests/test_clients.py .                                                  [ 81%]
tests/test_health.py ..                                                  [100%]

============================== 11 passed in 6.89s ==============================
```

### Frontend Build Output:
```text
> impulsetech-fe@1.0.0 build
> ng build

✔ Building...
Initial chunk files   | Names                    |  Raw size | Estimated transfer size
chunk-LPA2ETQO.js     | -                        | 154.84 kB |                44.47 kB
chunk-AJMZG5XG.js     | -                        |  83.11 kB |                20.86 kB
polyfills-FFHMD2TL.js | polyfills                |  34.52 kB |                11.28 kB
styles-A3KYAUY7.css   | styles                   |  21.64 kB |                 4.06 kB
main-ZXW7NXOR.js      | main                     |   1.36 kB |               659 bytes

                      | Initial total            | 295.47 kB |                81.32 kB

Lazy chunk files      | Names                    |  Raw size | Estimated transfer size
chunk-ML3OLLXZ.js     | -                        |  40.31 kB |                 8.34 kB
chunk-JETJKZOL.js     | client-list-component    |  26.46 kB |                 6.21 kB
chunk-IBHPHWI5.js     | shell-component          |   6.75 kB |                 2.08 kB
chunk-S3PZ5ODD.js     | login-component          |   6.08 kB |                 2.08 kB
chunk-67JYPFGU.js     | dashboard-home-component |   4.82 kB |                 1.75 kB

Application bundle generation complete. [13.018 seconds]
```

---

## 4. Conclusión
El módulo de Clientes (`IT-05`) cumple con el 100% de los criterios de aceptación y directrices de arquitectura. Se autoriza el paso a la columna `in testing`.
