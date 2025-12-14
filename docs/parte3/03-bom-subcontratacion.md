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

## 3.2 Códigos de BoM con Variantes

Para identificar fácilmente cada BoM, especialmente cuando hay muchas variantes,
usamos el campo **Código** (Reference) que aparece en el nombre de la BoM.

### Patrón para Tapas Terminadas

```
TAPA-TERM-{medida}-{terminación}
```

Ejemplos:
- `TAPA-TERM-180x90-LUST` (Lustre Mate, 180x90)
- `TAPA-TERM-180x90-BRIL` (Lustre Brillante, 180x90)
- `TAPA-TERM-220x100-NATU` (Natural, 220x100)

### Patrón para Mesa

```
MESA-{material_tapa}-{terminación}-{base}-{medida}
```

Ejemplos:
- `MESA-MAD-LUST-ACE-180x90` (Madera, Lustre Mate, Acero Negro, 180x90)
- `MESA-MAR-SINT-DOE-220x100` (Mármol, Sin Terminación, Acero Dorado, 220x100)
- `MESA-NEO-SINT-ACE-180x90` (Neolith, Sin Terminación, Acero Negro, 180x90)

### ¿Cómo se ve el código?

El código aparece en el display_name de la BoM:

```
TAPA-TERM-180x90-LUST: Tapa Madera Terminada 180x90 (Lustre Mate)
```

Esto facilita:
- Identificar variantes en listas
- Buscar BoMs específicas
- Exportar datos con referencias claras

---

## 3.3 Crear BoM: Base Acero Negro 180x90

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

## 3.4 Mapeo Variante → Componente

Cada variante de Tapa Terminada usa el mismo componente base (Tapa Sin Terminar),
pero es importante entender el mapeo:

| Variante Tapa Terminada | Componente Requerido |
|------------------------|---------------------|
| Tapa Madera Terminada 180x90 (Lustre Mate) | Tapa Madera Sin Terminar 180x90 |
| Tapa Madera Terminada 180x90 (Lustre Brillante) | Tapa Madera Sin Terminar 180x90 |
| Tapa Madera Terminada 180x90 (Natural) | Tapa Madera Sin Terminar 180x90 |
| Tapa Madera Terminada 220x100 (Lustre Mate) | Tapa Madera Sin Terminar 220x100 |
| Tapa Madera Terminada 220x100 (Lustre Brillante) | Tapa Madera Sin Terminar 220x100 |
| Tapa Madera Terminada 220x100 (Natural) | Tapa Madera Sin Terminar 220x100 |

!!! tip "Mapeo por Medida"
    El mapeo es por **medida**, no por terminación:
    - 180x90 → Tapa Sin Terminar 180x90
    - 220x100 → Tapa Sin Terminar 220x100

    La terminación es trabajo del Lustrador, no afecta qué componente usamos.

---

## 3.5 Crear BoM: Tapa Madera Terminada 180x90 (Lustre Mate)

Esta BoM sí tiene componentes porque enviamos la tapa sin terminar al lustrador.

### Información Principal

| Campo | Valor |
|-------|-------|
| **Producto** | Tapa Madera Terminada 180x90 |
| **Variante del producto** | Lustre Mate |
| **Código** | TAPA-TERM-180x90-LUST |
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

    1. Detecta que el componente tiene ruta **Dropship**
    2. Crea una PO a Carpintería automáticamente
    3. Genera un picking **DSC** para envío directo Carpintería → Lustrador
    4. Al validar el DSC (con QC), el componente llega al Lustrador

**Guardar**

---

## 3.6 Crear las BoMs Restantes

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

## 3.7 BoMs de Subcontratación - Sin Operaciones

!!! warning "Las BoMs de subcontratación NO llevan operaciones"
    A diferencia de las BoMs de fabricación interna, las BoMs de subcontratación
    **no tienen operaciones** porque:

    - El subcontratista hace el trabajo, no nosotros
    - No controlamos sus procesos internos
    - La Subcontract MO se completa automáticamente al recibir el producto
    - El tiempo de entrega se define en el Lead Time del proveedor
    - El QC se hace en el **DSC Picking** (ver Parte 4)

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
