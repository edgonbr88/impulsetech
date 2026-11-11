# Plan de Pruebas: [IT-02] Migración DDL Inicial con dbmate (Módulo de Usuarios y Roles)

**ID Tarea:** IT-02  
**Título:** Migración DDL Inicial con dbmate (Módulo de Usuarios y Roles)  
**Tarjeta Trello:** [https://trello.com/c/udMpLnhP](https://trello.com/c/udMpLnhP)  
**Fecha de Ejecución:** 2026-11-10  
**Estado:** SUPERADO (PASS)  
**Agente Evaluador / Implementador:** trello_implementer  

---

## 1. Alcance de Pruebas
- **Repositorio Impactado:** `impulsetech-migration` (archivo `db/migrations/20261110195500_create_usuarios_table.sql` y `db/schema.sql`).
- **Objetos de Base de Datos Creados en PostgreSQL 16:**
  - Extensiones: `uuid-ossp`, `pgcrypto`.
  - Tipo ENUM: `rol_usuario_enum` (`'ADMIN'`, `'EJECUTIVO'`).
  - Función de trigger: `update_updated_at_column()`.
  - Tabla: `usuarios` con UUID primario (`gen_random_uuid()`), restricciones de unicidad y defaults.
  - Índices: `idx_usuarios_email`, `idx_usuarios_rol`, `idx_usuarios_activo`.
  - Trigger: `trg_usuarios_updated_at` (actualización automática de `updated_at` en `BEFORE UPDATE`).
  - Datos semilla: Inserción del usuario Administrador inicial (`admin@impulsetech.com`) con hash bcrypt.

---

## 2. Pruebas Automatizadas y de Migración Ejecutadas

### 2.1 Aplicación de Migración (`dbmate up`)
- **Comando:** `docker compose run --rm migration up`
- **Resultado:**
  ```text
  Applying: 20261110195500_create_usuarios_table.sql
  Writing: ./db/schema.sql
  ```
- **Estado:** ✅ PASS

### 2.2 Reversibilidad de Migración (`dbmate rollback` y re-aplicación)
- **Comando:** `docker compose run --rm migration rollback && docker compose run --rm migration up`
- **Resultado:**
  ```text
  Rolling back: 20261110195500_create_usuarios_table.sql
  Writing: ./db/schema.sql
  Applying: 20261110195500_create_usuarios_table.sql
  Writing: ./db/schema.sql
  ```
- **Estado:** ✅ PASS (Reversión completa y limpia, sin residuos en el catálogo de PostgreSQL).

### 2.3 Verificación de Estructura DDL en PostgreSQL
- **Comando:** `docker compose exec postgres psql -U impulsetech -d impulsetech_dev -P pager=off -c "\d usuarios"`
- **Resultado:**
  - Columnas: `id (UUID PK)`, `nombre`, `email (UQ)`, `password_hash`, `rol (ENUM)`, `activo`, `created_at`, `updated_at`.
  - Índices: `usuarios_pkey`, `idx_usuarios_activo`, `idx_usuarios_email`, `idx_usuarios_rol`, `uq_usuarios_email`.
  - Trigger: `trg_usuarios_updated_at` activo.
- **Estado:** ✅ PASS

### 2.4 Verificación de Funcionamiento de Trigger `updated_at`
- **Comando:**
  ```sql
  UPDATE usuarios SET nombre = 'Admin Principal' WHERE email = 'admin@impulsetech.com';
  SELECT nombre, created_at < updated_at AS updated_at_changed FROM usuarios WHERE email = 'admin@impulsetech.com';
  ```
- **Resultado:** `updated_at_changed: t` (true).
- **Estado:** ✅ PASS

### 2.5 Verificación del Seed de Usuario Administrador
- **Comando:** `docker compose exec postgres psql -U impulsetech -d impulsetech_dev -P pager=off -c "SELECT id, nombre, email, rol, activo FROM usuarios WHERE email = 'admin@impulsetech.com';"`
- **Resultado:**
  ```text
  id: 3e235ac8-8afb-48f4-ac94-1b5193b87e7a
  nombre: Administrador ImpulseTech
  email: admin@impulsetech.com
  rol: ADMIN
  activo: true
  ```
- **Estado:** ✅ PASS

---

## 3. Guía de Pruebas Manuales / Comandos de Verificación Paso a Paso

### Paso 1: Consultar Estado de Migraciones
```bash
docker compose run --rm migration status
```
*Resultado Esperado:*
```text
Applied: 1
Pending: 0
```

### Paso 2: Consultar la Tabla Directamente en PostgreSQL
```bash
docker compose exec postgres psql -U impulsetech -d impulsetech_dev -P pager=off -c "SELECT id, email, rol, activo FROM usuarios;"
```

---

## 4. Matriz de Criterios de Aceptación (DoD)

- [x] Migración ejecutada con `dbmate up` sin advertencias ni errores.
- [x] Tabla `usuarios` creada con constraints de unicidad en email, tipos de datos correctos e índices.
- [x] Usuario Administrador semilla insertado con hash bcrypt válido (`admin@impulsetech.com`).
- [x] Trigger `trg_usuarios_updated_at` verificado en acción.
- [x] Reversibilidad con `dbmate rollback` y re-aplicación validada sin errores.
- [x] Plan de pruebas documentado en `test/IT-02-test-plan-migracion-ddl-usuarios.md`.
- [ ] PRs creados en GitHub y tarjeta en Trello movida a `in testing`.
