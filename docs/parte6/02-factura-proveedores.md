# 2. Validación de Facturas de Proveedores

Proceso crítico para validar facturas de subcontratistas con control 3-way match + QC.

---

## Objetivo

**Pagar solo lo que fue recibido Y aprobado por calidad.**

```
VALIDACIÓN 3-WAY MATCH + QC
        │
        ├── 1. Factura vs Orden de Compra (precios, cantidades)
        │
        ├── 2. Factura vs Recepciones (cantidades recibidas)
        │
        └── 3. Recepciones vs QC (calidad aprobada)
```

---

## 2.1 Recibir Factura del Proveedor

El proveedor envía su factura (email, portal, papel).

### Información a Verificar

| Dato | Verificar contra |
|------|------------------|
| Número de factura proveedor | Único, no duplicado |
| Fecha | Dentro del período fiscal |
| Referencia a nuestra PO | Orden de compra correcta |
| Productos | Coinciden con PO |
| Cantidades | ≤ Cantidades recibidas |
| Precios | Coinciden con PO |

---

## 2.2 Registrar la Factura `MANUAL`

```
Contabilidad → Proveedores → Facturas → Crear
```

### Datos del Encabezado

| Campo | Valor |
|-------|-------|
| **Proveedor** | Seleccionar (ej: Lustres & Acabados) |
| **Referencia factura** | Número de factura del proveedor |
| **Fecha factura** | Fecha del documento |
| **Fecha contable** | Fecha de registro |

### Agregar Líneas desde PO

1. Click en botón **Agregar líneas desde OC**
2. Seleccionar la(s) PO correspondiente(s)
3. Verificar que las líneas se agregan correctamente

!!! tip "Mejor Práctica"
    Siempre usar "Agregar líneas desde OC" en lugar de crear líneas manualmente.
    Esto asegura la trazabilidad y facilita la validación.

---

## 2.3 Validar contra Orden de Compra `MANUAL`

### Acceder a la PO

Click en Smart Button **Órdenes de Compra** o ir a:

```
Compras → Órdenes → [Número de PO]
```

### Verificar

| Campo | Factura | PO | ¿Coincide? |
|-------|---------|-----|------------|
| Producto | X | X | ✅ |
| Cantidad | X | X | ✅ |
| Precio unitario | X | X | ✅ |
| Impuestos | X | X | ✅ |

### Si hay Diferencias

| Diferencia | Acción |
|------------|--------|
| Precio mayor | Rechazar o solicitar nota de crédito |
| Cantidad mayor | Rechazar exceso |
| Producto incorrecto | Rechazar factura |

---

## 2.4 Validar contra Recepciones `MANUAL`

### Acceder a Recepciones

Click en Smart Button **Recepciones** o ir a:

```
Inventario → Informes → Historial de movimientos
```

Filtrar por:
- Proveedor
- Producto
- Fecha

### Verificar

| Verificación | Regla |
|--------------|-------|
| Cantidad facturada | ≤ Cantidad recibida |
| Producto | Coincide con recepción |
| Lote/Serie | Si aplica, coincide |

### Si hay Diferencias

| Diferencia | Acción |
|------------|--------|
| Factura > Recibido | Solo pagar lo recibido |
| Producto no recibido | Rechazar línea |

---

## 2.5 Validar contra Quality Checks `MANUAL`

### Acceder a QC

```
Calidad → Quality Checks
```

Filtrar por:
- Producto
- Proveedor (picking origin)
- Fecha de recepción

### Verificar

| Estado QC | Acción en Factura |
|-----------|-------------------|
| **Pass** ✅ | Aprobar pago |
| **Fail** ❌ | Rechazar / Nota de crédito |
| **Pendiente** ⏳ | Esperar resultado |

### Si QC Falló

```
QC Fallido
    │
    ├── ¿Material devuelto? → No pagar
    │
    ├── ¿Material aceptado con descuento? → Solicitar nota de crédito
    │
    └── ¿Reclamo en proceso? → Retener pago
```

---

## 2.6 Validar la Factura `MANUAL`

Una vez verificado todo:

1. Revisar totales
2. Click en **Confirmar**

