# 2. BoM Normal - Mesa

Las Listas de Materiales (BoM) definen qué componentes se necesitan para fabricar un producto.

## Acceder a BoMs

```
Manufactura → Productos → Listas de materiales
```

---

## 2.1 Estrategia de BoMs

La Mesa tiene 48 variantes totales (3 materiales × 2 bases × 2 medidas × 4 terminaciones), pero solo **20 combinaciones son válidas**:

| Material Tapa | Terminaciones válidas | Variantes |
|--------------|----------------------|-----------|
| Mármol Carrara | Solo "Sin Terminación" | 4 (2 bases × 2 medidas) |
| Neolith Negro | Solo "Sin Terminación" | 4 (2 bases × 2 medidas) |
| Madera Paraíso | Lustre Mate, Lustre Brillante, Natural | 12 (2 bases × 2 medidas × 3 terminaciones) |
| **Total** | | **20 BoMs** |

Para la Mesa con 20 variantes válidas, tenemos dos opciones:

### Opción A: Una BoM por variante (Recomendada)

- 20 BoMs específicas
- Cada una con sus componentes exactos
- Mayor control y claridad

### Opción B: Una BoM genérica con reglas

- 1 BoM con componentes dinámicos
- Más compleja de configurar
- Menos mantenimiento

!!! tip "Recomendación"
    Usar **Opción A** para casos con pocas variantes (≤ 30).
    Usar **Opción B** para casos con muchas variantes.

En esta guía usamos la **Opción A** con 20 BoMs.

---

## 2.2 Crear BoM: Mesa (Mármol + Sin Terminación + Acero Negro + 180x90)

Click en **Nuevo**

### Información Principal

| Campo | Valor |
|-------|-------|
| **Producto** | Mesa Comedor Premium |
| **Variante del producto** | Mármol Carrara, Sin Terminación, Acero Negro, 180x90 cm |
| **Cantidad** | 1.00 |
| **Tipo de BoM** | Fabricar este producto |

!!! warning "Seleccionar la variante completa"
    Es importante seleccionar la **variante específica** con los 4 atributos:
    - Material Tapa (Mármol Carrara)
    - Terminación (Sin Terminación)
    - Material Base (Acero Negro)
    - Medidas (180x90 cm)

### Componentes

En la pestaña **Componentes**, agregar:

| Producto | Cantidad |
|----------|----------|
| Tapa Mármol Carrara 180x90 | 1.00 |
| Base Acero Negro 180x90 | 1.00 |

### Operaciones

En la pestaña **Operaciones**, agregar (ver detalle en [Operaciones](04-operaciones.md)):

| Secuencia | Operación | Work Center | Duración |
|-----------|-----------|-------------|----------|
| 10 | Inspección inicial | QC | 10 min |
| 20 | Preparación de componentes | ENSAM | 15 min |
| 30 | Ensamble de componentes | ENSAM | 30 min |
| 40 | Ajustes finales | ENSAM | 15 min |
| 50 | Inspección final | QC | 10 min |

**Guardar**

---

## 2.3 Crear BoM: Mesa (Madera + Lustre Mate + Acero Negro + 180x90)

Esta variante usa la Tapa de Madera Terminada con la terminación correspondiente.

### Información Principal

| Campo | Valor |
|-------|-------|
| **Producto** | Mesa Comedor Premium |
| **Variante del producto** | Madera Paraíso, Lustre Mate, Acero Negro, 180x90 cm |
| **Cantidad** | 1.00 |
| **Tipo de BoM** | Fabricar este producto |

### Componentes

| Producto | Cantidad |
|----------|----------|
| Tapa Madera Terminada 180x90 (Lustre Mate) | 1.00 |
| Base Acero Negro 180x90 | 1.00 |

!!! info "Mapeo de Terminación"
    La terminación seleccionada en la Mesa (Lustre Mate, Lustre Brillante, Natural) debe coincidir con la variante de Tapa Madera Terminada:

    | Terminación Mesa | Tapa a usar |
    |-----------------|-------------|
    | Lustre Mate | Tapa Madera Terminada (Lustre Mate) |
    | Lustre Brillante | Tapa Madera Terminada (Lustre Brillante) |
    | Natural | Tapa Madera Terminada (Natural) |

### Operaciones

Las mismas 5 operaciones que la variante anterior (ver sección 2.2).

**Guardar**

---

## 2.4 Crear las BoMs Restantes

Repetir para las 20 variantes válidas. Usar **Acción → Duplicar** para acelerar.

### Variantes Mármol/Neolith (8 BoMs)

Estas usan "Sin Terminación" y tapas simples:

