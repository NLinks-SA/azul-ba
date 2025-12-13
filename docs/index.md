# Guía de Implementación Odoo
## Manufactura con Subcontratación + Dropship Subcontractor + MTO + Calidad

Esta guía documenta paso a paso cómo configurar Odoo para un escenario de **manufactura compleja** que incluye:

- ✅ Subcontratación en múltiples etapas
- ✅ Dropship Subcontractor (envíos directos entre proveedores)
- ✅ Control de calidad en Dropship Subcontractor
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

### Flujo especial para Tapas de Madera (Dropship Subcontractor)

```
┌─────────────────┐                      ┌─────────────────────┐     ┌─────────────────┐
│   CARPINTERÍA   │   Picking: DSC       │     LUSTRADOR       │     │     STOCK       │
│   Hnos. García  │═════════════════════>│  Lustres & Acabados │────>│   Disponible    │
│                 │   (dropship + QC)    │                     │     │                 │
│   Tapa Madera   │                      │   (produce Tapa     │     │   (Tapa         │
│   SIN Terminar  │   QC al validar →    │    Terminada)       │     │    Terminada)   │
│                 │   Pass/Fail          │                     │     │                 │
└─────────────────┘                      └─────────────────────┘     └─────────────────┘
```

La tapa sin terminar va **directo** de Carpintería al Lustrador (sin pasar por nuestro almacén).

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
       ├── PO → Lustrador (Tapas Madera Terminadas - subcontratación)
       └── PO → Marmolería/Neolith (otras tapas)
          │
          ▼ (al confirmar PO Lustrador)
4. SUBCONTRACT MO + DROPSHIP
   └── La PO Lustrador genera Subcontract MO
       └── Necesita Tapa Sin Terminar (ruta Dropship)
           └── PO → Carpintería
               └── DSC Picking (con QC) → Lustrador
          │
          ▼
5. RECEPCIONES + QC
   └── Control de calidad en DSC Picking
          │
          ▼
6. PRODUCCIÓN
   └── Work Orders de ensamblado
          │
          ▼
7. ENTREGA
   └── Despacho al cliente
          │
          ▼
8. FACTURACIÓN
   ├── Factura al cliente
   └── Validación facturas proveedores
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
