# 3. BoM de Subcontratación

Las BoMs de subcontratación definen productos que son fabricados por proveedores externos.

## ¿Qué es una BoM de Subcontratación?

```
FLUJO NORMAL (BoM Fabricar):
  Componentes del stock → Fabricación interna → Producto

FLUJO SUBCONTRATACIÓN:
  Componentes del stock → Envío a proveedor → Proveedor fabrica → Recibimos producto
```

---

## 3.1 BoMs de Subcontratación Necesarias

### Bases Metálicas

El proveedor (Metalúrgica) provee el producto completo.
No enviamos materiales.

| Producto | Subcontratista | Componentes |
|----------|----------------|-------------|
| Base Acero Negro 180x90 | Metalúrgica | Ninguno |
| Base Acero Negro 220x100 | Metalúrgica | Ninguno |
| Base Acero Dorado 180x90 | Metalúrgica | Ninguno |
| Base Acero Dorado 220x100 | Metalúrgica | Ninguno |

### Tapas de Madera Terminadas

El proveedor (Lustrador) recibe la tapa sin terminar y la devuelve terminada.

| Producto | Subcontratista | Componentes |
|----------|----------------|-------------|
| Tapa Madera Terminada 180x90 (Lustre Mate) | Lustrador | Tapa Madera Sin Terminar 180x90 |
| Tapa Madera Terminada 180x90 (Lustre Brillante) | Lustrador | Tapa Madera Sin Terminar 180x90 |
| Tapa Madera Terminada 180x90 (Natural) | Lustrador | Tapa Madera Sin Terminar 180x90 |
| Tapa Madera Terminada 220x100 (Lustre Mate) | Lustrador | Tapa Madera Sin Terminar 220x100 |
| Tapa Madera Terminada 220x100 (Lustre Brillante) | Lustrador | Tapa Madera Sin Terminar 220x100 |
| Tapa Madera Terminada 220x100 (Natural) | Lustrador | Tapa Madera Sin Terminar 220x100 |

---

## 3.2 Crear BoM: Base Acero Negro 180x90

```
Manufactura → Productos → Listas de materiales → Nuevo
```

### Información Principal

| Campo | Valor |
|-------|-------|
| **Producto** | Base Acero Negro 180x90 |
| **Cantidad** | 1.00 |
| **Tipo de BoM** | **Subcontratación** |

!!! warning "Tipo de BoM"
    Seleccionar **Subcontratación**, no "Fabricar este producto".

### Subcontratistas

En la sección **Subcontratistas** (aparece al seleccionar tipo Subcontratación):

| Subcontratista |
|----------------|
| Metalúrgica Precisión S.A. |

### Componentes

Dejar **vacío** - el proveedor provee todo el material.

**Guardar**

---

## 3.3 Crear BoM: Tapa Madera Terminada 180x90 (Lustre Mate)

Esta BoM sí tiene componentes porque enviamos la tapa sin terminar al lustrador.

### Información Principal

| Campo | Valor |
|-------|-------|
| **Producto** | Tapa Madera Terminada 180x90 |
| **Variante del producto** | Lustre Mate |
| **Cantidad** | 1.00 |
| **Tipo de BoM** | **Subcontratación** |

### Subcontratistas

| Subcontratista |
|----------------|
| Lustres & Acabados Premium |

### Componentes

| Producto | Cantidad |
|----------|----------|
| Tapa Madera Sin Terminar 180x90 | 1.00 |

!!! info "¿Qué pasa con este componente?"
    Cuando se crea una PO al Lustrador, Odoo:

    1. Reserva la Tapa Sin Terminar del stock
    2. Crea un movimiento de envío al subcontratista
    3. Al recibir la Tapa Terminada, consume el componente

**Guardar**

---

## 3.4 Crear las BoMs Restantes

### Bases (sin componentes)

| Producto | Subcontratista |
|----------|----------------|
| Base Acero Negro 220x100 | Metalúrgica Precisión S.A. |
| Base Acero Dorado 180x90 | Metalúrgica Precisión S.A. |
| Base Acero Dorado 220x100 | Metalúrgica Precisión S.A. |

