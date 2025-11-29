# 1. Facturación al Cliente

Proceso para generar la factura al cliente después de la entrega.

---

## Prerrequisitos

Antes de facturar, verificar:

- [x] Orden de venta confirmada (SO)
- [x] Manufactura completada (MO en estado "Hecho")
- [x] Entrega validada (Delivery Order completado)

---

## 1.1 Acceder a la Orden de Venta

```
Ventas → Pedidos → [Seleccionar SO]
```

### Verificar Estado

| Campo | Valor esperado |
|-------|----------------|
| **Estado** | Pedido de Venta |
| **Entrega** | Entregado (verde) |
| **Facturación** | Para facturar |

!!! warning "Política de Facturación"
    La factura solo se puede crear si:
    - Política = "Cantidades entregadas" → después de entregar
    - Política = "Cantidades ordenadas" → después de confirmar SO

---

## 1.2 Crear la Factura `MANUAL`

### Desde la SO

1. Abrir la SO
2. Click en botón **Crear factura**
3. Seleccionar tipo:

| Opción | Uso |
|--------|-----|
| **Factura regular** | Factura completa por todo lo entregado |
| **Anticipo (porcentaje)** | Cobro parcial adelantado |
| **Anticipo (monto fijo)** | Cobro de monto específico |

4. Click en **Crear y ver factura**

---

## 1.3 Revisar la Factura `MANUAL`

### Verificar Datos

| Campo | Verificar |
|-------|-----------|
| **Cliente** | Correcto |
| **Fecha factura** | Fecha actual o según política |
| **Líneas** | Productos y cantidades correctas |
| **Impuestos** | Aplicados correctamente |
| **Total** | Coincide con SO |

### Smart Buttons

| Botón | Información |
|-------|-------------|
| **Origen** | Link a la SO |
| **Entregas** | Documentos de entrega relacionados |

---

## 1.4 Validar la Factura `MANUAL`

1. Verificar todos los datos
2. Click en **Confirmar**

### Resultado

| Impacto | Descripción |
|---------|-------------|
| **Estado** | Cambia a "Publicado" |
| **Número** | Se asigna número de factura |
| **Contabilidad** | Se genera asiento contable |
| **Cuenta por cobrar** | Se registra deuda del cliente |

---

## 1.5 Enviar la Factura `MANUAL`

### Por Email

1. Click en **Enviar e imprimir**
2. Verificar destinatario
3. Adjuntar PDF automáticamente
4. **Enviar**

### Descargar PDF

1. Click en **Imprimir** → **Facturas**
2. Descargar PDF

---

## 1.6 Registrar Pago (Opcional) `MANUAL`

Cuando el cliente paga:

```
Contabilidad → Clientes → Pagos → Crear
```

O desde la factura:

1. Abrir factura
2. Click en **Registrar pago**
3. Completar:

| Campo | Valor |
|-------|-------|
| **Diario** | Banco / Efectivo |
| **Monto** | Importe pagado |
| **Fecha** | Fecha del pago |
| **Memo** | Referencia del pago |

4. **Crear pago**

### Resultado

- Factura cambia a estado **Pagado**
- Se genera asiento de cobro
- Se cancela la cuenta por cobrar

---

## Flujo Visual

```
┌─────────────────────────────────────────────────────────────┐
│               FACTURACIÓN AL CLIENTE                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   SO Confirmada                                             │
│        │                                                    │
│        ▼                                                    │
│   ┌─────────┐      ┌─────────┐      ┌─────────┐           │
│   │   MO    │ ──▶  │ Entrega │ ──▶  │ Crear   │           │
│   │Completa │      │Validada │      │ Factura │           │
│   └─────────┘      └─────────┘      └────┬────┘           │
│                                          │                 │
│                                          ▼                 │
│                                    ┌──────────┐            │
│                                    │ Revisar  │            │
│                                    │  Datos   │            │
│                                    └────┬─────┘            │
│                                         │                  │
│                                         ▼                  │
│                    ┌─────────┐    ┌──────────┐            │
│                    │ Enviar  │◀───│ Confirmar│            │
│                    │ Cliente │    │ Factura  │            │
│                    └────┬────┘    └──────────┘            │
│                         │                                  │
│                         ▼                                  │
│                    ┌─────────┐                             │
│                    │ Cobrar  │                             │
│                    └─────────┘                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Verificación

### Lista de Facturas

```
Contabilidad → Clientes → Facturas
```

| Número | Cliente | Total | Estado |
|--------|---------|-------|--------|
| INV/2024/0001 | Cliente Demo | $X.XXX | Publicado / Pagado |

---

## Siguiente Paso

Ver el proceso de validación de facturas de proveedores.

➡️ [Validación Facturas Proveedores](02-factura-proveedores.md)
