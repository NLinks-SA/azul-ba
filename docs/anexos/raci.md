# Matriz RACI

Definición de responsabilidades por proceso y rol.

---

## ¿Qué es RACI?

| Letra | Significado | Descripción |
|-------|-------------|-------------|
| **R** | Responsable | Ejecuta la tarea |
| **A** | Accountable | Aprueba/firma (único dueño) |
| **C** | Consultado | Aporta información |
| **I** | Informado | Recibe notificación |

---

## Matriz por Proceso

| Proceso | Ventas | Compras | Inventario | Calidad | Producción | Contabilidad |
|---------|:------:|:-------:|:----------:|:-------:|:----------:|:------------:|
| **Cotización** | **R** | I | I | I | I | I |
| **Confirmación SO** | **A/R** | I | I | I | I | I |
| **Generación MO/PO** | C | C | C | C | C | C |
| **Revisión y confirmación POs** | I | **A/R** | C | I | I | I |
| **Recepciones proveedores** | I | I | **A/R** | C | I | I |
| **Control de calidad proveedores** | I | I | C | **A/R** | I | I |
| **Transferencias entre proveedores** | I | I | **A/R** | C | I | I |
| **Ensamblado interno (Work Orders)** | I | I | C | C | **A/R** | I |
| **Validación MO** | I | I | C | C | **A/R** | I |
| **Entrega al cliente** | I | I | **A/R** | I | C | I |
| **Facturación cliente** | **A/R** | I | I | I | I | C |
| **Carga factura proveedor** | I | I | I | I | I | **A/R** |
| **Validación 3-way (PO+Recep+QC)** | I | C | C | C | I | **A/R** |

---

## Detalle por Área

### Ventas

| Responsabilidad | Tipo |
|-----------------|------|
| Crear cotización | R |
| Enviar cotización al cliente | R |
| Confirmar venta (SO) | A/R |
| Generar factura al cliente | A/R |

### Compras

| Responsabilidad | Tipo |
|-----------------|------|
| Revisar POs generadas | R |
| Validar precios y condiciones | R |
| Confirmar órdenes de compra | A/R |
| Consultar sobre facturas de proveedores | C |

### Inventario

| Responsabilidad | Tipo |
|-----------------|------|
| Recibir materiales de proveedores | A/R |
| Ejecutar transferencias entre ubicaciones | A/R |
| Preparar entregas a clientes | A/R |
| Validar movimientos de stock | A/R |

### Calidad

| Responsabilidad | Tipo |
|-----------------|------|
| Ejecutar controles en recepciones | A/R |
| Ejecutar controles en manufactura | A/R |
| Aprobar/rechazar lotes | A/R |
| Gestionar alertas de calidad | A/R |

### Producción

| Responsabilidad | Tipo |
|-----------------|------|
| Ejecutar Work Orders | A/R |
| Registrar consumos de materiales | R |
| Registrar producción | R |
| Completar órdenes de manufactura | A/R |

### Contabilidad

| Responsabilidad | Tipo |
|-----------------|------|
| Registrar facturas de proveedores | A/R |
| Validar 3-way match (PO + Recepción + QC) | A/R |
| Aprobar pagos a proveedores | A/R |
| Registrar factura al cliente | C |

---

## Flujo de Aprobaciones

```
FACTURA PROVEEDOR
       │
       ▼
┌─────────────────────────────────────────┐
│  Contabilidad registra factura          │
└─────────────────┬───────────────────────┘
                  │
       ┌──────────┼──────────┐
       │          │          │
       ▼          ▼          ▼
   ┌───────┐  ┌───────┐  ┌───────┐
   │  PO   │  │ Recep │  │  QC   │
   │ OK?   │  │ OK?   │  │ OK?   │
   └───┬───┘  └───┬───┘  └───┬───┘
       │          │          │
       └──────────┼──────────┘
                  │
                  ▼
         ┌───────────────┐
         │ ¿Todo OK?     │
         └───────┬───────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
   ┌─────────┐      ┌──────────┐
   │ Validar │      │ Rechazar │
   │ Factura │      │ / Ajustar│
   └─────────┘      └──────────┘
```

---

## Escalamiento

| Situación | Escala a |
|-----------|----------|
| QC rechazado | Supervisor de Calidad → Compras |
| Diferencia PO vs Factura | Compras → Contabilidad |
| Demora en producción | Supervisor Producción → Ventas |
| Faltante en recepción | Inventario → Compras |
