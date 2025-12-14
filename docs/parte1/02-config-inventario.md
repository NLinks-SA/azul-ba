# 2. Configuración de Inventario

## Acceder a la Configuración

1. Ir a **Inventario**
2. Click en **Configuración → Ajustes**

---

## 2.1 Activar Ubicaciones y Rutas

### Ubicación
```
Inventario → Configuración → Ajustes → sección "Warehouse"
```

### Configuración

En la sección **Warehouse**, activar las siguientes opciones:

| Opción en UI | Descripción | Activar |
|--------------|-------------|---------|
| **Track product location in your warehouse** | Habilita ubicaciones múltiples (Storage Locations) | ☑ Sí |
| **Use your own routes** | Habilita rutas personalizadas (Multi-Step Routes) | ☑ Sí |

!!! info "¿Por qué estas opciones?"
    - **Track product location**: Permite crear ubicaciones específicas (Stock, Subcontratación, etc.)
    - **Use your own routes**: Permite configurar flujos personalizados y ver la ruta Dropship

### Guardar
Click en **Guardar** para aplicar los cambios.

---

## 2.2 Configurar el Almacén (Simplificado)

Para esta demo usamos un flujo simplificado de **1 paso**.

### Ubicación
```
Inventario → Configuración → Almacenes
```

### Pasos

1. Click en el almacén principal
2. Configurar:

| Campo | Valor | Descripción |
|-------|-------|-------------|
| **Incoming Shipments** | Receive goods directly (1 step) | Directo a Stock |
| **Outgoing Shipments** | Deliver goods directly (1 step) | Directo desde Stock |

!!! tip "¿Por qué 1 paso?"
    Para esta demo simplificamos el flujo. El control de calidad se hace
    en el picking **DSC** (Dropship Subcontractor), no en recepciones normales.

---

## 2.3 Crear Ubicaciones de Subcontratista

### Ubicación
```
Inventario → Configuración → Ubicaciones
```

### ¿Por qué crear estas ubicaciones?

Cada subcontratista necesita una ubicación para:

- Rastrear materiales enviados al proveedor
- Destino del Dropship Subcontractor (DSC)
- Control de inventario en tránsito

### Importante: Jerarquía Correcta

!!! warning "Ubicación Padre"
    Las ubicaciones de subcontratista deben ser hijas de **"Subcontratación"**
    (no de "Vendors"), para que el Dropship Subcontractor funcione correctamente.

    ```
    Subcontratación/
    ├── Subcontract - Carpintería Hnos. García
    ├── Subcontract - Lustres & Acabados
    ├── Subcontract - Metalúrgica Precisión
    ├── Subcontract - Marmolería Del Sur
    └── Subcontract - Neolith Argentina
    ```

### Validación Técnica: Jerarquía de Ubicaciones

Para verificar que las ubicaciones están correctamente configuradas:

1. La ubicación padre **"Subcontratación"** debe:
   - Tener `is_subcontracting_location = True`
   - Tener `usage = internal`

2. Cada ubicación hija debe:
   - Tener la ubicación "Subcontratación" como padre (`location_id`)
   - Heredar automáticamente `is_subcontracting_location = True`
   - Tener `usage = internal` (no transit)

!!! info "¿Por qué `internal` y no `transit`?"
    Odoo requiere que las ubicaciones de subcontratación tengan `usage = internal`
    (no `transit`). Esto permite:

    - Rastrear el inventario exacto en cada subcontratista
    - Manejar correctamente el consumo de materiales
    - Aplicar reglas de stock y reordenamiento

### Pasos

1. Buscar la ubicación **"Subcontratación"** (creada automáticamente por el módulo mrp_subcontracting)
2. Click en **Nuevo** para crear cada ubicación de subcontratista:

| Nombre | Tipo | Ubicación Padre |
|--------|------|-----------------|
| Subcontract - Carpintería Hnos. García | Interna | Subcontratación |
| Subcontract - Lustres & Acabados | Interna | Subcontratación |
| Subcontract - Metalúrgica Precisión | Interna | Subcontratación |
| Subcontract - Marmolería Del Sur | Interna | Subcontratación |
| Subcontract - Neolith Argentina | Interna | Subcontratación |

