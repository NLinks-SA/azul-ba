# 3. Recepciones con Control de Calidad

Procesamos las recepciones de componentes, completando los controles de calidad configurados.

## 3.1 Acceder a Recepciones

```
Inventario → Operaciones → Recepciones
```

Ver recepciones pendientes (estado "Preparado" o "Por hacer").

---

## 3.2 Recepción de Tapa Sin Terminar (Carpintería)

### Abrir la Recepción

Buscar la recepción del proveedor **Carpintería Hnos. García**.

### Quality Check Pendiente

Al abrir, debería aparecer un indicador de **Quality Check pendiente**.

| Indicador | Significado |
|-----------|-------------|
| 🔴 Quality Check | Hay controles pendientes |
| Botón "Quality Checks" | Ver/completar controles |

### Completar el Control

1. Click en **Quality Checks** o en el indicador
2. Se abre el control **QC-REC-TAPA-CRUDA**
3. Verificar instrucciones:
   - Dimensiones correctas
   - Sin grietas ni nudos excesivos
   - Humedad de la madera en rango
   - Sin manchas ni decoloraciones
4. Seleccionar **Pass** o **Fail**

### Si Pass

- El check se marca como completado ✅
- Podés validar la recepción

### Si Fail

- Se crea una **Quality Alert**
- Debés decidir: rechazar, aceptar con descuento, etc.

### Validar Recepción

1. Verificar cantidad recibida
2. Click en **Validar**
3. La Tapa Sin Terminar entra al stock

---

## 3.3 Recepción de Base (Metalúrgica)

### Abrir la Recepción

Buscar la recepción del proveedor **Metalúrgica Precisión S.A.**

### Completar Control QC-REC-BASE

Verificar según instrucciones:
- Soldaduras completas y limpias
- Pintura sin descascarado
- Color correcto (Negro)
- Nivelación correcta
- Dimensiones correctas

**Pass** → Validar recepción

---

## 3.4 Flujo de Subcontratación (Lustrador)

Este es el flujo más complejo porque involucra envío de componentes.

### Paso 1: Verificar Stock de Componente

Antes de procesar, verificar que la Tapa Sin Terminar está en stock:

```
Inventario → Productos → Tapa Madera Sin Terminar 180x90
```

Debería mostrar stock > 0 después de la recepción de Carpintería.

### Paso 2: Ver la PO del Lustrador

```
Compras → Pedidos → PO al Lustrador
```

Verificar que tiene:
- Producto: Tapa Madera Terminada
- Estado: Orden de compra

### Paso 3: Envío al Subcontratista (si aplica)

Si el sistema generó un movimiento de envío:

```
Inventario → Operaciones → Entregas
```

Buscar entrega a la **ubicación del subcontratista** (Lustrador).

1. Abrir la entrega
2. Validar el envío de la Tapa Sin Terminar

!!! info "Ubicación Subcontratista"
    La Tapa Sin Terminar se mueve a la ubicación del Lustrador
    (creada en la configuración inicial).

### Paso 4: Recibir Tapa Terminada

```
Inventario → Operaciones → Recepciones
```

Buscar recepción del **Lustrador**.

### Completar Control QC-REC-TAPA-LUSTRADA

Verificar según instrucciones:
- Acabado uniforme sin burbujas
- Brillo correcto (Mate)
- Sin rayaduras ni golpes
- Bordes bien terminados

**Pass** → Validar recepción

### Resultado

- La Tapa Terminada entra al stock
- La Tapa Sin Terminar se consume automáticamente

---

## 3.5 Ver Quality Checks Completados

### Lista de Checks

```
Calidad → Quality Checks
```

Filtrar por estado "Hecho":

| Check | Producto | Resultado |
|-------|----------|-----------|
| QC-REC-TAPA-CRUDA | Tapa Sin Terminar 180x90 | Pass ✅ |
| QC-REC-BASE | Base Acero Negro 180x90 | Pass ✅ |
| QC-REC-TAPA-LUSTRADA | Tapa Terminada 180x90 | Pass ✅ |

---

## 3.6 Ver Quality Alerts (si hubo fallas)

```
Calidad → Quality Alerts
```

Si algún check falló, aparecerá una alerta para gestionar:
- Asignar responsable
- Documentar el problema
- Definir acciones correctivas
- Cerrar cuando se resuelve

---

## Verificación

### Stock de Componentes

```
Inventario → Informes → Inventario
```

| Producto | Ubicación | Cantidad |
|----------|-----------|----------|
| Tapa Madera Terminada 180x90 (Lustre Mate) | Stock | 1 |
| Base Acero Negro 180x90 | Stock | 1 |

### Estado de la MO

La MO debería mostrar componentes **disponibles** ahora:

| Componente | Disponible |
|------------|------------|
| Tapa Madera Terminada | 1 ✅ |
| Base Acero Negro | 1 ✅ |

---

## Flujo Visual

```
┌─────────────────────────────────────────────────────────────┐
│                    RECEPCIONES                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Carpintería          Metalúrgica         Lustrador         │
│      │                    │                   │             │
│      ▼                    ▼                   │             │
│  ┌───────┐           ┌───────┐               │             │
│  │Recibir│           │Recibir│               │             │
│  │Tapa ST│           │ Base  │               │             │
│  └───┬───┘           └───┬───┘               │             │
│      │                   │                   │             │
│      ▼                   ▼                   │             │
│  ┌───────┐           ┌───────┐               │             │
│  │QC Pass│           │QC Pass│               │             │
│  └───┬───┘           └───┬───┘               │             │
│      │                   │                   │             │
│      ▼                   ▼                   ▼             │
│  ┌───────┐           ┌───────┐        ┌───────────┐       │
│  │ Stock │           │ Stock │        │Enviar Tapa│       │
│  │Tapa ST│           │ Base  │        │ST a Lust. │       │
│  └───┬───┘           └───────┘        └─────┬─────┘       │
│      │                                      │             │
│      └──────────────────────────────────────┘             │
│                         │                                  │
│                         ▼                                  │
│                   ┌───────────┐                            │
│                   │  Recibir  │                            │
│                   │Tapa Term. │                            │
│                   └─────┬─────┘                            │
│                         │                                  │
│                         ▼                                  │
│                   ┌───────────┐                            │
│                   │  QC Pass  │                            │
│                   └─────┬─────┘                            │
│                         │                                  │
│                         ▼                                  │
│                   ┌───────────┐                            │
│                   │   Stock   │                            │
│                   │ Tapa Term │                            │
│                   └───────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Siguiente Paso

Con todos los componentes en stock, proceder a la producción.

➡️ [Producción](04-produccion.md)