### Tapas Terminadas (con componente)

| Producto + Variante | Subcontratista | Componente |
|--------------------|----------------|------------|
| Tapa Madera Term. 180x90 (Lustre Brillante) | Lustrador | Tapa Sin Term. 180x90 |
| Tapa Madera Term. 180x90 (Natural) | Lustrador | Tapa Sin Term. 180x90 |
| Tapa Madera Term. 220x100 (Lustre Mate) | Lustrador | Tapa Sin Term. 220x100 |
| Tapa Madera Term. 220x100 (Lustre Brillante) | Lustrador | Tapa Sin Term. 220x100 |
| Tapa Madera Term. 220x100 (Natural) | Lustrador | Tapa Sin Term. 220x100 |

---

## 3.5 Operaciones en BoM de Subcontratación (Opcional)

Podés agregar operaciones para:
- Planificar tiempos
- Ver en el Gantt
- Costear el trabajo del proveedor

### Ejemplo para Tapa Terminada

| Operación | Work Center | Duración |
|-----------|-------------|----------|
| Preparación superficie | LUST | 30 min |
| Aplicación lustre | LUST | 60 min |
| Secado y pulido | LUST | 30 min |
| Control de calidad | QC | 15 min |

---

## Verificación

### Lista de BoMs de Subcontratación

```
Manufactura → Productos → Listas de materiales
```

Filtrar por **Tipo = Subcontratación**:

| Producto | Subcontratista | Componentes |
|----------|----------------|-------------|
| Base Acero Negro 180x90 | Metalúrgica | 0 |
| Base Acero Negro 220x100 | Metalúrgica | 0 |
| Base Acero Dorado 180x90 | Metalúrgica | 0 |
| Base Acero Dorado 220x100 | Metalúrgica | 0 |
| Tapa Madera Term. 180x90 (Mate) | Lustrador | 1 |
| Tapa Madera Term. 180x90 (Brillante) | Lustrador | 1 |
| Tapa Madera Term. 180x90 (Natural) | Lustrador | 1 |
| Tapa Madera Term. 220x100 (Mate) | Lustrador | 1 |
| Tapa Madera Term. 220x100 (Brillante) | Lustrador | 1 |
| Tapa Madera Term. 220x100 (Natural) | Lustrador | 1 |

Total: **10 BoMs de subcontratación**

---

## Flujo Resultante

Con estas BoMs configuradas:

```
1. Venta Mesa (Madera, Negro, 180x90)
         │
         ▼
2. MO Mesa necesita:
   ├── Tapa Madera Terminada 180x90 (Lustre Mate)
   └── Base Acero Negro 180x90
         │
         ▼ (MTO genera POs)
3. PO a Lustrador (Tapa Terminada - subcontratación)
         │
         ▼ (confirmar PO)
4. Subcontract MO necesita: Tapa Sin Terminar
         │
         ▼ (ruta Dropship del componente)
5. PO a Carpintería
         │
         ▼ (confirmar PO)
6. DSC Picking (con QC) → Lustrador
   └── Carpintería envía directo al Lustrador
         │
         ▼
7. PO a Metalúrgica (Base)
   └── Metalúrgica provee: Base completa
         │
         ▼
8. Recepciones con QC
         │
         ▼
9. MO puede producirse
```

!!! info "Dropship Subcontractor"
    El componente "Tapa Sin Terminar" tiene ruta **Dropship**.
    Cuando el Lustrador (subcontratista) lo necesita, Odoo:

    1. Crea PO a Carpintería automáticamente
    2. Genera picking DSC (Dropship Subcontractor)
    3. El envío va directo Carpintería → Lustrador (sin pasar por stock)

---

## Resumen

| Tipo BoM | Cantidad | Subcontratista |
|----------|----------|----------------|
| Bases (sin componentes) | 4 | Metalúrgica |
| Tapas Terminadas (con componente) | 6 | Lustrador |
| **Total subcontratación** | **10** | |
