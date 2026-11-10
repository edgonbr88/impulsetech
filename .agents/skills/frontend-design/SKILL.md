---
name: frontend-design
description: >-
  Directrices de diseño visual distintivo e intencional para la construcción y evolución de la UI de ImpulseTech en Angular 18+.
  Garantiza una identidad visual profesional, sobria y orientada a la operación B2B, evitando activamente clichés de IA y plantillas genéricas.
---

# Frontend Design — ImpulseTech

Aborda este diseño con la mentalidad de un Lead Designer enfocado en productos B2B de alto rendimiento y consultoría de operaciones. ImpulseTech no es una plantilla genérica de SaaS ni un dashboard prefabricado: es la plataforma operativa que conecta trámites legales, automatizaciones con IA y software a la medida para negocios en Venezuela.

---

## 1. Fundamentos de Identidad y Contexto

* **Materia del Producto:** CRM operativo interno y centro de control multicanal (Leads, Clientes, Servicios Legales/IA/Software y Cobranzas Multimoneda).
* **Audiencia Principal:** Administradores y Ejecutivos de Cuenta de ImpulseTech.
  * *Necesidades clave:* Máxima legibilidad, alta densidad de información estructurada, visualización inmediata de embudos (Kanban), estados de servicios y cuentas por cobrar en divisas (USD, VES tasa BCV, USDT).
* **Personalidad de Marca:**
  * Rigor corporativo y legal (confianza, orden, precisión documental).
  * Vértice tecnológico moderno (agilidad, automatización, claridad).
  * Pragmatismo operativo (cero distracciones o elementos decorativos vacíos).

---

## 2. Paleta Intencional de Tokens (Cero Clichés de IA)

Queda estrictamente prohibido caer en los patrones genéricos generados por IA:
* **NO** a fondos crema cálido (`#F4F1EA`) con acentos terracota (`#D97757`).
* **NO** al tema "hacker oscuro" genérico con verde neón ácido sin justificación.
* **NO** al "SaaS-card kit" idéntico: no dividir todo en tarjetas repetitivas con sombra gris suave difusa (`rgba(0,0,0,0.08)`) y esquinas redondeadas uniformes sin jerarquía.

### Paleta Base Recomendada (4-6 colores deliberados):
* **Superficie Principal (Canvas):** `#0F172A` (Slate profundo) para modo oscuro o `#F8FAFC` (Slate puro muy limpio) para modo claro.
* **Superficies de Elevación (Cards / Paneles):** `#1E293B` (en dark) o `#FFFFFF` con borde sutil de 1px `#E2E8F0` (en light).
* **Color Primario de Marca (Tech / Acción):** `#0284C7` (Sky / Azul cerúleo profesional).
* **Color de Acento Legal / Confianza:** `#475569` (Slate neutro para metadata y estructura).
* **Acentos de Estado Financiero & Operativo:**
  * Verde Éxito / Cobrado: `#10B981` (Emerald).
  * Ámbar Alerta / Trámite en espera: `#F59E0B` (Amber).
  * Rojo Riesgo / Moroso: `#EF4444` (Rose).
  * Púrpura Software / IA: `#8B5CF6` (Violet).

---

## 3. Jerarquía Tipográfica y Estructura

* **Tipografía:** Usar familias sans-serif de alta legibilidad técnica (ej. `Inter`, `Geist Sans` o tipografía de sistema moderna).
* **Tratamiento tipográfico intencional:**
  * Evitar resaltar palabras individuales con diferente color o negrita dentro del mismo titular.
  * No abusar de etiquetas en mayúsculas (`ALL-CAPS`) con espaciado excesivo en cada encabezado.
  * Los números financieros y códigos identificadores (`IT-XX`, RIFs, montos en divisas) deben destacar por peso y alineación tabular, no por tamaños extravagantes.
* **Layouts Funcionales:**
  * Uso de Bento Grids asimétricos donde las tarjetas tienen tamaños proporcionados al valor de la información que contienen (ej. el pipeline activo ocupa 70% del ancho, mientras que el semáforo financiero ocupa el 30% restante).
  * Tablas de datos con densidad compacta para ejecutivos, con soporte de filtrado rápido y estados vacíos claros.

---

## 4. Copywriting y UX Humano

* Cada botón y acción debe indicar exactamente qué va a suceder:
  * Usar "Crear Servicio", "Registrar Pago", "Convertir a Cliente".
  * Evitar términos vagos como "Enviar", "Submit", "Aceptar".
* **Estados Vacíos con Dirección:** Si un embudo no tiene leads o un cliente no tiene servicios, la pantalla no debe ser un vacío triste, sino una invitación a actuar: *"No hay servicios registrados para este cliente. Haz clic en 'Agregar Servicio' para iniciar un trámite legal o setup de IA."*
* **Errores y Advertencias:** Mensajes directos y claros que expliquen el problema y la acción correctiva (ej. *"Debes indicar la tasa BCV del día para pagos en Bolívares (VES)"*).

---

## 5. Reglas Técnicas en Angular 18+

1. **Separación Obligatoria de Plantillas:**
   * Todo componente **DEBE** separar su plantilla HTML en un archivo independiente (`.component.html`) y su hoja de estilos en (`.component.scss` / `.component.css`).
   * **PROHIBIDO** el uso de `template: \`...\`` inline en el archivo `.ts`.
2. **Componentes Standalone y Signals:**
   * Utilizar la arquitectura moderna de Angular 18 (`standalone: true`, `imports: [...]`, `signal()`, `computed()`).
3. **Control de Accesibilidad y Responsive:**
   * Contraste de texto nivel WCAG AA como mínimo.
   * Navegación completa por teclado con anillos de foco visibles (`focus-visible`).
   * Vistas adaptables a resoluciones de laptop y pantallas de escritorio.
