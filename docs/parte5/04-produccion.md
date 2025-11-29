# 4. Producción

Con los componentes disponibles, procedemos a fabricar la mesa.

## 4.1 Acceder a la MO

```
Manufactura → Operaciones → Órdenes de fabricación
```

Buscar la MO generada desde la venta.

---

## 4.2 Verificar Disponibilidad

### Estado de Componentes

| Componente | Necesario | Disponible | Estado |
|------------|-----------|------------|--------|
| Tapa Madera Terminada 180x90 (Lustre Mate) | 1 | 1 | ✅ Listo |
| Base Acero Negro 180x90 | 1 | 1 | ✅ Listo |

### Verificar Disponibilidad

Click en **Verificar disponibilidad** si el estado no está actualizado.

!!! success "Listos para Producir"
    Cuando todos los componentes muestran disponibilidad,
    podemos proceder con la fabricación.

---

## 4.3 Confirmar la MO

Si la MO está en estado "Borrador":

1. Click en **Confirmar**
2. El estado cambia a **Confirmada**

---

## 4.4 Planificar Work Orders

### Ver Work Orders

Click en el botón **Work Orders** o ir a la pestaña correspondiente.

Los Work Orders siguen la secuencia de operaciones de la BoM:

| # | Work Order | Work Center | Duración | Estado |
|---|------------|-------------|----------|--------|
| 1 | Inspección inicial | QC | 10 min | Pendiente |
| 2 | Preparación de componentes | ENSAM | 15 min | Pendiente |
| 3 | Ensamble tapa-base | ENSAM | 30 min | Pendiente |
| 4 | Ajustes y nivelación | ENSAM | 15 min | Pendiente |
| 5 | Inspección final | QC | 10 min | Pendiente |

---

## 4.5 Ejecutar Work Orders

### Opción A: Desde la MO

Click en **Planificar** para programar los Work Orders, luego ejecutar cada uno.

### Opción B: Desde Work Center (Tablet)

```
Manufactura → Work Centers → [Seleccionar WC] → Work Orders
```

Esta vista simula una tablet de producción.

---

## 4.6 Work Order 1: Inspección Inicial (QC)

### Iniciar

1. Click en **Iniciar** en el Work Order
2. El estado cambia a "En progreso"
3. Se registra la hora de inicio

### Quality Check de Manufactura

!!! important "Control de Calidad"
    En este Work Order aparece el Quality Check **QC-MFG-ENSAMBLE**
    configurado para manufactura.

1. Aparece el control **Control Pre-Ensamblado Mesa**
2. Verificar según instrucciones:
   - Todos los componentes presentes y correctos
   - Tapa y base son compatibles (mismo tamaño)
   - Sin defectos visibles en componentes
   - Herrajes y tornillos disponibles
3. Seleccionar **Pass**

### Completar

1. Click en **Hecho** o **Siguiente**
2. Se registra tiempo real
3. Avanza al siguiente Work Order

---

## 4.7 Work Orders 2-4: Producción (ENSAM)

### WO2: Preparación de Componentes

1. **Iniciar** el Work Order
2. Desembalar y preparar componentes
3. **Hecho** para completar

### WO3: Ensamble Tapa-Base

1. **Iniciar** el Work Order
2. Fijar la tapa a la base
3. Los componentes se consumen (si está configurado)
4. **Hecho** para completar

### WO4: Ajustes y Nivelación

1. **Iniciar** el Work Order
2. Nivelar y realizar ajustes finales
3. **Hecho** para completar

---

## 4.8 Work Order 5: Inspección Final (QC)

### Iniciar

1. Click en **Iniciar**
2. Realizar inspección visual final

### Completar

1. Verificar que la mesa cumple con las especificaciones
2. Click en **Hecho**

---

## 4.9 Producir Cantidad

### Registrar Producción

Una vez completados todos los Work Orders:

1. En la MO, click en **Producir**
2. Verificar cantidad producida: 1
3. Click en **Validar** o **Marcar como hecho**

### Resultado

- La Mesa se agrega al stock
- Los componentes se consumen
- La MO cambia a estado **Hecho**

---

## 4.10 Ver Trazabilidad

### Desde la MO

