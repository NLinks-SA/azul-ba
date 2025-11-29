# 2. Atributos de Producto

Los atributos permiten crear **variantes** de un mismo producto.

Para nuestra Mesa, necesitamos 3 atributos:
- Material de la Tapa
- Material de la Base
- Medidas

## Acceder a Atributos

```
Inventario → Configuración → Atributos
```

O también:

```
Ventas → Configuración → Atributos del producto
```

---

## 2.1 Crear Atributo: Material Tapa

Click en **Nuevo**

### Datos del Atributo

| Campo | Valor |
|-------|-------|
| **Nombre** | Material Tapa |
| **Tipo de visualización** | Radio (o Pills) |
| **Modo de creación de variantes** | Instantáneamente |

### Valores del Atributo

En la sección **Valores del atributo**, agregar:

| Valor | Es personalizado |
|-------|------------------|
| Mármol Carrara | No |
| Neolith Negro | No |
| Madera Paraíso | No |

**Guardar**

---

## 2.2 Crear Atributo: Material Base

Click en **Nuevo**

### Datos del Atributo

| Campo | Valor |
|-------|-------|
| **Nombre** | Material Base |
| **Tipo de visualización** | Radio |
| **Modo de creación de variantes** | Instantáneamente |

### Valores del Atributo

| Valor | Es personalizado |
|-------|------------------|
| Acero Negro | No |
| Acero Dorado | No |

**Guardar**

---

## 2.3 Crear Atributo: Medidas

Click en **Nuevo**

### Datos del Atributo

| Campo | Valor |
|-------|-------|
| **Nombre** | Medidas |
| **Tipo de visualización** | Select (desplegable) |
| **Modo de creación de variantes** | Instantáneamente |

### Valores del Atributo

| Valor | Es personalizado |
|-------|------------------|
| 180x90 cm | No |
| 220x100 cm | No |

**Guardar**

---

## 2.4 Crear Atributo: Terminación (para Tapas Madera)

Este atributo es solo para las tapas de madera que tienen diferentes terminaciones.

Click en **Nuevo**

### Datos del Atributo

| Campo | Valor |
|-------|-------|
| **Nombre** | Terminación |
| **Tipo de visualización** | Radio |
| **Modo de creación de variantes** | Instantáneamente |

### Valores del Atributo

| Valor | Es personalizado |
|-------|------------------|
| Lustre Mate | No |
| Lustre Brillante | No |
| Natural | No |

**Guardar**

---

## Opciones de Variantes

### Modo de Creación de Variantes

| Modo | Comportamiento |
|------|----------------|
| **Instantáneamente** | Crea todas las variantes al guardar el producto |
| **Dinámicamente** | Crea variantes solo cuando se usan (ej: en una venta) |
| **Nunca** | No crea variantes, solo para personalización |

!!! tip "Recomendación"
    Usar **Instantáneamente** para productos de catálogo fijo.

    Usar **Dinámicamente** si hay muchas combinaciones y no todas se venden.

---

## Verificación

### Lista de Atributos

```
Inventario → Configuración → Atributos
```

| Atributo | Valores | Variantes |
|----------|---------|-----------|
| Material Tapa | 3 (Mármol, Neolith, Madera) | Instantáneamente |
| Material Base | 2 (Negro, Dorado) | Instantáneamente |
| Medidas | 2 (180x90, 220x100) | Instantáneamente |
| Terminación | 3 (Mate, Brillante, Natural) | Instantáneamente |

### Cálculo de Variantes

Para la Mesa:
```
3 (tapas) × 2 (bases) × 2 (medidas) = 12 variantes
```

Para Tapa Madera Terminada (por tamaño):
```
3 terminaciones = 3 variantes por tamaño
```

---

## Resumen

| Atributo | Valores | Uso |
|----------|---------|-----|
| Material Tapa | 3 | Mesa |
| Material Base | 2 | Mesa |
| Medidas | 2 | Mesa, Tapas, Bases |
| Terminación | 3 | Tapa Madera Terminada |
