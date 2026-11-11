# Plan de Pruebas: [IT-04] Frontend: Setup de Angular 18, Design System y Módulo de Login

**ID Tarea:** IT-04  
**Título:** Frontend: Setup de Angular 18, Design System y Módulo de Login  
**Tarjeta Trello:** [https://trello.com/c/9ZwNjebO](https://trello.com/c/9ZwNjebO)  
**Fecha de Ejecución:** 2026-11-10  
**Estado:** SUPERADO (PASS)  
**Agente Evaluador / Implementador:** trello_implementer  

---

## 1. Alcance de Pruebas
- **Repositorio Impactado:** `impulsetech-fe`
- **Módulos y Componentes Probados:**
  - `core/services/auth.service.ts`: Manejo de sesión reactiva con Signals (`currentUser`, `token`, `isAuthenticated`, `isAdmin`).
  - `core/interceptors/jwt.interceptor.ts`: Inyección de header `Authorization: Bearer <token>`.
  - `core/guards/auth.guard.ts`: `authGuard` (protección de rutas privadas) y `guestGuard` (redirección si ya está autenticado).
  - `modules/auth/login/`: Formulario reactivo de login (`LoginComponent`) con validación y manejo de errores.
  - `layout/shell/`: Shell privado con Sidebar de navegación, datos del usuario activo y botón de logout (`ShellComponent`).
  - `modules/dashboard/home/`: Vista principal del Dashboard con Bento Grid (`DashboardHomeComponent`).
  - Separación de plantillas: 100% de los componentes con archivos independientes `.component.html`.

---

## 2. Pruebas Automatizadas de Compilación (ng build)

- **Comando:** `docker compose exec frontend npm run build`
- **Resultado:**
  ```text
  Initial chunk files   | Names                    |  Raw size | Estimated transfer size
  chunk-CQALIZEG.js     | -                        | 231.04 kB |                62.11 kB
  polyfills-FFHMD2TL.js | polyfills                |  34.52 kB |                11.28 kB
  styles-IDEP22G4.css   | styles                   |  15.31 kB |                 3.25 kB
  main-Y6NPCEWO.js      | main                     |   1.23 kB |               621 bytes
                        | Initial total            | 282.10 kB |                77.26 kB

  Lazy chunk files      | Names                    |  Raw size | Estimated transfer size
  chunk-4ENWOQAL.js     | login-component          |  38.80 kB |                 9.05 kB
  chunk-EEO2X3FN.js     | shell-component          |   6.48 kB |                 2.03 kB
  chunk-BN2CXDQ7.js     | dashboard-home-component |   4.78 kB |                 1.73 kB

  Application bundle generation complete. [17.438 seconds]
  Output location: /app/dist/impulsetech-fe
  ```
- **Estado:** ✅ PASS (Cero errores de compilación TypeScript 5.5, chunks diferidos generados correctamente).

---

## 3. Pruebas de Integración y Flujo de Usuario

### 3.1 Carga del Servidor de Desarrollo en Docker
- **Comando:** `curl -s http://localhost:4200/`
- **Resultado:** Retorna HTML inicial cargando `@vite/client`, `styles.css`, `polyfills.js` y `main.js`.
- **Estado:** ✅ PASS

### 3.2 Flujo de Autenticación (Login)
1. Usuario visita `http://localhost:4200/login`.
2. Introduce credenciales válidas (`admin@impulsetech.com` / `Admin2026*!`).
3. El servicio `AuthService.login()` envía petición a `POST http://localhost:8000/api/v1/auth/login`.
4. El token JWT y el perfil del usuario se persisten en `localStorage` y en los signals `token()` y `currentUser()`.
5. El router redirige automáticamente a `/dashboard`.
- **Estado:** ✅ PASS

### 3.3 Protección de Rutas con Guards
1. Usuario anónimo intenta ingresar a `http://localhost:4200/dashboard` sin token.
2. `authGuard` intercepta la navegación, verifica `authService.isAuthenticated() == false`.
3. Se redirige de inmediato a `/login`.
- **Estado:** ✅ PASS

### 3.4 Interceptor HTTP (JWT)
1. Al realizar peticiones protegidas dentro de la sesión, `jwtInterceptor` inyecta automáticamente el header `Authorization: Bearer <TOKEN>`.
- **Estado:** ✅ PASS

### 3.5 Cierre de Sesión (Logout)
1. Desde el Shell lateral, se pulsa "Cerrar Sesión".
2. `authService.logout()` remueve el token y perfil de `localStorage` y limpia los signals.
3. El router redirige al usuario a `/login`.
- **Estado:** ✅ PASS

---

## 4. Matriz de Criterios de Aceptación (DoD)

- [x] Compilación limpia de Angular 18 sin errores de tipado (`npm run build`).
- [x] Formulario reactivo de login conectado con backend FastAPI (`/api/v1/auth/login`).
- [x] Signals reactivos de sesión (`currentUser`, `token`, `isAuthenticated`, `isAdmin`) operativos.
- [x] Guards funcionales (`authGuard` y `guestGuard`) protegiendo rutas y evitando loops.
- [x] Interceptor HTTP (`jwtInterceptor`) inyectando token en peticiones salientes.
- [x] Separación estricta de plantillas `.component.html` en todos los componentes creados.
- [x] Diseño sobrio y profesional auditado bajo la skill `frontend-design` (paleta Slate/Sky, Bento Grid, sin clichés de IA).
- [ ] PRs generados en GitHub y tarjeta en Trello movida a `in testing`.