La MO completada muestra:
- Componentes consumidos (con lotes si aplica)
- Producto producido
- Tiempos de cada operación
- Quality Checks realizados

### Desde el Producto

```
Inventario → Productos → Mesa Comedor Premium
```

El producto muestra stock disponible.

---

## Verificación

### Estado de la MO

| Campo | Valor |
|-------|-------|
| **Estado** | Hecho ✅ |
| **Cantidad producida** | 1 |
| **Quality Checks** | Todos Pass |

### Stock de Mesa

```
Inventario → Informes → Inventario
```

| Producto | Ubicación | Cantidad |
|----------|-----------|----------|
| Mesa Comedor Premium (Madera/Negro/180x90/Mate) | Stock | 1 |

### Componentes Consumidos

| Componente | Antes | Después |
|------------|-------|---------|
| Tapa Madera Terminada | 1 | 0 |
| Base Acero Negro | 1 | 0 |

---

## 4.11 Entrega al Cliente

### Acceder a la Entrega

```
Inventario → Operaciones → Entregas
```

O desde el SO, click en el smart button **Entrega**.

### Validar Entrega

1. Abrir la orden de entrega
2. Verificar cantidad: 1 Mesa
3. Click en **Validar**

### Resultado

- La Mesa sale del stock
- La entrega se marca como **Hecho**
- El SO se marca como **Entregado**

---

## Flujo Completo

```
┌─────────────────────────────────────────────────────────────┐
│                     PRODUCCIÓN                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   MO Confirmada                                             │
│        │                                                    │
│        ▼                                                    │
│   ┌─────────┐                                               │
│   │Verificar│                                               │
│   │ Disp.   │ → Componentes disponibles ✅                  │
│   └────┬────┘                                               │
│        │                                                    │
│        ▼                                                    │
│   ┌─────────────────────────────────────────────┐          │
│   │           WORK ORDERS                       │          │
│   ├─────────────────────────────────────────────┤          │
│   │                                             │          │
│   │  WO1: Inspección Inicial (QC)              │          │
│   │       └── QC Check: Pass ✅                 │          │
│   │              │                              │          │
│   │              ▼                              │          │
│   │  WO2: Preparación (ENSAM)                  │          │
│   │              │                              │          │
│   │              ▼                              │          │
│   │  WO3: Ensamble (ENSAM)                     │          │
│   │       └── Consumo de componentes           │          │
│   │              │                              │          │
│   │              ▼                              │          │
│   │  WO4: Ajustes (ENSAM)                      │          │
│   │              │                              │          │
│   │              ▼                              │          │
│   │  WO5: Inspección Final (QC)                │          │
│   │                                             │          │
│   └──────────────────────┬──────────────────────┘          │
│                          │                                  │
│                          ▼                                  │
│                    ┌──────────┐                             │
│                    │ Producir │                             │
│                    │  Mesa    │                             │
│                    └────┬─────┘                             │
│                         │                                   │
│                         ▼                                   │
│                    ┌──────────┐                             │
│                    │  Stock   │                             │
│                    │   Mesa   │                             │
│                    └────┬─────┘                             │
│                         │                                   │
│                         ▼                                   │
│                    ┌──────────┐                             │
│                    │ Entrega  │                             │
│                    │ Cliente  │                             │
│                    └──────────┘                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Resumen del Flujo Completo

| Etapa | Documentos | Estado |
|-------|------------|--------|
| 1. Venta | SO | Confirmado → Entregado |
| 2. Compras | 3 POs | Confirmadas → Recibidas |
| 3. Recepciones | 3+ Recepciones | Validadas con QC |
| 4. Manufactura | 1 MO, 5 WOs | Completados con QC |
| 5. Entrega | 1 Delivery | Validada |

### Quality Checks Totales

| Tipo | Cantidad |
|------|----------|
| Recepción (componentes) | 3 |
| Manufactura | 1 |
| **Total** | **4** |

---

## Felicitaciones

Has completado exitosamente el flujo de punta a punta de:

- **MTO (Make to Order)**: Fabricación bajo demanda
- **Subcontratación**: Trabajo con proveedores externos
- **Control de Calidad**: Verificaciones en cada etapa

---

## Siguiente Paso

Consultar los anexos para información adicional.

➡️ [Anexos](../anexos/index.md)
