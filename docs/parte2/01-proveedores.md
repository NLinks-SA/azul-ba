# 1. Proveedores

## Acceder a Proveedores

```
Compras → Pedidos → Proveedores
```

O también:

```
Contactos → Filtrar por "Es proveedor"
```

---

## 1.1 Crear Proveedores

Click en **Nuevo** y crear cada proveedor:

### Proveedor 1: Marmolería Del Sur

| Campo | Valor |
|-------|-------|
| **Nombre** | Marmolería Del Sur |
| **Es una empresa** | ✅ Sí |
| **Dirección** | (tu ciudad) |
| **Teléfono** | (opcional) |
| **Email** | marmoleria@ejemplo.com |

En pestaña **Compra y Venta**:

| Campo | Valor |
|-------|-------|
| **Es proveedor** | ✅ (se marca automáticamente) |

---

### Proveedor 2: Neolith Argentina

| Campo | Valor |
|-------|-------|
| **Nombre** | Neolith Argentina |
| **Es una empresa** | ✅ Sí |

---

### Proveedor 3: Carpintería Artesanal Hnos. García

| Campo | Valor |
|-------|-------|
| **Nombre** | Carpintería Artesanal Hnos. García |
| **Es una empresa** | ✅ Sí |

!!! info "Este proveedor"
    Produce las tapas de madera **SIN terminar**.
    Luego van al Lustrador para terminación.

---

### Proveedor 4: Lustres & Acabados Premium

| Campo | Valor |
|-------|-------|
| **Nombre** | Lustres & Acabados Premium |
| **Es una empresa** | ✅ Sí |

!!! info "Este proveedor"
    Recibe las tapas de madera sin terminar y aplica el lustrado/terminación.
    Es un **subcontratista** que procesa material que nosotros le enviamos.

---

### Proveedor 5: Metalúrgica Precisión S.A.

| Campo | Valor |
|-------|-------|
| **Nombre** | Metalúrgica Precisión S.A. |
| **Es una empresa** | ✅ Sí |

!!! info "Este proveedor"
    Produce las bases metálicas como **subcontratista**.
    Nosotros no le enviamos material, él provee todo.

---

## 1.2 Asignar Ubicaciones de Subcontratación

Para los proveedores que son subcontratistas, asignar la ubicación creada en la Parte 1.

### Pasos

1. Abrir el proveedor (ej: Carpintería Artesanal)
2. Ir a pestaña **Compra y Venta** o **Inventario**
3. Buscar campo: **Subcontractor Location** (Ubicación de subcontratista)
4. Seleccionar la ubicación correspondiente

### Asignaciones

| Proveedor | Ubicación |
|-----------|-----------|
| Carpintería Artesanal Hnos. García | Subcontract - Carpintería |
| Lustres & Acabados Premium | Subcontract - Lustrador |
| Metalúrgica Precisión S.A. | Subcontract - Metalúrgica |
| Marmolería Del Sur | Subcontract - Marmolería |
| Neolith Argentina | Subcontract - Neolith |

!!! tip "Si no ves el campo"
    El campo **Subcontractor Location** aparece después de:

    1. Activar Subcontracting en ajustes
    2. Crear las ubicaciones de subcontratista

---

## 1.3 Crear Clientes (Opcional)

Para probar el flujo completo, crear al menos un cliente:

```
Ventas → Pedidos → Clientes → Nuevo
```

| Campo | Valor |
|-------|-------|
| **Nombre** | Estudio de Arquitectura Modernista |
| **Es una empresa** | ✅ Sí |

---

## Verificación

### Lista de Proveedores

```
Compras → Pedidos → Proveedores
```

Deberías ver 5 proveedores:

| Proveedor | Ubicación Subcontrat. |
|-----------|----------------------|
| Marmolería Del Sur | Subcontract - Marmolería |
| Neolith Argentina | Subcontract - Neolith |
| Carpintería Artesanal Hnos. García | Subcontract - Carpintería |
| Lustres & Acabados Premium | Subcontract - Lustrador |
| Metalúrgica Precisión S.A. | Subcontract - Metalúrgica |

---

## Resumen

| Ítem | Cantidad |
|------|----------|
| Proveedores creados | 5 |
| Con ubicación subcontratista | 5 |
| Clientes (opcional) | 1+ |
