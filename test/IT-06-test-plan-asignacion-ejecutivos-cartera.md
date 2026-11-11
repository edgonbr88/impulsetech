# Plan de Pruebas: [IT-06] Asignación de Ejecutivos: Regla de 1 Ejecutivo Responsable por Cliente y Filtros de Cartera

**ID de Tarjeta en Trello:** `6af354247d3dac9422a2aeec`  
**Fecha de Ejecución:** 2026-11-10  
**Ramas de Pruebas:** `feature/IT-06-asignacion-ejecutivos-cartera`  
**Pull Requests Asociados:**
- Backend: [impulsetech-be#4](https://github.com/edgonbr88/impulsetech-be/pull/4)
- Frontend: [impulsetech-fe#4](https://github.com/edgonbr88/impulsetech-fe/pull/4)

---

## 1. Alcance de las Pruebas
Verificación de las reglas de negocio sobre la titularidad y gestión de clientes:
1. Regla de **1 Ejecutivo Responsable por Cliente** garantizada a nivel relacional y de API.
2. Endpoint `PATCH /api/v1/clients/{id}/reassign` para transferencia de titularidad y registro de trazabilidad en notas.
3. Parámetro `solo_mi_cartera=true` en `GET /api/v1/clients` para aislar clientes asignados al usuario autenticado.
4. Consumo seguro de ejecutivos activos en `/api/v1/users/ejecutivos` sin restricción de rol Admin.
5. Tabs reactivos en Angular ("Toda la Cartera" / "Mi Cartera"), selector de ejecutivo para Admin y modal interactivo de reasignación.

---

## 2. Matriz de Casos de Prueba

| ID | Componente | Descripción de la Prueba | Entrada / Acción | Resultado Esperado | Estado |
|---|---|---|---|---|---|
| **CP-01** | Backend API | Listado filtrado por cartera propia | `GET /api/v1/clients?solo_mi_cartera=true` | Solo retorna clientes donde `ejecutivo_id == current_user.id`. | ✅ Aprobado |
| **CP-02** | Backend API | Reasignación de ejecutivo con motivo | `PATCH /api/v1/clients/{id}/reassign` con `nuevo_ejecutivo_id` y motivo | Código 200 OK, `ejecutivo_id` actualizado y nota agregada con fecha UTC. | ✅ Aprobado |
| **CP-03** | Backend API | Reasignación con ejecutivo inexistente | `PATCH /api/v1/clients/{id}/reassign` con UUID aleatorio | Código 400 Bad Request ("El nuevo ejecutivo asignado no existe"). | ✅ Aprobado |
| **CP-04** | Backend Suite | Ejecución de suite de tests automatizada | `docker compose exec backend pytest` | 12 tests pasados exitosamente en verde. | ✅ Aprobado |
| **CP-05** | Frontend API | Consumo de ejecutivos activos | `clientService.getEjecutivos()` | Llama a `/api/v1/users/ejecutivos` permitiendo acceso a ejecutivos y admins. | ✅ Aprobado |
| **CP-06** | Frontend Build | Compilación de producción de Angular | `docker compose exec frontend npm run build` | Compilación limpia sin errores ni advertencias (14.2s). | ✅ Aprobado |
| **CP-07** | Frontend UI | Alternancia de tabs Toda vs Mi Cartera | Clic en "Mi Cartera" | Se activa Signal, la tabla se recarga con `solo_mi_cartera=true`. | ✅ Aprobado |
| **CP-08** | Frontend UI | Filtro de ejecutivo exclusivo para Admin | Cambio en dropdown de ejecutivos | Se filtra la lista por el ID del ejecutivo seleccionado. | ✅ Aprobado |
| **CP-09** | Frontend UI | Modal de reasignación desde Ficha 360° | Clic en "Reasignar ejecutivo" y confirmación | Modal se despliega, reasigna en backend y actualiza la ficha al instante. | ✅ Aprobado |

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

tests/test_auth.py ........                                              [ 66%]
tests/test_clients.py ..                                                 [ 83%]
tests/test_health.py ..                                                  [100%]

============================== 12 passed in 9.00s ==============================
```

### Frontend Build Output:
```text
> impulsetech-fe@1.0.0 build
> ng build

✔ Building...
Initial chunk files   | Names                    |  Raw size | Estimated transfer size
chunk-2PIDWQOR.js     | -                        | 236.71 kB |                63.75 kB
polyfills-FFHMD2TL.js | polyfills                |  34.52 kB |                11.28 kB
styles-NVXRPDGY.css   | styles                   |  22.37 kB |                 4.17 kB
main-BRU6HJ7F.js      | main                     |   1.33 kB |               647 bytes

                      | Initial total            | 294.93 kB |                79.84 kB

Lazy chunk files      | Names                    |  Raw size | Estimated transfer size
chunk-53GRVYSI.js     | -                        |  40.30 kB |                 8.33 kB
chunk-FOAPEM5P.js     | client-list-component    |  34.20 kB |                 7.47 kB
chunk-S3QS5KI7.js     | shell-component          |   6.71 kB |                 2.05 kB
chunk-GLTGU5EI.js     | login-component          |   6.04 kB |                 2.06 kB
chunk-VJ64ZB4B.js     | dashboard-home-component |   4.78 kB |                 1.73 kB

Application bundle generation complete. [14.271 seconds]
```

---

## 4. Conclusión
La funcionalidad de asignación de ejecutivos, regla de 1 ejecutivo por cliente y filtros de cartera (`IT-06`) se encuentra totalmente implementada y verificada. Tarjeta apta para pasar a `in testing`.
