# 2. Control Points en Manufactura

Configuramos controles de calidad dentro del proceso de fabricación.

## Acceder a Control Points

```
Calidad → Control Points → Nuevo
```

---

## 2.1 Crear: QC Pre-Ensamblado Mesa

Este control se activa antes de comenzar el ensamblado de la mesa.

### Información Principal

| Campo | Valor |
|-------|-------|
| **Título** | Control Pre-Ensamblado Mesa |
| **Referencia** | QC-MFG-ENSAMBLE |

### Alcance

| Campo | Valor |
|-------|-------|
| **Productos** | Mesa Comedor Premium (todas las variantes) |
| **Tipos de operación** | Manufacturing (Fabricación) |

!!! info "Tipo de Operación"
    Seleccionar **Manufacturing** (o Fabricación) para que el control
    se active en órdenes de fabricación, no en recepciones.

### Configuración del Control

| Campo | Valor |
|-------|-------|
| **Tipo de test** | Pass - Fail |
| **Equipo** | Main Quality Team |
| **Control per** | Operation (por operación) |
| **Control Frequency** | All |

### Asociar a Operación (Opcional)

Si querés que el control aparezca en una operación específica:

| Campo | Valor |
|-------|-------|
| **Operación** | Inspección inicial |

!!! note "Sin operación"
    Si no seleccionás operación, el control aparece al inicio del Work Order.

### Instrucciones

```html
<p>Verificar antes de ensamblar:</p>
<ul>
  <li>Todos los componentes presentes y correctos</li>
  <li>Tapa y base son compatibles (mismo tamaño)</li>
  <li>Sin defectos visibles en componentes</li>
  <li>Herrajes y tornillos disponibles</li>
</ul>
<p><strong>No proceder si falta algo o hay defectos.</strong></p>
```

### Mensaje de Falla

```html
<p>No proceder con el ensamblado.</p>
<p>Reportar el problema al supervisor y crear alerta de calidad.</p>
```

**Guardar**

---

## 2.2 Control Point en Work Order Específico (Alternativa)

Otra forma es agregar el Quality Check directamente en la BoM.

### Pasos

1. Ir a **Manufactura → BoMs → [Seleccionar BoM de Mesa]**
2. Pestaña **Operaciones**
3. En la operación deseada, buscar campo **Quality Point**
4. Seleccionar o crear el control point

### Ventaja

El control queda asociado directamente a la operación en esa BoM específica.

---

## 2.3 Tipos de Control en Manufactura

### Pass - Fail

Simple aprobado/rechazado. Ideal para inspecciones visuales.

### Measure (Medición)

Para controles dimensionales:

| Campo | Valor |
|-------|-------|
| **Tipo de test** | Measure |
| **Unidad de medida** | cm |
| **Norma** | 180 |
| **Tolerancia** | 0.5 |

El operador ingresa la medición y el sistema valida si está en rango.

### Take a Picture

Requiere foto del producto:

| Campo | Valor |
|-------|-------|
| **Tipo de test** | Take a Picture |

Útil para evidencia visual de defectos o confirmación de estado.

---

## Verificación

### Lista de Control Points de Manufactura

```
Calidad → Control Points
```

Filtrar por Operación = Manufacturing:

| Referencia | Título | Productos | Operación |
|------------|--------|-----------|-----------|
| QC-MFG-ENSAMBLE | Control Pre-Ensamblado Mesa | 12 variantes | Manufacturing |

---

## Flujo Completo de Quality

Con todos los Control Points configurados:

```
1. RECEPCIÓN DE COMPONENTES
   ├── Recibir Tapa Mármol → QC-REC-MARMOL → Pass/Fail
   ├── Recibir Base → QC-REC-BASE → Pass/Fail
   └── (stock disponible si Pass)

2. FABRICACIÓN
   ├── Crear Work Order
   ├── QC-MFG-ENSAMBLE → Pass/Fail
   ├── Proceder con ensamblado
   └── Completar producción

3. RESULTADO
   └── Mesa lista para entrega
```

---

## Ver Quality Checks Pendientes

```
Calidad → Quality Checks
```

Muestra todos los controles pendientes de completar.

### Filtros Útiles

- **Por hacer**: Checks pendientes
- **Por producto**: Ver checks de un producto específico
- **Por equipo**: Ver checks asignados a un equipo

---

## Quality Alerts

Si un check falla, se puede crear una **Quality Alert**:

```
Calidad → Quality Alerts
```

Las alertas permiten:
- Documentar el problema
- Asignar responsable
- Seguir acciones correctivas
- Cerrar cuando se resuelve

---

## Resumen de Parte 4

| Tipo | Cantidad |
|------|----------|
| Control Points Recepción | 5 |
| Control Points Manufactura | 1 |
| **Total Control Points** | **6** |

---

## Siguiente Paso

Con la configuración completa, vamos a probar el flujo de punta a punta.

➡️ [Parte 5: Flujo Operativo](../parte5/index.md)
