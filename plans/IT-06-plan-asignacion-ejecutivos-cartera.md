# Plan de Implementación: [IT-06] Asignación de Ejecutivos: Regla de 1 Ejecutivo Responsable por Cliente y Filtros de Cartera

**ID de Tarjeta en Trello:** `6af354247d3dac9422a2aeec`  
**Rama Base:** `feature/IT-05-modulo-clientes` (o `main`)  
**Ramas de Trabajo:**
- `impulsetech`: `feature/IT-06-asignacion-ejecutivos-cartera`
- `impulsetech-be`: `feature/IT-06-asignacion-ejecutivos-cartera`
- `impulsetech-fe`: `feature/IT-06-asignacion-ejecutivos-cartera`

---

## 1. Contexto de Negocio y Reglas (`STARTUP_CANVAS.md`)
- **Regla de Negocio Canónica:** Cada cliente tiene asignado **exactamente un único Ejecutivo de Cuenta**, quien es el punto de contacto, seguimiento de hitos y responsable comercial.
- **Reglas de Acceso a la Cartera (RBAC & Cartera):**
  - **ADMIN:** Tiene visión global de toda la cartera de clientes. Puede filtrar por cualquier ejecutivo o ver "Todos", reasignar ejecutivos libremente y gestionar todas las cuentas.
  - **EJECUTIVO:** Puede alternar rápidamente entre "Mi Cartera" (clientes donde `ejecutivo_id == current_user.id`) y "Toda la Cartera" (o estar restringido según la vista predeterminada). Por defecto, al entrar al Directorio, si es EJECUTIVO, su vista inicia filtrada en **"Mi Cartera"**.
- **Reasignación Rápida:** Acción para que el Administrador (o ejecutivo facultado) transfiera la titularidad de un cliente de un ejecutivo a otro con trazabilidad en notas o endpoint dedicado/PUT directo.
- **Consumo del Endpoint de Ejecutivos:** Asegurar que el selector de ejecutivos en el frontend consuma `/api/v1/users/ejecutivos` (disponible para cualquier usuario autenticado) en lugar de `/api/v1/users` (que requiere rol `ADMIN`).

---

## 2. Especificación Técnica

### A. Backend (`impulsetech-be`)
1. **Endpoint `GET /api/v1/clients` con soporte para filtro de cartera:**
   - Parámetro opcional `solo_mi_cartera: bool = False`. Si es `True`, fuerza `ejecutivo_id = current_user.id`.
   - Permitir a los ejecutivos ver clientes asignados o consultar de forma transparente.
2. **Endpoint de Reasignación de Ejecutivo (`PATCH /api/v1/clients/{cliente_id}/reassign`):**
   - Payload: `{"nuevo_ejecutivo_id": UUID, "motivo": str | None}`.
   - Valida que el nuevo ejecutivo exista y esté activo.
   - Actualiza el cliente, registra el cambio en notas operativas si se envía motivo.
3. **Tests con `pytest`:**
   - Crear un usuario con rol `EJECUTIVO`.
   - Verificar filtro de cartera (`solo_mi_cartera=True` o `ejecutivo_id`).
   - Probar endpoint de reasignación validando que se actualiza el `ejecutivo_id`.

### B. Frontend (`impulsetech-fe`)
1. **Tabs o Switch de Cartera en Directorio (`client-list`):**
   - Switch / Selector:
     - "Toda la Cartera" (con contador total).
     - "Mi Cartera" (con contador de clientes a cargo del usuario logueado).
   - Dropdown adicional para Administradores: "Filtrar por Ejecutivo" (con lista de todos los ejecutivos activos).
2. **Corrección de carga de ejecutivos:**
   - Actualizar `ClientService.getEjecutivos()` para llamar a `/api/v1/users/ejecutivos` (para que los usuarios con rol `EJECUTIVO` puedan cargar la lista sin error 403).
3. **Acción de Reasignación en Ficha 360° y Menú de Tabla:**
   - Modal/Selector rápido "Reasignar Ejecutivo" en la Ficha 360°.

---

## 3. Pruebas y Criterios de Aceptación (DoD)
- [x] Backend: Endpoint de reasignación y soporte de filtro de cartera implementados y testeados con pytest.
- [x] Frontend: Tabs "Toda la Cartera" / "Mi Cartera" funcionando reactivamente con Signals.
- [x] Frontend: Dropdown de filtro por ejecutivo para usuarios Admin.
- [x] Frontend: Reasignación de ejecutivo desde la Ficha 360° funcional.
- [x] Compilación limpia con `npm run build`.
- [x] PRs creados en GitHub y tarjeta movida a `in testing`.