---

## 2.4 Verificar Picking Type DSC

Al instalar el módulo `mrp_subcontracting_dropshipping`, se crea automáticamente el Picking Type **DSC** (Dropship Subcontractor).

### Verificar

```
Inventario → Configuración → Tipos de operación
```

Buscar:

| Nombre | Código | Descripción |
|--------|--------|-------------|
| Dropship Subcontractor | DSC | Envío directo de proveedor a subcontratista |

!!! info "¿Qué es el Picking Type DSC?"
    Es el tipo de operación que se usa cuando un proveedor envía materiales
    **directamente** a un subcontratista:

    ```
    Proveedor (Carpintería) ──DSC──► Subcontratista (Lustrador)
    ```

    - **Origen**: Partners/Vendors (ubicación genérica de proveedores)
    - **Destino**: Subcontratación (ubicación padre de subcontratistas)

### Verificar Configuración DSC

El Picking Type DSC debe tener:

| Campo | Valor Correcto |
|-------|----------------|
| `default_location_src_id` | Partners/Vendors |
| `default_location_dest_id` | Subcontratación (la ubicación padre) |
| `code` | `dropship_subcontractor` |

Esto permite que el destino específico se determine por el `dest_address_id` de la PO
(la ubicación del subcontratista que necesita el material).

### Validación de stock.rule DSC

El módulo `mrp_subcontracting_dropshipping` crea automáticamente una regla de stock
que conecta la ruta Dropship con el picking type DSC.

Para verificar:

```
Inventario → Configuración → Reglas de rutas
```

Buscar la regla con:

| Campo | Valor |
|-------|-------|
| **Nombre** | (contiene "DSC" o "Dropship Subcontractor") |
| **Ruta** | Dropship |
| **Picking Type** | Dropship Subcontractor |
| **Acción** | Buy |

Esta regla es **crítica**: sin ella, los productos con ruta Dropship no generarán
pickings DSC cuando un subcontratista los necesite.

---

## 2.5 Activar Ruta MTO

### Ubicación
```
Inventario → Configuración → Rutas
```

### Verificar Ruta MTO

Buscar la ruta **"Replenish on Order (MTO)"** y verificar:

| Campo | Valor |
|-------|-------|
| **Active** | ✅ Sí |
| **Product Selectable** | ✅ Sí |

Si no está activa, activarla para que los productos puedan usar MTO.

---

## Verificación

Al finalizar deberías tener:

```
📍 Ubicaciones
├── WH/
│   └── Stock          ← Almacén principal
├── Subcontratación/   ← Padre de ubicaciones de subcontratistas
│   ├── Subcontract - Carpintería Hnos. García
│   ├── Subcontract - Lustres & Acabados
│   ├── Subcontract - Metalúrgica Precisión
│   ├── Subcontract - Marmolería Del Sur
│   └── Subcontract - Neolith Argentina
└── Partners/Vendors   ← Ubicación genérica de proveedores

📋 Tipos de Operación
├── Recepciones (WH/IN)
├── Entregas (WH/OUT)
└── Dropship Subcontractor (DSC)  ← Para envíos proveedor→subcontratista
```

---

## Resumen de Cambios

| Configuración | Valor |
|---------------|-------|
| Multi-Step Routes | ✅ Activado |
| Almacén - Recepción | 1 paso (directo) |
| Almacén - Envío | 1 paso (directo) |
| Ubicaciones subcontratista | 5 (bajo "Subcontratación") |
| Picking Type DSC | ✅ Verificado |
| Ruta MTO | ✅ Activa y seleccionable |

!!! note "Ya no necesitamos Ruta Resupply Lustrador"
    Con el módulo `mrp_subcontracting_dropshipping`, la ruta **Dropship** en el producto
    es suficiente. Odoo genera automáticamente el DSC Picking cuando un subcontratista
    necesita un componente con esa ruta.
