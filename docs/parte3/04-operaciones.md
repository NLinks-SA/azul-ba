# 4. Operaciones y Routings

Las Operaciones definen los pasos de fabricación y en qué Work Center se realizan.

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
| 10 | Inspección inicial | QC | 10 min | Verificar componentes |
| 20 | Preparación de componentes | ENSAM | 15 min | Desembalar y preparar |
| 30 | Ensamble tapa-base | ENSAM | 30 min | Fijar tapa a base |
| 40 | Ajustes y nivelación | ENSAM | 15 min | Nivelar y ajustar |
| 50 | Inspección final | QC | 10 min | Control de calidad final |

### Agregar Operación en BoM

1. Abrir una BoM de Mesa
2. Ir a pestaña **Operaciones**
3. Click en **Agregar línea**

#### Campos de la Operación

| Campo | Valor |
|-------|-------|
| **Operación** | Inspección inicial |
| **Work Center** | Control de Calidad (QC) |
| **Duración predeterminada** | 10.00 minutos |
| **Secuencia** | 10 |

!!! tip "Secuencia"
    Usar múltiplos de 10 (10, 20, 30...) permite insertar operaciones intermedias después.

---

## 4.2 Operaciones para Tapas Terminadas (Subcontratación)

Las BoMs de subcontratación también pueden tener operaciones para planificación.

### Secuencia de Operaciones

| # | Operación | Work Center | Duración | Descripción |
|---|-----------|-------------|----------|-------------|
| 10 | Preparación superficie | LUST | 30 min | Lijado y preparación |
| 20 | Aplicación de lustre | LUST | 60 min | Aplicar terminación |
| 30 | Secado | LUST | 120 min | Tiempo de secado |
| 40 | Pulido final | LUST | 30 min | Pulir y acabar |
| 50 | Control de calidad | QC | 15 min | Inspección |

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
    - Tapa: consumir en "Ensamble tapa-base"
    - Base: consumir en "Ensamble tapa-base"

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

### Ver Operaciones de una BoM

```
Manufactura → Productos → Listas de materiales → [Seleccionar BoM]
```

Pestaña **Operaciones**:

| Operación | WC | Duración |
|-----------|-----|----------|
| Inspección inicial | QC | 10 min |
| Preparación | ENSAM | 15 min |
| Ensamble | ENSAM | 30 min |
| Ajustes | ENSAM | 15 min |
| Inspección final | QC | 10 min |

**Total: ~80 min por mesa**

---

## Resumen

| Tipo BoM | Operaciones | Tiempo total aprox |
|----------|-------------|-------------------|
| Mesa | 5 | 80 min |
| Tapa Terminada | 5 | 255 min |

---

## Siguiente Paso

Con las BoMs y operaciones configuradas, pasamos a configurar el **Control de Calidad**.

➡️ [Parte 4: Control de Calidad](../parte4/index.md)
