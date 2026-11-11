# Plan de Pruebas: [IT-12] Frontend: Enlace de Servicios a API, Manejo de Estados Vacíos (Empty States) y Alertas de Conexión

- **ID de la Historia:** `IT-12`
- **Trello Card ID:** `6af46905c82724fb5116ce88`
- **Módulo:** Experiencia de Usuario (UX), Resiliencia de Red y Enlace de API
- **Fecha de Ejecución:** 2026-11-11
- **Responsable:** ImpulseTech Core Platform Team / AI Assistant

---

## 1. Alcance y Objetivos de la Prueba

Verificar:
1. La resolución correcta de endpoints HTTP desde el frontend hacia el backend FastAPI (`http://localhost:8000/api/v1`) evitando rutas relativas inválidas en el dev server de Angular.
2. La presentación de mensajes y bloques de **Empty State** cuando no hay registros en la base de datos para Clientes, Leads y Servicios, incorporando botones de llamada a la acción (*Registrar Primer Cliente*, *Registrar Primer Lead*, *Aperturar Servicio*).
3. La distinción visual entre ausencia de datos (*Empty State*) y un error de conexión HTTP (red caída, timeout), incluyendo un botón de *"Reintentar conexión"*.

---

## 2. Pruebas de Red y Comunicación Frontend -> Backend

- **Configuración de Entorno:**
  - Archivos creados: `src/environments/environment.ts` y `src/environments/environment.prod.ts`.
  - Constante: `apiBaseUrl: 'http://localhost:8000/api/v1'`.
- **Servicios Angular Verificados:**
  - `ClientService` -> consume `${environment.apiBaseUrl}/clients` y `/users/ejecutivos`.
  - `LeadService` -> consume `${environment.apiBaseUrl}/leads`, `/users/ejecutivos` y `/clients`.
  - `ServiceContractsService` -> consume `${environment.apiBaseUrl}/services` y `/clients`.
  - `PaymentService` -> consume `${environment.apiBaseUrl}/payments`.
  - `DashboardService` -> consume `${environment.apiBaseUrl}/dashboard/metrics`.
  - `AuthService` -> consume `${environment.apiBaseUrl}/auth`.

---

## 3. Pruebas de Compilación y Frontend (Angular 18)

### Comando ejecutado:
```bash
docker compose exec frontend npm run build
```

### Resultados:
```text
Application bundle generation complete. [30.894 seconds]
Output location: /app/dist/impulsetech-fe

Initial chunk files   | Names                    |  Raw size | Estimated transfer size
chunk-TY7HPAEV.js     | -                        | 179.22 kB |                51.17 kB
chunk-X72DFSNW.js     | -                        |  88.83 kB |                22.08 kB
polyfills-FFHMD2TL.js | polyfills                |  34.52 kB |                11.28 kB

Lazy chunk files      | Names                    |  Raw size | Estimated transfer size
chunk-8N1GZ1F6.js     | lead-list-component      |  38.25 kB |                 8.53 kB
chunk-PCPQ81P4.js     | client-list-component    |  34.82 kB |                 7.53 kB
chunk-OG5O54XB.js     | service-list-component   |  27.78 kB |                 6.56 kB
chunk-MLAXBTXR.js     | payment-list-component   |  26.09 kB |                 6.42 kB

Application bundle generated successfully with 0 errors.
```

- **Componentes Verificados:**
  - `ClientListComponent`: Empty state con mensaje *"Aún no hay clientes registrados"* y botón CTA. Banner de error con botón *"Reintentar conexión"*.
  - `LeadListComponent`: Empty state con mensaje *"Aún no hay prospectos registrados"* y botón CTA. Banner de error con botón *"Reintentar conexión"*.
  - `ServiceListComponent`: Empty state con mensaje *"Aún no hay servicios registrados"* y botón CTA. Banner de error con botón *"Reintentar conexión"*.
  - `PaymentListComponent`: Banner de error enriquecido con botón *"Reintentar conexión"*.

---

## 4. Estado de Pull Requests

- **Frontend Angular:** `impulsetech-fe` -> PR #10 (`feature/IT-12-empty-states-y-conexion`)
- **Repositorio Orquestador:** `impulsetech` -> PR en proceso.

---

## 5. Conclusión y Veredicto

**Veredicto:** **APROBADO PARA QA / IN TESTING**  
Todos los criterios de aceptación de la tarjeta `[IT-12]` fueron implementados y verificados.
