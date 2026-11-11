# Plan de Implementación: [IT-02] Migración DDL Inicial con dbmate (Módulo de Usuarios y Roles)

**ID Tarea:** IT-02  
**Tarjeta Trello:** [https://trello.com/c/udMpLnhP](https://trello.com/c/udMpLnhP) (ID: `6af354233a563603fc2e5ffc`)  
**Fecha:** 2026-11-10  
**Estado del Plan:** LISTO PARA IMPLEMENTACIÓN  
**Agente Revisor/Planificador:** trello_planner  

---

## 1. Contexto de Negocio y Justificación
ImpulseTech requiere una estructura de datos canónica y persistente para gestionar a los operadores de la plataforma en su Fase 1:
- **Administrador (`ADMIN`)**: Acceso total al sistema, configuración de ejecutivos, supervisión de métricas financieras globales y embudos.
- **Ejecutivo de Cuenta (`EJECUTIVO`)**: Gestión de cartera de clientes asignados, calificación de leads y seguimiento de servicios en curso.

La autenticación futura (tarea `IT-03`) depende de esta tabla para validar credenciales con hashes de contraseñas seguros (bcrypt) y asociar la identidad a tokens JWT.

---

## 2. Alcance Técnico y Arquitectura
- **Repositorio Impactado:** `impulsetech-migration` (y registro en `impulsetech`).
- **Motor:** PostgreSQL 16.
- **Herramienta de Migración:** `dbmate` (utilizando la imagen oficial `amacneil/dbmate:2.15`).
- **Archivo de Migración:** `impulsetech-migration/db/migrations/20261110195500_create_usuarios_table.sql`.
- **Regla de Gobernanza:** Ejecución y prueba estricta en el entorno local (PostgreSQL en Docker). Cero ejecuciones directas sobre entornos productivos sin testeo previo.

---

## 3. Modelo de Datos y Script DDL (PostgreSQL / dbmate)

### Script SQL: `db/migrations/20261110195500_create_usuarios_table.sql`

```sql
-- migrate:up
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Tipo ENUM de roles de usuario
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'rol_usuario_enum') THEN
        CREATE TYPE rol_usuario_enum AS ENUM ('ADMIN', 'EJECUTIVO');
    END IF;
END$$;

-- 2. Función genérica para actualización de updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 3. Tabla de Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol rol_usuario_enum NOT NULL DEFAULT 'EJECUTIVO',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_usuarios_email UNIQUE (email)
);

-- 4. Índices para rendimiento en búsquedas y filtros
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios (email);
CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios (rol);
CREATE INDEX IF NOT EXISTS idx_usuarios_activo ON usuarios (activo);

-- 5. Trigger para actualizar automáticamente updated_at
DROP TRIGGER IF EXISTS trg_usuarios_updated_at ON usuarios;
CREATE TRIGGER trg_usuarios_updated_at
BEFORE UPDATE ON usuarios
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- 6. Seed del usuario Administrador inicial (Password: Admin2026*!)
INSERT INTO usuarios (nombre, email, password_hash, rol, activo)
VALUES (
    'Administrador ImpulseTech',
    'admin@impulsetech.com',
    '$2b$12$jRsFZJVJfajSmyz5apQCr.3BqA5WstoPeEN/LHDe79li6bpfv2aBu',
    'ADMIN',
    TRUE
)
ON CONFLICT (email) DO NOTHING;

-- migrate:down
DROP TRIGGER IF EXISTS trg_usuarios_updated_at ON usuarios;
DROP TABLE IF EXISTS usuarios;
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP TYPE IF EXISTS rol_usuario_enum;
```

---

## 4. Pruebas y Verificación

- **Prueba 1: Aplicación de Migración (`dbmate up`)**
  - Comando: `docker compose run --rm migration up`
  - Esperado: Aplica `20261110195500_create_usuarios_table.sql` exitosamente.
- **Prueba 2: Verificación de Estructura e Índices en PostgreSQL**
  - Comando: `docker compose exec postgres psql -U impulsetech -d impulsetech_dev -c "\d usuarios"`
  - Esperado: Tabla `usuarios` con columnas UUID, nombre, email, password_hash, rol, activo, timestamps e índices.
- **Prueba 3: Verificación del Seed del Administrador**
  - Comando: `docker compose exec postgres psql -U impulsetech -d impulsetech_dev -c "SELECT id, nombre, email, rol, activo FROM usuarios WHERE email = 'admin@impulsetech.com';"`
  - Esperado: 1 fila retornada con rol `ADMIN` y `activo = true`.
- **Prueba 4: Prueba de Reversibilidad (Rollback y Re-up)**
  - Comando: `docker compose run --rm migration rollback && docker compose run --rm migration up`
  - Esperado: Rollback elimina limpiamente la tabla y ENUM; re-up vuelve a crear todo sin errores.

---

## 5. Checklist Paso a Paso (Para trello_implementer)
- [x] Crear el archivo de migración en `impulsetech-migration/db/migrations/20261110195500_create_usuarios_table.sql`.
- [x] Ejecutar la migración localmente con `docker compose run --rm migration up`.
- [x] Validar la existencia de la tabla, índices y ENUM en PostgreSQL.
- [x] Validar que el usuario Administrador inicial fue insertado correctamente.
- [x] Validar el trigger de actualización de `updated_at`.
- [x] Validar la reversibilidad completa (`dbmate rollback` seguido de `dbmate up`).
- [x] Generar el Plan de Pruebas en `test/IT-02-test-plan-migracion-ddl-usuarios.md`.
- [x] Crear rama `feature/IT-02-migracion-ddl-usuarios`, hacer commit y push a GitHub.
- [x] Crear Pull Request en GitHub para `impulsetech-migration` y `impulsetech`.
- [x] Mover tarjeta en Trello a `in testing` con el resumen de la ejecución.

---

## 6. Criterios de Aceptación (Definition of Done - DoD)
- [x] Migración ejecutada con `dbmate up` sin advertencias ni errores.
- [x] Tabla `usuarios` creada con constraints de unicidad en email y tipos adecuados.
- [x] Usuario Administrador semilla disponible con hash bcrypt válido.
- [x] Rollback probado y validado.
- [x] Documento de pruebas registrado en `test/IT-02-test-plan-migracion-ddl-usuarios.md`.
- [x] Tarjeta en Trello movida a `in testing`.
