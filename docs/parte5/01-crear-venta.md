# 1. Crear la Venta

Iniciamos el flujo creando un pedido de venta.

## Acceder a Ventas

```
Ventas → Pedidos → Nuevo
```

---

## 1.1 Crear el Pedido

### Información del Cliente

| Campo | Valor |
|-------|-------|
| **Cliente** | (seleccionar o crear uno de prueba) |

### Líneas del Pedido

Click en **Agregar producto** en la pestaña de líneas:

| Campo | Valor |
|-------|-------|
| **Producto** | Mesa Comedor Premium |

### Seleccionar Variante

Al seleccionar el producto, aparecerá un diálogo para elegir la variante:

| Atributo | Valor |
|----------|-------|
| **Material Tapa** | Madera Terminada |
| **Material Base** | Acero Negro |
| **Medidas** | 180x90 |
| **Terminación** | Lustre Mate |

### Completar Línea

| Campo | Valor |
|-------|-------|
| **Cantidad** | 1 |
| **Precio** | (se completa automáticamente) |

---

## 1.2 Verificar la Ruta

Antes de confirmar, verificá que el producto tiene la ruta correcta:

1. Click en el producto en la línea
2. Ir a la pestaña **Inventario** del producto
3. Verificar que tiene: **Reponer bajo pedido (MTO)** + **Fabricar**

!!! warning "Ruta MTO"
    Si el producto no tiene la ruta MTO, la orden de fabricación
    NO se creará automáticamente al confirmar la venta.

---

## 1.3 Confirmar el Pedido

1. Click en **Confirmar**
2. El estado cambia a **Pedido de Venta**

### ¿Qué sucede al confirmar?

```
Confirmar SO
     │
     ▼
Sistema detecta ruta MTO + Fabricar
     │
     ▼
Crea Manufacturing Order (MO)
     │
     ▼
MO necesita componentes con ruta MTO + Comprar
     │
     ▼
Crea Purchase Orders (POs) a proveedores
```

---

## 1.4 Ver Documentos Generados

### Smart Buttons

Después de confirmar, aparecen botones inteligentes en el SO:

| Botón | Descripción |
|-------|-------------|
| **Entrega** | Orden de entrega pendiente |
| **Fabricación** | MO generada automáticamente |

### Verificar MO

Click en el botón de **Fabricación** para ver la orden de manufactura creada.

---

## Verificación

### Estado del SO

| Campo | Valor esperado |
|-------|----------------|
| **Estado** | Pedido de Venta |
| **Entrega** | Pendiente |

### Documentos Creados

```
Ventas → Pedidos → [Tu pedido]
```

Debería mostrar:
- 1 Delivery Order (pendiente)
- 1 Manufacturing Order (borrador o confirmada)

---

## Siguiente Paso

Verificar que se crearon correctamente la MO y las POs.

➡️ [Verificar MO y POs](02-mo-pos.md)
