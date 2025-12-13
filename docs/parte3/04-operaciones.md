# 4. Operaciones y Routings

Las Operaciones definen los pasos de fabricación **internos** y en qué Work Center se realizan.

## ¿Dónde se configuran?

Las operaciones se configuran **dentro de cada BoM**, en la pestaña **Operaciones**.

```
Manufactura → Productos → Listas de materiales → [BoM] → Pestaña Operaciones
```

---

## 4.1 Operaciones para Mesa

Cada BoM de Mesa debe tener estas operaciones:

### Secuencia de Operaciones

| # | Operación | Work Center | Duración | Descripción |
|---|-----------|-------------|----------|-------------|
| 10 | Ensamble Tapa + Base | ENSAM | 60 min | Fijar tapa a base |
| 20 | Control de Calidad Final | QC | 15 min | Verificar ensamble |
| 30 | Embalaje | ENSAM | 30 min | Embalar para entrega |

### Agregar Operación en BoM

1. Abrir una BoM de Mesa
2. Ir a pestaña **Operaciones**
3. Click en **Agregar línea**

#### Campos de la Operación

| Campo | Valor |
|-------|-------|
| **Operación** | Ensamble Tapa + Base |
| **Work Center** | Ensamble Final (ENSAM) |
| **Duración predeterminada** | 60.00 minutos |
| **Secuencia** | 10 |

!!! tip "Secuencia"
    Usar múltiplos de 10 (10, 20, 30...) permite insertar operaciones intermedias después.

---

## 4.2 BoMs de Subcontratación - Sin Operaciones

!!! warning "Las BoMs de subcontratación NO llevan operaciones"
    Los productos fabricados por subcontratistas (Tapa Terminada, Bases, etc.)
    **no tienen operaciones** porque:

    - El subcontratista hace el trabajo, no nosotros
    - No controlamos sus procesos internos
    - La Subcontract MO se completa automáticamente al recibir
    - El QC se hace en el **DSC Picking**, no en operaciones

---

## 4.3 Configuración de Tiempo

### Tipos de Tiempo

En cada operación podés configurar:

| Campo | Descripción |
|-------|-------------|
| **Duración predeterminada** | Tiempo base de la operación |
| **Tiempo de setup** | Preparación antes de empezar |
| **Tiempo de cleanup** | Limpieza después de terminar |

### Modos de Cálculo

| Modo | Descripción |
|------|-------------|
| **Manual** | Tiempo fijo ingresado |
| **Por pieza** | Tiempo × cantidad |
| **Último WO** | Usa el tiempo del último work order similar |

!!! info "Recomendación"
    Para empezar, usar **Manual** con tiempos estimados.
    Odoo aprenderá de los tiempos reales con el tiempo.

---

## 4.4 Consumo de Materiales

Podés configurar en qué operación se consumen los materiales.

### Opciones

| Opción | Descripción |
|--------|-------------|
| **Al inicio** | Al comenzar la primera operación |
| **En operación** | Al comenzar una operación específica |
| **Al final** | Al completar la última operación |

### Configurar en Componente

En la pestaña **Componentes** de la BoM:

| Campo | Descripción |
|-------|-------------|
| **Consumido en operación** | Seleccionar la operación donde se consume |

!!! example "Ejemplo"
    - Tapa: consumir en "Ensamble Tapa + Base"
    - Base: consumir en "Ensamble Tapa + Base"

---

## 4.5 Vista Gantt de Planificación

Con las operaciones configuradas, podés ver la planificación:

```
Manufactura → Planificación → Planificación por Work Center
```

Muestra:
- Operaciones por Work Center
- Fechas programadas
- Carga de trabajo
- Conflictos de capacidad

---

## Verificación

### Ver Operaciones de una BoM de Mesa

```
Manufactura → Productos → Listas de materiales → [Seleccionar BoM de Mesa]
```

Pestaña **Operaciones**:

| Operación | WC | Duración |
|-----------|-----|----------|
| Ensamble Tapa + Base | ENSAM | 60 min |
| Control de Calidad Final | QC | 15 min |
| Embalaje | ENSAM | 30 min |

**Total: ~105 min por mesa**

---

## Resumen

| Tipo BoM | Operaciones | Tiempo total |
|----------|-------------|--------------|
| Mesa | 3 | 105 min |
| Subcontratación | 0 | N/A (proveedor) |

---

## Siguiente Paso

Con las BoMs y operaciones configuradas, pasamos a configurar el **Control de Calidad**.

➡️ [Parte 4: Control de Calidad](../parte4/index.md)
