# 2. BoM Normal - Mesa

Las Listas de Materiales (BoM) definen qué componentes se necesitan para fabricar un producto.

## Acceder a BoMs

```
Manufactura → Productos → Listas de materiales
```

---

## 2.1 Estrategia de BoMs

Para la Mesa con 12 variantes, tenemos dos opciones:

### Opción A: Una BoM por variante (Recomendada)

- 12 BoMs específicas
- Cada una con sus componentes exactos
- Mayor control

### Opción B: Una BoM genérica con reglas

- 1 BoM con componentes dinámicos
- Más compleja de configurar
- Menos mantenimiento

!!! tip "Recomendación"
    Usar **Opción A** para casos con pocas variantes (< 20).
    Usar **Opción B** para casos con muchas variantes.

En esta guía usamos la **Opción A**.

---

## 2.2 Crear BoM: Mesa (Mármol, Acero Negro, 180x90)

Click en **Nuevo**

### Información Principal

| Campo | Valor |
|-------|-------|
| **Producto** | Mesa Comedor Premium |
| **Variante del producto** | Mármol Carrara, Acero Negro, 180x90 cm |
| **Cantidad** | 1.00 |
| **Tipo de BoM** | Fabricar este producto |

!!! warning "Seleccionar la variante"
    Es importante seleccionar la **variante específica**, no solo el producto.

### Componentes

En la pestaña **Componentes**, agregar:

| Producto | Cantidad |
|----------|----------|
| Tapa Mármol Carrara 180x90 | 1.00 |
| Base Acero Negro 180x90 | 1.00 |

### Operaciones

En la pestaña **Operaciones**, agregar (ver detalle en [Operaciones](04-operaciones.md)):

| Operación | Work Center | Duración |
|-----------|-------------|----------|
| Inspección inicial | QC | 10 min |
| Ensamble de componentes | ENSAM | 30 min |
| Inspección final | QC | 10 min |

**Guardar**

---

## 2.3 Crear BoM: Mesa (Madera, Acero Negro, 180x90)

Esta variante usa la Tapa de Madera Terminada.

### Información Principal

| Campo | Valor |
|-------|-------|
| **Producto** | Mesa Comedor Premium |
| **Variante del producto** | Madera Paraíso, Acero Negro, 180x90 cm |
| **Cantidad** | 1.00 |
| **Tipo de BoM** | Fabricar este producto |

### Componentes

| Producto | Cantidad |
|----------|----------|
| Tapa Madera Terminada 180x90 (Lustre Mate) | 1.00 |
| Base Acero Negro 180x90 | 1.00 |

!!! info "¿Qué terminación usar?"
    En este ejemplo usamos "Lustre Mate" como default.

    En producción real, podrías crear más variantes de mesa
    que mapeen a diferentes terminaciones, o usar una BoM
    genérica con reglas.

### Operaciones

(Las mismas que la anterior)

**Guardar**

---

## 2.4 Crear las BoMs Restantes

Repetir para las 12 variantes:

| Variante Mesa | Componente Tapa | Componente Base |
|---------------|-----------------|-----------------|
| Mármol + Negro + 180x90 | Tapa Mármol 180x90 | Base Negro 180x90 |
| Mármol + Negro + 220x100 | Tapa Mármol 220x100 | Base Negro 220x100 |
| Mármol + Dorado + 180x90 | Tapa Mármol 180x90 | Base Dorado 180x90 |
| Mármol + Dorado + 220x100 | Tapa Mármol 220x100 | Base Dorado 220x100 |
| Neolith + Negro + 180x90 | Tapa Neolith 180x90 | Base Negro 180x90 |
| Neolith + Negro + 220x100 | Tapa Neolith 220x100 | Base Negro 220x100 |
| Neolith + Dorado + 180x90 | Tapa Neolith 180x90 | Base Dorado 180x90 |
| Neolith + Dorado + 220x100 | Tapa Neolith 220x100 | Base Dorado 220x100 |
| Madera + Negro + 180x90 | Tapa Madera Term. 180x90 | Base Negro 180x90 |
| Madera + Negro + 220x100 | Tapa Madera Term. 220x100 | Base Negro 220x100 |
| Madera + Dorado + 180x90 | Tapa Madera Term. 180x90 | Base Dorado 180x90 |
| Madera + Dorado + 220x100 | Tapa Madera Term. 220x100 | Base Dorado 220x100 |

!!! tip "Duplicar BoMs"
    Usar **Acción → Duplicar** y solo cambiar la variante y componentes.

---

## 2.5 Tiempos de Producción

En cada BoM, configurar en la pestaña **Varios**:

| Campo | Valor | Descripción |
|-------|-------|-------------|
| **Tiempo de producción** | 1 día | Tiempo para fabricar |
| **Días para preparar MO** | 2 días | Anticipación para planificar |

Estos tiempos afectan:
- La fecha programada de la MO
- El cálculo de fecha de entrega al cliente

---

## Verificación

### Lista de BoMs

```
Manufactura → Productos → Listas de materiales
```

Filtrar por producto "Mesa Comedor Premium":

| BoM | Variante | Componentes | Tipo |
|-----|----------|-------------|------|
| Mesa/001 | Mármol + Negro + 180x90 | 2 | Fabricar |
| Mesa/002 | Mármol + Negro + 220x100 | 2 | Fabricar |
| ... | ... | ... | ... |

Total: **12 BoMs** para Mesa

---

## Resumen

| Ítem | Cantidad |
|------|----------|
| BoMs de Mesa | 12 |
| Componentes por BoM | 2 |
| Operaciones por BoM | 3 (aprox) |
