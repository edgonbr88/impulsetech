# Plan de Implementación: [IT-04] Frontend: Setup de Angular 18, Design System y Módulo de Login

**ID Tarea:** IT-04  
**Tarjeta Trello:** [https://trello.com/c/9ZwNjebO](https://trello.com/c/9ZwNjebO) (ID: `6af3542362b5f61e8b4684aa`)  
**Fecha:** 2026-11-10  
**Estado del Plan:** LISTO PARA IMPLEMENTACIÓN  
**Agente Revisor/Planificador:** trello_planner  

---

## 1. Contexto de Negocio y Justificación
ImpulseTech requiere una interfaz de acceso y autenticación profesional, ágil y confiable para sus operadores internos (Administradores y Ejecutivos).
La experiencia de inicio de sesión debe reflejar seriedad corporativa, integrando:
- Inicio de sesión seguro contra la API FastAPI (`POST /api/v1/auth/login`).
- Almacenamiento seguro del token JWT y estado de sesión reactivo con Signals de Angular 18.
- Redirección automática y protección de rutas mediante Guards funcionales.
- Inyección transparente del token en peticiones HTTP salientes con HttpInterceptor.
- Layout privado de trabajo (Shell) con navegación lateral responsiva, estado del usuario y opción de cierre de sesión.
- Estética y directrices visuales estrictas de la skill `frontend-design` (paleta intencional, tipografía legible, cero plantillas genéricas de IA, separación obligatoria de `.html` y `.ts`).

---

## 2. Alcance Técnico y Arquitectura
- **Repositorio Impactado:** `impulsetech-fe` (y registro en `impulsetech`).
- **Framework:** Angular 18.2+ (Standalone Components, Signals, Router, HttpClient).
- **Estilos:** Tailwind CSS con tokens definidos en `frontend-design`.
- **Estructura Modular en `impulsetech-fe/src/app/`:**
  ```text
  src/app/
  ├── core/
  │   ├── models/
  │   │   └── user.model.ts          (Interfaces User, LoginRequest, AuthResponse)
  │   ├── services/
  │   │   └── auth.service.ts        (Signals currentUser, isAuthenticated, métodos login, logout, getMe)
  │   ├── interceptors/
  │   │   └── jwt.interceptor.ts     (Inyección de Authorization: Bearer <token>)
  │   └── guards/
  │       ├── auth.guard.ts          (Bloquea acceso anónimo a rutas privadas)
  │       └── guest.guard.ts         (Redirige a dashboard si ya está autenticado)
  ├── layout/
  │   └── shell/
  │       ├── shell.component.ts     (Layout privado con sidebar, header, perfil y router-outlet)
  │       ├── shell.component.html
  │       └── shell.component.scss
  ├── modules/
  │   ├── auth/
  │   │   └── login/
  │   │       ├── login.component.ts (Formulario reactivo, validaciones, loader y feedback de error)
  │   │       ├── login.component.html
  │   │       └── login.component.scss
  │   └── dashboard/
  │       └── home/
  │           ├── dashboard-home.component.ts (Vista principal de bienvenida con Bento Grid)
  │           ├── dashboard-home.component.html
  │           └── dashboard-home.component.scss
  ├── app.config.ts                  (provideHttpClient con withInterceptors([jwtInterceptor]))
  ├── app.routes.ts                  (Configuración de rutas con guards)
  ├── app.component.ts               (Root component con router-outlet)
  └── app.component.html
  ```

---

## 3. Directivas de Diseño y UI/UX (`frontend-design`)
- **Separación Obligatoria de Plantillas:** Todos los componentes (`login`, `shell`, `dashboard-home`) deben tener sus archivos `.component.html` independientes. Prohibido el uso de templates inline.
- **Paleta Intencional:**
  - Superficies: Slate profundo `#0F172A`, Cards `#1E293B`, bordes `#334155`.
  - Acción / Tech: Sky Cerúleo `#0284C7` / `#0EA5E9`.
  - Estados: Éxito `#10B981`, Alerta `#F59E0B`, Error `#EF4444`.
- **Microcopy y Accesibilidad:**
  - Botón: "Iniciar Sesión" (con estado de carga "Validando credenciales...").
  - Inputs con etiquetas claras, mensajes de error explicativos sin culpar al usuario.
  - Soporte de teclado (tabulación y foco visible).

---

## 4. Pruebas y Verificación
- **Prueba 1: Compilación de Angular (`npm run build`)**
  - Comando: `docker compose exec frontend npm run build`
  - Esperado: Compilación limpia sin errores de tipado TypeScript ni de Tailwind.
- **Prueba 2: Carga del Login**
  - Navegar a `http://localhost:4200/login`
  - Verificar renderizado del formulario, logo de ImpulseTech y validaciones en vivo.
- **Prueba 3: Autenticación Exitosa**
  - Ingresar: `admin@impulsetech.com` / `Admin2026*!`
  - Verificar guardado del token en `localStorage`, actualización de Signal `currentUser()` y redirección inmediata a `/dashboard`.
- **Prueba 4: Protección de Rutas (Guard)**
  - Limpiar `localStorage` e intentar ingresar directamente a `http://localhost:4200/dashboard`
  - Verificar redirección forzada a `/login`.
- **Prueba 5: Cierre de Sesión (Logout)**
  - En el shell privado, pulsar "Cerrar Sesión".
  - Verificar limpieza de token y redirección a `/login`.

---

## 5. Checklist Paso a Paso (Para trello_implementer)
- [x] Definir interfaces de usuario y autenticación en `core/models/user.model.ts`.
- [x] Implementar `core/services/auth.service.ts` con gestión de Signals reactivos (`currentUser`, `isAuthenticated`).
- [x] Implementar interceptor funcional `core/interceptors/jwt.interceptor.ts`.
- [x] Implementar guards funcionales `auth.guard.ts` y `guestGuard`.
- [x] Configurar inyección en `app.config.ts`.
- [x] Crear componente de Login (`modules/auth/login/`) con ReactiveFormsModule y plantilla separada `.html`.
- [x] Crear componente de Shell privado (`layout/shell/`) con Sidebar, Navbar y plantilla separada `.html`.
- [x] Crear vista de Dashboard Home (`modules/dashboard/home/`) con plantilla separada `.html`.
- [x] Configurar rutas en `app.routes.ts`.
- [x] Validar compilación con `docker compose exec frontend npm run build`.
- [x] Probar flujo completo de login, guard y logout en el navegador.
- [x] Generar Plan de Pruebas en `test/IT-04-test-plan-frontend-angular-login.md`.
- [ ] Crear ramas `feature/IT-04-frontend-angular-login`, commit y push a GitHub.
- [ ] Crear Pull Requests en GitHub para `impulsetech-fe` e `impulsetech`.
- [ ] Mover tarjeta en Trello a `in testing` con el reporte final.

---

## 6. Criterios de Aceptación (Definition of Done - DoD)
- [x] Compilación limpia con `npm run build` en el frontend.
- [x] Formulario de login conectado y validado contra el backend FastAPI.
- [x] Signals de usuario y estado reactivo funcionando correctamente.
- [x] Guards bloqueando acceso a rutas privadas sin token válido.
- [x] Interceptor inyectando header `Authorization: Bearer <TOKEN>` en peticiones protegidas.
- [x] Separación estricta de plantillas `.component.html` en todos los componentes creados.
- [x] Plan de pruebas documentado en `test/IT-04-test-plan-frontend-angular-login.md`.
- [ ] PRs creados en GitHub y tarjeta en Trello movida a `in testing`.
