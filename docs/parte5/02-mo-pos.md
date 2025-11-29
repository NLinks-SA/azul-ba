# 2. Verificar MO y POs

Verificamos que el sistema generó automáticamente la orden de fabricación y las órdenes de compra.

## 2.1 Verificar Manufacturing Order

### Acceder a la MO

```
Manufactura → Operaciones → Órdenes de fabricación
```

O desde el SO, click en el smart button **Fabricación**.

### Datos de la MO

| Campo | Valor esperado |
|-------|----------------|
| **Producto** | Mesa Comedor Premium (variante seleccionada) |
| **Cantidad** | 1 |
| **Estado** | Borrador o Confirmada |
| **Origen** | Número del SO |

### Componentes (Pestaña Componentes)

La MO muestra los componentes necesarios según la BoM:

| Componente | Cantidad | Disponible |
|------------|----------|------------|
| Tapa Madera Terminada 180x90 (Lustre Mate) | 1 | 0 ❌ |
| Base Acero Negro 180x90 | 1 | 0 ❌ |

!!! info "Disponibilidad"
    Los componentes muestran 0 disponible porque son MTO
    y deben comprarse/fabricarse primero.

---

## 2.2 Verificar Purchase Orders

### Acceder a las POs

```
Compras → Pedidos → Solicitudes de presupuesto
```

### POs Generadas

Deberían existir las siguientes POs (en estado RFQ o confirmadas):

| Proveedor | Producto | Cantidad |
|-----------|----------|----------|
| Carpintería Hnos. García | Tapa Madera Sin Terminar 180x90 | 1 |
| Lustres & Acabados Premium | Tapa Madera Terminada 180x90 (Lustre Mate) | 1 |
| Metalúrgica Precisión S.A. | Base Acero Negro 180x90 | 1 |

!!! note "Cadena de Abastecimiento"
    La PO al Lustrador es por **subcontratación**: requiere primero
    recibir la Tapa Sin Terminar de la Carpintería, enviarla al Lustrador,
    y luego recibir la Tapa Terminada.

### Verificar Detalles de PO

Para cada PO, verificar:

| Campo | Descripción |
|-------|-------------|
| **Proveedor** | Correcto según el producto |
| **Producto** | El componente necesario |
| **Origen** | Referencia a la MO o SO |
| **Fecha prevista** | Calculada según lead time |

---

## 2.3 Confirmar las POs

### Confirmar Cada PO

1. Abrir la PO
2. Click en **Confirmar pedido**
3. El estado cambia a **Orden de compra**

### Orden de Confirmación Recomendada

```
1. PO Carpintería (Tapa Sin Terminar)
   └── Genera recepción

2. PO Metalúrgica (Base)
   └── Genera recepción

3. PO Lustrador (Tapa Terminada)
   └── Genera recepción + envío de componentes
```

---

## 2.4 Verificar Recepciones Generadas

### Acceder a Recepciones

```
Inventario → Operaciones → Recepciones
```

### Recepciones Esperadas

| Proveedor | Producto | Estado |
|-----------|----------|--------|
| Carpintería | Tapa Sin Terminar 180x90 | Preparado/Por hacer |
| Metalúrgica | Base Acero Negro 180x90 | Preparado/Por hacer |
| Lustrador | Tapa Terminada 180x90 | Esperando (componentes) |

---

## 2.5 Flujo de Subcontratación (Lustrador)

La PO al Lustrador tiene un flujo especial:

```
1. Confirmar PO al Lustrador
         │
         ▼
2. Sistema reserva Tapa Sin Terminar (del stock)
         │
         ▼
3. Crea movimiento de ENVÍO al subcontratista
         │
         ▼
4. Al recibir Tapa Terminada, consume la Sin Terminar
```

### Ver Movimientos de Subcontratación

En la PO del Lustrador:
- Pestaña **Productos** muestra la Tapa Terminada a recibir
- Link **Resupply** o movimiento asociado muestra el envío de componentes

---

## Diagrama de Flujo

```
        ┌─────────────────────┐
        │    Sale Order       │
        │  (Mesa confirmada)  │
        └─────────┬───────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  Manufacturing Order │
        │   (Mesa a fabricar) │
        └─────────┬───────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌───────┐   ┌───────────┐   ┌───────────┐
│  PO   │   │    PO     │   │    PO     │
│Carpint│   │ Metalúrg  │   │ Lustrador │
└───┬───┘   └─────┬─────┘   └─────┬─────┘
    │             │               │
    ▼             ▼               ▼
┌───────┐   ┌───────────┐   ┌───────────┐
│ Recep │   │   Recep   │   │  Recep +  │
│Tapa ST│   │   Base    │   │ Envío Sub │
└───────┘   └───────────┘   └───────────┘
```

---

## Verificación Final

### Lista de Verificación

- [ ] MO creada con componentes correctos
- [ ] PO a Carpintería con Tapa Sin Terminar
- [ ] PO a Metalúrgica con Base
- [ ] PO a Lustrador con Tapa Terminada (subcontratación)
- [ ] Todas las POs confirmadas
- [ ] Recepciones pendientes visibles

---

## Siguiente Paso

Procesar las recepciones con los controles de calidad.

➡️ [Recepciones con QC](03-recepciones.md)
