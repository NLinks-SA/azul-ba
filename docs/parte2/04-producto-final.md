# 4. Producto Final - Mesa

Ahora creamos el producto principal: la Mesa de Comedor con variantes.

## Acceder a Productos

```
Inventario → Productos → Productos → Nuevo
```

---

## 4.1 Crear la Mesa

### Pestaña: Información General

| Campo | Valor |
|-------|-------|
| **Nombre** | Mesa Comedor Premium |
| **Referencia interna** | MESA-PREMIUM |
| **Tipo de producto** | Almacenable |
| **Categoría** | Mobiliario / Mesas |
| **Precio de venta** | 1500.00 |
| **Coste** | 800.00 |

#### Configuración adicional

| Campo | Valor |
|-------|-------|
| **Se puede vender** | ✅ Sí |
| **Se puede comprar** | ❌ No |

!!! info "¿Por qué no se puede comprar?"
    La mesa se **fabrica** internamente, no se compra.
    Los componentes sí se compran.

---

### Pestaña: Atributos y Variantes

Agregar tres líneas de atributos:

| Atributo | Valores a seleccionar |
|----------|----------------------|
| Material Tapa | Mármol Carrara, Neolith Negro, Madera Paraíso |
| Material Base | Acero Negro, Acero Dorado |
| Medidas | 180x90 cm, 220x100 cm |

Al guardar, Odoo crea automáticamente:

```
3 × 2 × 2 = 12 variantes
```

---

### Pestaña: Inventario

| Campo | Valor |
|-------|-------|
| **Rutas** | ☑ Manufacture, ☑ Replenish on Order (MTO) |

!!! warning "Rutas críticas"
    - **Manufacture**: Indica que se fabrica
    - **MTO**: Genera MO automáticamente al confirmar venta

---

### Pestaña: Ventas

| Campo | Valor |
|-------|-------|
| **Tiempo de entrega al cliente** | 14 días |
| **Descripción para clientes** | Mesa de comedor premium. Seleccione material de tapa, base y medidas. |

---

## 4.2 Guardar y Verificar Variantes

Click en **Guardar**

### Ver las Variantes

Después de guardar, aparece un botón **Variantes** (o un número indicando la cantidad).

Click para ver las 12 variantes:

| Variante | Combinación |
|----------|-------------|
| 1 | Mármol Carrara + Acero Negro + 180x90 |
| 2 | Mármol Carrara + Acero Negro + 220x100 |
| 3 | Mármol Carrara + Acero Dorado + 180x90 |
| 4 | Mármol Carrara + Acero Dorado + 220x100 |
| 5 | Neolith Negro + Acero Negro + 180x90 |
| 6 | Neolith Negro + Acero Negro + 220x100 |
| 7 | Neolith Negro + Acero Dorado + 180x90 |
| 8 | Neolith Negro + Acero Dorado + 220x100 |
| 9 | Madera Paraíso + Acero Negro + 180x90 |
| 10 | Madera Paraíso + Acero Negro + 220x100 |
| 11 | Madera Paraíso + Acero Dorado + 180x90 |
| 12 | Madera Paraíso + Acero Dorado + 220x100 |

---

## 4.3 Configurar Precios por Variante (Opcional)

Si diferentes combinaciones tienen diferentes precios:

### Opción A: Extra por atributo

En **Atributos y Variantes**, editar cada valor:

| Valor | Precio extra |
|-------|--------------|
| Mármol Carrara | +200.00 |
| Neolith Negro | +100.00 |
| Madera Paraíso | 0.00 |
| Acero Dorado | +50.00 |
| 220x100 cm | +150.00 |

### Opción B: Precio fijo por variante

Ir a cada variante y establecer precio específico.

---

## Verificación Final de Parte 2

### Productos Creados

```
Inventario → Productos → Productos
```

| Producto | Tipo | Rutas | Variantes |
|----------|------|-------|-----------|
| Mesa Comedor Premium | Almacenable | Manufacture + MTO | 12 |
| Base Acero Negro 180x90 | Almacenable | Buy + MTO | - |
| Base Acero Negro 220x100 | Almacenable | Buy + MTO | - |
| Base Acero Dorado 180x90 | Almacenable | Buy + MTO | - |
| Base Acero Dorado 220x100 | Almacenable | Buy + MTO | - |
| Tapa Mármol Carrara 180x90 | Almacenable | Buy + MTO | - |
| Tapa Mármol Carrara 220x100 | Almacenable | Buy + MTO | - |
| Tapa Neolith Negro 180x90 | Almacenable | Buy + MTO | - |
| Tapa Neolith Negro 220x100 | Almacenable | Buy + MTO | - |
| Tapa Madera Sin Terminar 180x90 | Almacenable | Buy + MTO | - |
| Tapa Madera Sin Terminar 220x100 | Almacenable | Buy + MTO | - |
| Tapa Madera Terminada 180x90 | Almacenable | Buy + MTO | 3 |
| Tapa Madera Terminada 220x100 | Almacenable | Buy + MTO | 3 |

### Proveedores Asignados

Verificar en cada componente que tenga proveedor configurado en la pestaña **Compra**.

---

## Resumen de Parte 2

| Ítem | Cantidad |
|------|----------|
| Proveedores | 5 |
| Atributos | 4 |
| Productos componente | 12 |
| Producto final | 1 (con 12 variantes) |
| **Total variantes** | **18** |

---

## Siguiente Paso

Ahora que tenemos los productos, debemos crear las **Listas de Materiales (BoM)** y los **Work Centers**.

➡️ [Parte 3: Manufactura](../parte3/index.md)
