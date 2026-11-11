# Plan de Implementación: [IT-12] Frontend: Enlace de Servicios a API, Manejo de Estados Vacíos (Empty States) y Alertas de Conexión

- **ID de la Historia:** `IT-12`
- **Trello Card ID:** `6af46905c82724fb5116ce88`
- **Fase:** Fase 5 - Calidad de Interfaz, Resiliencia de Red y UX
- **Responsable:** ImpulseTech Engineering Team
- **Fecha:** 2026-11-11

---

## 1. Contexto y Objetivos

Para optimizar la experiencia de usuario y garantizar una resiliencia robusta frente a fallos de red o bases de datos sin registros iniciales:
1. **Configuración de Red Homogénea:** Centralizar `apiBaseUrl` a través de los entornos de Angular (`src/environments/environment.ts`), asegurando que todos los servicios de datos conecten con FastAPI (`http://localhost:8000/api/v1`).
2. **Empty States Intencionales (`frontend-design`):**
   - En **Clientes**: Mostrar bloque visual cuando `clients().length === 0`, con mensaje *"Aún no hay clientes registrados"* y botón CTA *"Registrar Primer Cliente"*.
   - En **Leads & Embudos**: Mostrar bloque visual en tabla y kanban cuando no hay prospectos, con mensaje *"Aún no hay prospectos en este embudo comercial"* y botón CTA *"Nuevo Prospecto"*.
   - En **Servicios**: Mostrar bloque visual cuando `services().length === 0`, con mensaje *"Aún no hay servicios ni contratos registrados"* y botón CTA *"Crear Servicio"*.
   - En **Finanzas / Pagos**: Mantener y reforzar el empty state con CTA para registrar el primer pago.
3. **Manejo de Error y Botón de Reintento:**
   - Si la API responde con error o no hay conexión con el backend, mostrar un banner de advertencia diferenciado que incluya un botón explícito de *"Reintentar carga"*.

### Criterios de Aceptación (DoD):
- [x] Servicios HTTP consumiendo `environment.apiBaseUrl` sin rutas relativas huérfanas.
- [x] Componente Clientes (`ClientListComponent`) con Empty State + CTA y botón de reintento ante errores.
- [x] Componente Leads (`LeadListComponent`) con Empty State + CTA y botón de reintento ante errores.
- [x] Componente Servicios (`ServiceListComponent`) con Empty State + CTA y botón de reintento ante errores.
- [x] Componente Finanzas (`PaymentListComponent`) con botón de reintento ante errores de conexión.
- [x] Plantillas `.html` y `.scss` separadas bajo lineamientos de `frontend-design`.
- [x] Compilación limpia con `npm run build` sin errores.
- [x] Plan de pruebas en `test/IT-12-test-plan-empty-states-conexion.md`.
- [x] PRs creados y tarjeta movida a `in testing` en Trello.

---

## 2. Plan Paso a Paso de Ejecución

### Paso 1: Ramas Git
- Main repo `impulsetech`: crear rama `feature/IT-12-empty-states-y-conexion`.
- Frontend repo `impulsetech-fe`: crear rama `feature/IT-12-empty-states-y-conexion`.

### Paso 2: Actualización de Componentes de Frontend
1. **`ClientListComponent`**:
   - Agregar botón de reintento en el banner de error.
   - Refinar el bloque de Empty State existente con llamada a la acción y diseño mejorado.
2. **`LeadListComponent`**:
   - Agregar botón de reintento en el banner de error.
   - Agregar bloque de Empty State tanto en vista Tabla como en vista Kanban con botón `openCreateModal()`.
3. **`ServiceListComponent`**:
   - Agregar botón de reintento en el banner de error.
   - Agregar fila o bloque de Empty State en la tabla cuando `services().length === 0` con botón `openCreateModal()`.
4. **`PaymentListComponent`**:
   - Agregar botón de reintento de carga de datos en caso de error HTTP.

### Paso 3: Validación y Compilación
- Ejecutar `docker compose exec frontend npm run build` y certificar compilación exitosa.

### Paso 4: Documentación y Trello
- Crear `test/IT-12-test-plan-empty-states-conexion.md`.
- Abrir PRs en GitHub.
- Mover tarjeta a `in testing` en Trello.
