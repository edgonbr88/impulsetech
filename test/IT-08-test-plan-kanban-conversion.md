# Plan de Pruebas: [IT-08] Vistas Kanban de Embudos de Venta y Acción de Conversión Lead -> Cliente en Angular

**ID de Tarjeta en Trello:** `6af35425e01d867c7da63c99`  
**Fecha de Ejecución:** 2026-11-11  
**Ramas de Pruebas:** `feature/IT-08-kanban-leads-conversion`  
**Pull Requests Asociados:**
- Backend: [impulsetech-be#6](https://github.com/edgonbr88/impulsetech-be/pull/6)
- Frontend: [impulsetech-fe#6](https://github.com/edgonbr88/impulsetech-fe/pull/6)

---

## 1. Alcance de las Pruebas
Verificación integral del flujo de ventas visual y la conversión operativa de oportunidades a clientes:
1. Endpoint `POST /api/v1/leads/{id}/convert-to-client` en FastAPI para transformación atómica Lead -> Cliente.
2. Validación de duplicidad de RIF en la conversión y actualización de etapa a `GANADO`.
3. Tablero Kanban interactivo con 6 columnas por etapa (`NUEVO`, `DIAGNOSTICO`, `PROPUESTA`, `NEGOCIACION`, `GANADO`, `PERDIDO`).
4. Métricas de conteo y valor acumulado en USD por columna.
5. Modal reactivo de conversión con formulario prellenado y validación de RIF fiscal.
6. Alternancia fluida entre Vista Kanban y Vista Tabla.

---

## 2. Matriz de Casos de Prueba

| ID | Componente | Descripción de la Prueba | Entrada / Acción | Resultado Esperado | Estado |
|---|---|---|---|---|---|
| **CP-01** | Backend API | Conversión de Lead a Cliente exitosa | `POST /api/v1/leads/{id}/convert-to-client` con RIF válido | Código 200 OK, cliente creado en BD, lead actualizado con `cliente_id` y etapa `GANADO`. | ✅ Aprobado |
| **CP-02** | Backend API | Prevención de RIF duplicado al convertir | Conversión con RIF ya existente en la tabla `clientes` | Código 400 Bad Request ("Ya existe un cliente registrado con el RIF..."). | ✅ Aprobado |
| **CP-03** | Backend Suite | Ejecución de suite de tests automatizada | `docker compose exec backend pytest` | 14 tests pasados exitosamente en verde. | ✅ Aprobado |
| **CP-04** | Frontend Build | Compilación de producción de Angular | `docker compose exec frontend npm run build` | Compilación limpia sin errores en 20.3s. | ✅ Aprobado |
| **CP-05** | Frontend UI | Alternancia de vistas (Tabla / Kanban) | Clic en botones de modo de vista | Renderizado dinámico del formato correspondiente. | ✅ Aprobado |
| **CP-06** | Frontend UI | Métricas de columna en el Kanban | Visualización de cabeceras de columnas | Conteo exacto de leads y suma total en USD por etapa. | ✅ Aprobado |
| **CP-07** | Frontend UI | Avance rápido de etapa en Kanban | Clic en "Avanzar a Diagnóstico / Propuesta" | Llamada al API y reubicación visual de la tarjeta. | ✅ Aprobado |
| **CP-08** | Frontend UI | Flujo modal de conversión a cliente | Clic en "Convertir a Cliente" y envío de RIF | Lead pasa a columna GANADO, se crea cliente y se permite ir a su ficha. | ✅ Aprobado |

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

tests/test_auth.py ........                                              [ 57%]
tests/test_clients.py ..                                                 [ 71%]
tests/test_health.py ..                                                  [ 85%]
tests/test_leads.py ..                                                   [100%]

============================= 14 passed in 18.66s ==============================
```

### Frontend Build Output:
```text
> impulsetech-fe@1.0.0 build
> ng build

✔ Building...
Initial chunk files   | Names                    |  Raw size | Estimated transfer size
chunk-DVMF626P.js     | -                        | 247.01 kB |                67.21 kB
polyfills-FFHMD2TL.js | polyfills                |  34.52 kB |                11.28 kB
styles-RHQKLNSZ.css   | styles                   |  26.64 kB |                 4.74 kB
main-NDPJJZNL.js      | main                     |   1.42 kB |               666 bytes

                      | Initial total            | 309.60 kB |                83.89 kB

Lazy chunk files      | Names                    |  Raw size | Estimated transfer size
chunk-BBZPAZZW.js     | -                        |  40.92 kB |                 8.39 kB
chunk-HPVB65I6.js     | lead-list-component      |  36.19 kB |                 8.14 kB
chunk-NRRM32GP.js     | client-list-component    |  34.19 kB |                 7.46 kB
chunk-QGH2GEBO.js     | shell-component          |   6.89 kB |                 2.06 kB
chunk-NYQKC7DZ.js     | login-component          |   6.04 kB |                 2.06 kB
chunk-RJRGY64G.js     | dashboard-home-component |   4.78 kB |                 1.73 kB

Application bundle generation complete. [20.395 seconds]
```

---

## 4. Conclusión
El tablero Kanban de embudos de venta y la acción de conversión automática de Lead a Cliente (`IT-08`) quedan 100% implementados y verificados. Tarjeta lista para pasar a `in testing`.