| # | Material Tapa | Terminación | Base | Medidas | Componente Tapa | Componente Base |
|---|--------------|-------------|------|---------|-----------------|-----------------|
| 1 | Mármol Carrara | Sin Terminación | Acero Negro | 180x90 | Tapa Mármol Carrara 180x90 | Base Acero Negro 180x90 |
| 2 | Mármol Carrara | Sin Terminación | Acero Negro | 220x100 | Tapa Mármol Carrara 220x100 | Base Acero Negro 220x100 |
| 3 | Mármol Carrara | Sin Terminación | Acero Dorado | 180x90 | Tapa Mármol Carrara 180x90 | Base Acero Dorado 180x90 |
| 4 | Mármol Carrara | Sin Terminación | Acero Dorado | 220x100 | Tapa Mármol Carrara 220x100 | Base Acero Dorado 220x100 |
| 5 | Neolith Negro | Sin Terminación | Acero Negro | 180x90 | Tapa Neolith Negro 180x90 | Base Acero Negro 180x90 |
| 6 | Neolith Negro | Sin Terminación | Acero Negro | 220x100 | Tapa Neolith Negro 220x100 | Base Acero Negro 220x100 |
| 7 | Neolith Negro | Sin Terminación | Acero Dorado | 180x90 | Tapa Neolith Negro 180x90 | Base Acero Dorado 180x90 |
| 8 | Neolith Negro | Sin Terminación | Acero Dorado | 220x100 | Tapa Neolith Negro 220x100 | Base Acero Dorado 220x100 |

### Variantes Madera (12 BoMs)

Estas usan terminaciones de lustre y tapas terminadas:

| # | Material Tapa | Terminación | Base | Medidas | Componente Tapa | Componente Base |
|---|--------------|-------------|------|---------|-----------------|-----------------|
| 9 | Madera Paraíso | Lustre Mate | Acero Negro | 180x90 | Tapa Madera Terminada 180x90 (Lustre Mate) | Base Acero Negro 180x90 |
| 10 | Madera Paraíso | Lustre Mate | Acero Negro | 220x100 | Tapa Madera Terminada 220x100 (Lustre Mate) | Base Acero Negro 220x100 |
| 11 | Madera Paraíso | Lustre Mate | Acero Dorado | 180x90 | Tapa Madera Terminada 180x90 (Lustre Mate) | Base Acero Dorado 180x90 |
| 12 | Madera Paraíso | Lustre Mate | Acero Dorado | 220x100 | Tapa Madera Terminada 220x100 (Lustre Mate) | Base Acero Dorado 220x100 |
| 13 | Madera Paraíso | Lustre Brillante | Acero Negro | 180x90 | Tapa Madera Terminada 180x90 (Lustre Brillante) | Base Acero Negro 180x90 |
| 14 | Madera Paraíso | Lustre Brillante | Acero Negro | 220x100 | Tapa Madera Terminada 220x100 (Lustre Brillante) | Base Acero Negro 220x100 |
| 15 | Madera Paraíso | Lustre Brillante | Acero Dorado | 180x90 | Tapa Madera Terminada 180x90 (Lustre Brillante) | Base Acero Dorado 180x90 |
| 16 | Madera Paraíso | Lustre Brillante | Acero Dorado | 220x100 | Tapa Madera Terminada 220x100 (Lustre Brillante) | Base Acero Dorado 220x100 |
| 17 | Madera Paraíso | Natural | Acero Negro | 180x90 | Tapa Madera Terminada 180x90 (Natural) | Base Acero Negro 180x90 |
| 18 | Madera Paraíso | Natural | Acero Negro | 220x100 | Tapa Madera Terminada 220x100 (Natural) | Base Acero Negro 220x100 |
| 19 | Madera Paraíso | Natural | Acero Dorado | 180x90 | Tapa Madera Terminada 180x90 (Natural) | Base Acero Dorado 180x90 |
| 20 | Madera Paraíso | Natural | Acero Dorado | 220x100 | Tapa Madera Terminada 220x100 (Natural) | Base Acero Dorado 220x100 |

!!! tip "Proceso eficiente"
    1. Crear la primera BoM completamente (variante + componentes + operaciones)
    2. Usar **Acción → Duplicar**
    3. Cambiar solo: variante del producto y componentes según la tabla

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

| # | Variante | Componentes | Tipo |
|---|----------|-------------|------|
| 1-4 | Mármol Carrara + Sin Terminación + (varias bases/medidas) | 2 | Fabricar |
| 5-8 | Neolith Negro + Sin Terminación + (varias bases/medidas) | 2 | Fabricar |
| 9-12 | Madera Paraíso + Lustre Mate + (varias bases/medidas) | 2 | Fabricar |
| 13-16 | Madera Paraíso + Lustre Brillante + (varias bases/medidas) | 2 | Fabricar |
| 17-20 | Madera Paraíso + Natural + (varias bases/medidas) | 2 | Fabricar |

Total: **20 BoMs** para Mesa

### Verificar Operaciones

Cada BoM debe tener las mismas 5 operaciones:

| Secuencia | Operación | Work Center | Duración |
|-----------|-----------|-------------|----------|
| 10 | Inspección inicial | QC | 10 min |
| 20 | Preparación de componentes | ENSAM | 15 min |
| 30 | Ensamble de componentes | ENSAM | 30 min |
| 40 | Ajustes finales | ENSAM | 15 min |
| 50 | Inspección final | QC | 10 min |

---

## Resumen

| Ítem | Cantidad |
|------|----------|
| BoMs de Mesa | 20 |
| Componentes por BoM | 2 (1 tapa + 1 base) |
| Operaciones por BoM | 5 |
| Tiempo total operaciones | ~80 minutos |
| Tiempo de producción | 1 día |
| Días para preparar MO | 2 días |