### Resultado

| Impacto | Descripción |
|---------|-------------|
| **Estado** | Cambia a "Publicado" |
| **Contabilidad** | Asiento contable generado |
| **Cuenta por pagar** | Deuda con proveedor registrada |
| **Costo** | Capitalizado en inventario |

---

## 2.7 Programar Pago `MANUAL`

```
Contabilidad → Proveedores → Pagos → Crear
```

O desde la factura: **Registrar pago**

| Campo | Valor |
|-------|-------|
| **Proveedor** | Seleccionado automáticamente |
| **Monto** | Total de factura |
| **Fecha de pago** | Según términos |
| **Diario** | Banco |

---

## Flujo Visual

```
┌─────────────────────────────────────────────────────────────┐
│         VALIDACIÓN FACTURA PROVEEDOR (3-WAY + QC)          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Proveedor envía Factura                                   │
│            │                                                │
│            ▼                                                │
│   ┌─────────────────┐                                       │
│   │ Registrar en    │                                       │
│   │ Contabilidad    │                                       │
│   └────────┬────────┘                                       │
│            │                                                │
│   ┌────────┴────────────────────────┐                      │
│   │                                 │                       │
│   ▼                                 ▼                       │
│ ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│ │ Validar  │    │ Validar  │    │ Validar  │              │
│ │ vs PO    │    │vs Recep. │    │ vs QC    │              │
│ └────┬─────┘    └────┬─────┘    └────┬─────┘              │
│      │               │               │                      │
│      └───────────────┼───────────────┘                      │
│                      │                                      │
│                      ▼                                      │
│              ┌──────────────┐                               │
│              │ ¿Todo OK?    │                               │
│              └──────┬───────┘                               │
│                     │                                       │
│         ┌───────────┴───────────┐                          │
│         │                       │                          │
│         ▼                       ▼                          │
│   ┌───────────┐          ┌───────────┐                     │
│   │  Validar  │          │ Rechazar/ │                     │
│   │  Factura  │          │  Ajustar  │                     │
│   └─────┬─────┘          └───────────┘                     │
│         │                                                   │
│         ▼                                                   │
│   ┌───────────┐                                             │
│   │   Pagar   │                                             │
│   └───────────┘                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Checklist de Validación

```markdown
## Validación Factura Proveedor: [Número]

### 1. Datos Generales
- [ ] Proveedor correcto
- [ ] Número factura único (no duplicado)
- [ ] Fecha dentro del período

### 2. vs Orden de Compra
- [ ] PO identificada: ____________
- [ ] Productos coinciden
- [ ] Cantidades coinciden
- [ ] Precios coinciden
- [ ] Impuestos correctos

### 3. vs Recepciones
- [ ] Recepción identificada: ____________
- [ ] Cantidad facturada ≤ recibida
- [ ] Fecha recepción antes de factura

### 4. vs Quality Control
- [ ] QC identificado: ____________
- [ ] Estado: Pass / Fail
- [ ] Si Fail: acción tomada ____________

### 5. Aprobación
- [ ] Validado por: ____________
- [ ] Fecha: ____________
```

---

## Casos Especiales

### Factura Parcial

El proveedor factura solo parte de la PO:

1. Agregar solo las líneas facturadas
2. Las líneas restantes quedan pendientes
3. Se facturarán en documento posterior

### Nota de Crédito

Si hay que ajustar una factura ya validada:

```
Contabilidad → Proveedores → Facturas → [Factura] → Agregar nota de crédito
```

### Factura sin PO

!!! danger "No Recomendado"
    Evitar registrar facturas sin PO previa.
    Si es necesario:
    1. Crear PO retroactiva
    2. O documentar excepción con aprobación

---

## Reportes Útiles

### Facturas Pendientes de Validar

```
Contabilidad → Proveedores → Facturas
```

Filtrar: Estado = Borrador

### Antigüedad de Cuentas por Pagar

```
Contabilidad → Reportes → Antigüedad de cuentas por pagar
```

### Facturas vs Recepciones

```
Compras → Reportes → Compras por producto
```

---

## Volver

➡️ [Índice Facturación](index.md)
