# Guía de Implementación Odoo
## Manufactura con Subcontratación Multietapa + MTO + Calidad

Esta guía documenta paso a paso cómo configurar Odoo para un escenario de **manufactura compleja** que incluye:

- ✅ Subcontratación en múltiples etapas
- ✅ Envíos entre proveedores
- ✅ Controles de calidad en recepciones y producción
- ✅ Ensamblado interno
- ✅ Make to Order (MTO) - Fabricación bajo pedido
- ✅ Trazabilidad completa

---

## 📦 Caso de Uso: Fábrica de Muebles

Una empresa fabrica **Mesas de Comedor Premium** con las siguientes características:

| Componente | Variantes | Proveedor |
|------------|-----------|-----------|
| **Tapa** | Mármol, Neolith, Madera | Marmolería, Neolith Argentina, Carpintería → Lustrador |
| **Base** | Acero Negro, Acero Dorado | Metalúrgica |
| **Mesa** | 20 combinaciones válidas | Ensamblado interno |
| **Terminación** | Sin Terminación, Lustre Mate/Brillante, Natural | Depende del material |

### Flujo especial para Tapas de Madera (con transferencia visible)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│   CARPINTERÍA   │     │   WH/STOCK      │     │     LUSTRADOR       │     │     FÁBRICA     │
│   (Proveedor A) │────▶│   (Recepción)   │────▶│    (Proveedor B)    │────▶│    (Interno)    │
└─────────────────┘     └─────────────────┘     └─────────────────────┘     └─────────────────┘
        │                       │                         │                         │
   Tapa Madera            Envío a Lustrador         Tapa Madera               Mesa Final
   SIN Terminar           (Transfer visible)        CON Terminación           Ensamblada
```

La transferencia de Stock → Lustrador aparece en **Inventario → Operaciones → Traslados internos**.

---

## 🎯 Flujo Objetivo

Al finalizar esta configuración, el sistema operará así:

```
1. VENTA
   └── Confirmar Orden de Venta
          │
          ▼ (automático - MTO)
2. MANUFACTURA
   └── Se genera MO para Mesa
          │
          ▼ (automático - MTO)
3. COMPRAS
   └── Se generan POs para componentes
       ├── PO → Metalúrgica (Bases)
       ├── PO → Lustrador (Tapas Madera)
       └── PO → Marmolería/Neolith (otras tapas)
          │
          ▼
4. RECEPCIONES + QC
   └── Control de calidad en cada recepción
          │
          ▼
5. PRODUCCIÓN
   └── Work Orders de ensamblado
          │
          ▼
6. ENTREGA
   └── Despacho al cliente
          │
          ▼
7. FACTURACIÓN
   ├── Factura al cliente
   └── Validación facturas proveedores (3-way + QC)
```

---

## 📚 Estructura de la Guía

| Parte | Contenido |
|-------|-----------|
| [**Parte 1**](parte1/index.md) | Preparación del Sistema - Apps y configuraciones |
| [**Parte 2**](parte2/index.md) | Datos Maestros - Proveedores y productos |
| [**Parte 3**](parte3/index.md) | Manufactura - Work Centers y BoMs |
| [**Parte 4**](parte4/index.md) | Control de Calidad |
| [**Parte 5**](parte5/index.md) | Flujo Operativo - Prueba completa |
| [**Parte 6**](parte6/index.md) | Facturación - Cliente y proveedores |
| [**Anexos**](anexos/index.md) | RACI, BPMN, Glosario, Troubleshooting, Script |

---

## ⏱️ Tiempo Estimado

| Tarea | Tiempo |
|-------|--------|
| Configuración inicial | 30 min |
| Datos maestros | 1 hora |
| Manufactura | 1 hora |
| Calidad | 30 min |
| Pruebas | 30 min |
| **Total** | **~3.5 horas** |

!!! tip "Script de Automatización"
    Si preferís automatizar la configuración, en los [Anexos](anexos/script.md) encontrarás un script Python que crea toda la demo en minutos.

---

## 🔧 Requisitos Previos

- Odoo 17+ (probado en Odoo 19)
- Acceso de administrador
- Módulos Enterprise recomendados (Quality)

!!! note "Versión de Odoo"
    Esta guía fue creada para **Odoo 19**, pero los conceptos aplican a versiones 17+.
