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
| Lustres & Acabados Premium | Tapa Madera Terminada 180x90 (Lustre Mate) | 1 |
| Metalúrgica Precisión S.A. | Base Acero Negro 180x90 | 1 |

!!! note "Subcontratación"
    La PO al Lustrador es por **subcontratación**. Al confirmarla, se creará
    automáticamente una **Subcontract MO** que necesitará la Tapa Sin Terminar.

!!! info "¿Dónde está la PO a Carpintería?"
    La PO a Carpintería (por la Tapa Sin Terminar) **NO existe todavía**.
    Se creará automáticamente cuando se confirme la PO al Lustrador,
    gracias al flujo **Dropship Subcontractor**.

---

## 2.3 Confirmar las POs

### Orden de Confirmación

```
1. PO Metalúrgica (Base)
   └── Genera recepción normal

2. PO Lustrador (Tapa Terminada) ← CLAVE
   └── Al confirmar:
       ├── Crea Subcontract MO
       └── Subcontract MO necesita Tapa Sin Terminar (ruta Dropship)
           └── Sistema crea PO a Carpintería automáticamente
               └── Genera DSC Picking (Carpintería → Lustrador directo)
```

### Confirmar PO a Metalúrgica

1. Abrir la PO a Metalúrgica
2. Click en **Confirmar pedido**
3. Se genera una recepción normal

### Confirmar PO a Lustrador (Subcontratación)

1. Abrir la PO a Lustres & Acabados Premium
2. Click en **Confirmar pedido**
3. **Automáticamente** Odoo:
   - Crea una **Subcontract MO** para la Tapa Terminada
   - Detecta que necesita Tapa Sin Terminar (componente de la BoM de subcontratación)
   - La Tapa Sin Terminar tiene ruta **Dropship**
   - Crea PO a **Carpintería** automáticamente
   - Genera un **DSC Picking** (Dropship Subcontractor)

---

## 2.4 Verificar el Flujo Dropship Subcontractor

### Ver la PO a Carpintería (creada automáticamente)

```
Compras → Pedidos → Órdenes de compra
```

Buscar PO a **Carpintería Hnos. García**:

| Campo | Valor |
|-------|-------|
| **Proveedor** | Carpintería Hnos. García |
| **Producto** | Tapa Madera Sin Terminar 180x90 |
| **Dropship Address** | Lustres & Acabados Premium (el subcontratista) |

!!! info "Dropship Address"
    El campo `dest_address_id` (Dropship Address) indica que el proveedor
    debe enviar el material **directamente al Lustrador**, no a nuestro almacén.

### Ver el DSC Picking

```
Inventario → Operaciones → Dropship Subcontractor
```

O buscar picking con código **DSC**:

| Campo | Valor |
|-------|-------|
| **Tipo** | Dropship Subcontractor (DSC) |
| **Producto** | Tapa Madera Sin Terminar 180x90 |
| **Origen** | Partners/Vendors |
| **Destino** | Subcontract - Lustres & Acabados |
| **Quality Check** | 🔴 Pendiente |

!!! warning "¿Qué es DSC Picking?"
    El **DSC Picking** (Dropship Subcontractor) es un movimiento especial donde
    un proveedor envía materiales **directamente** a un subcontratista,
    sin pasar por nuestro almacén.

    ```
    Carpintería ──(DSC)──► Lustrador (NO pasa por WH/Stock)
    ```

---

## 2.5 Diagrama de Flujo Actualizado

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
                  │ MTO
    ┌─────────────┴─────────────┐
    │                           │
    ▼                           ▼
┌───────────┐             ┌───────────┐
│    PO     │             │    PO     │
│ Metalúrg  │             │ Lustrador │ (subcontratación)
└─────┬─────┘             └─────┬─────┘
      │                         │
      ▼                         ▼ Confirmar
┌───────────┐             ┌───────────┐
│   Recep   │             │Subcontract│
│   Base    │             │    MO     │
└───────────┘             └─────┬─────┘
                                │ necesita Tapa Sin Terminar
                                │ (ruta Dropship)
                                ▼
                          ┌───────────┐
                          │    PO     │ (creada automáticamente)
                          │Carpintería│
                          └─────┬─────┘
                                │
                                ▼
                          ┌───────────┐
                          │    DSC    │ ← Dropship Subcontractor
                          │  Picking  │   Carpintería → Lustrador
                          │  + QC     │   (con Control de Calidad)
                          └───────────┘
```

---

## Verificación Final

### Lista de Verificación

- [ ] MO creada con componentes correctos
- [ ] PO a Metalúrgica confirmada
- [ ] PO a Lustrador confirmada (subcontratación)
- [ ] Subcontract MO creada automáticamente
- [ ] PO a Carpintería creada automáticamente (Dropship)
- [ ] DSC Picking visible con QC pendiente

---

## Siguiente Paso

Procesar las recepciones y el DSC Picking con control de calidad.

➡️ [Recepciones y DSC](03-recepciones.md)
