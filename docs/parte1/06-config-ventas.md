# 6. Configuración de Ventas (MTO)

## ¿Qué es MTO?

**MTO = Make to Order** (Fabricar bajo pedido)

Con MTO activo:
- No se mantiene stock del producto final
- Cada venta genera automáticamente una orden de fabricación
- Los componentes se compran/fabrican solo cuando hay demanda

---

## 6.1 Verificar Ruta MTO

### Ubicación
```
Inventario → Configuración → Rutas
```

!!! tip "Ver rutas inactivas"
    Si no ves la ruta MTO, activá el filtro para ver rutas **archivadas/inactivas**.

### Buscar la Ruta

Buscar: **"Replenish on Order (MTO)"** o **"MTO"**

| Campo | Valor esperado |
|-------|----------------|
| Nombre | Replenish on Order (MTO) |
| Activa | ✅ Debe estar activa |
| Seleccionable en producto | ✅ Debe estar activo |

---

## 6.2 Activar la Ruta MTO

Si la ruta está inactiva o no es seleccionable:

1. Click en la ruta MTO
2. Editar:

| Campo | Valor |
|-------|-------|
| Activa | ✅ Sí |
| Seleccionable en producto | ✅ Sí |

3. **Guardar**

---

## 6.3 Otras Rutas Importantes

Verificar que estas rutas también estén activas y seleccionables:

| Ruta | Uso |
|------|-----|
| **Buy** | Productos que se compran |
| **Manufacture** | Productos que se fabrican |
| **Replenish on Order (MTO)** | Productos bajo pedido |

### Combinaciones de Rutas

Para nuestro caso:

| Producto | Rutas |
|----------|-------|
| Mesa (final) | Manufacture + MTO |
| Componentes (tapas, bases) | Buy + MTO |

!!! info "¿Por qué Buy + MTO en componentes?"
    - **Buy**: Indica que se compran a proveedores
    - **MTO**: Se compran solo cuando hay demanda (desde una MO)

    Sin MTO, Odoo esperaría stock existente en lugar de generar una PO.

---

## 6.4 Verificación

Ir a un producto de prueba:

```
Inventario → Productos → [Cualquier producto]
```

En la pestaña **Inventario**, sección **Operaciones**, verificar que el campo **Rutas** permite seleccionar:

- ☑ Buy
- ☑ Manufacture
- ☑ Replenish on Order (MTO)

Si alguna no aparece, volver al paso 6.2 y verificar que `Seleccionable en producto` esté activo.

---

## Resumen

| Configuración | Estado |
|---------------|--------|
| Ruta MTO | ✅ Activa |
| Ruta MTO - Seleccionable en producto | ✅ Activa |
| Ruta Buy | ✅ Activa |
| Ruta Manufacture | ✅ Activa |

---

## Siguiente Paso

Con la configuración del sistema completa, pasamos a crear los **Datos Maestros**:

➡️ [Parte 2: Datos Maestros](../parte2/index.md)
