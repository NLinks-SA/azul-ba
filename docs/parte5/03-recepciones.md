# 3. Recepciones y Dropship Subcontractor

Procesamos las recepciones de componentes y el DSC Picking con control de calidad.

## Flujo General

```
                    ┌─────────────────┐
                    │   RECEPCIONES   │
                    └────────┬────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       │                     │                     │
       ▼                     ▼                     ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  Recepción  │       │     DSC     │       │  Recepción  │
│    Base     │       │   Picking   │       │Tapa Termin. │
│ (Metalúrg.) │       │  (+ QC)     │       │ (Lustrador) │
└─────────────┘       └─────────────┘       └─────────────┘
```

!!! info "Orden de Procesamiento"
    1. **Recepción Base** (Metalúrgica) - Sin QC configurado
    2. **DSC Picking** (Carpintería → Lustrador) - **Con QC**
    3. **Recepción Tapa Terminada** (Lustrador) - Después que termine de producir

---

## 3.1 Recepción de Base (Metalúrgica)

### Acceder a Recepciones

```
Inventario → Operaciones → Recepciones
```

### Procesar Recepción

1. Buscar recepción de **Metalúrgica Precisión S.A.**
2. Verificar producto: Base Acero Negro 180x90
3. Click en **Validar**
4. La Base entra al stock

---

## 3.2 DSC Picking - Dropship Subcontractor (con QC)

Este es el movimiento clave del flujo: Carpintería envía la Tapa Sin Terminar **directamente** al Lustrador.

### Acceder al DSC Picking

```
Inventario → Operaciones → Dropship Subcontractor
```

O buscar pickings con código **DSC**.

### Identificar el Picking

| Campo | Valor |
|-------|-------|
| **Referencia** | xxx/DSC/00001 |
| **Tipo** | Dropship Subcontractor |
| **Producto** | Tapa Madera Sin Terminar 180x90 |
| **Desde** | Partners/Vendors |
| **Hacia** | Subcontract - Lustres & Acabados |
| **Quality Check** | 🔴 1 Pendiente |

### Quality Check en DSC

!!! warning "Control de Calidad Obligatorio"
    El DSC Picking tiene configurado un **Quality Point** que requiere
    verificar la Tapa Sin Terminar antes de que llegue al Lustrador.

    Esto es crítico porque si la madera tiene defectos, el Lustrador
    no podrá producir una Tapa Terminada de calidad.

#### Completar el Control de Calidad

1. Abrir el DSC Picking
2. Ver indicador **Quality Checks** (🔴 1)
3. Click en **Quality Checks**
4. Se abre el control: **QC - Recepción Tapa Madera (DSC)**

#### Verificaciones a Realizar

| Verificación | Criterio |
|--------------|----------|
| Dimensiones | 180x90 o 220x100 correctas |
| Calidad madera | Sin nudos, grietas ni manchas |
| Humedad | < 12% |
| Corte | Cepillado correcto |
| Defectos | Sin defectos visibles |

#### Resultado del Control

**Si PASS:**
- El check se marca completado ✅
- Podés validar el DSC Picking
- La Tapa Sin Terminar llega al Lustrador

**Si FAIL:**
- Se crea una **Quality Alert**
- El envío se rechaza
- Debe gestionarse con Carpintería

### Validar el DSC Picking

1. Después de completar el QC con Pass
2. Click en **Validar**
3. El movimiento se completa

### Resultado

```
ANTES del DSC Picking:
├── Partners/Vendors: Tapa Sin Terminar (virtual)
└── Subcontract - Lustrador: 0

DESPUÉS del DSC Picking:
├── Partners/Vendors: 0
└── Subcontract - Lustrador: Tapa Sin Terminar ✅
```

!!! info "¿Por qué es importante?"
    Una vez validado el DSC Picking:
    - El Lustrador tiene la materia prima
    - La Subcontract MO puede producirse
    - Cuando el Lustrador termina, nos envía la Tapa Terminada

---

## 3.3 Recepción de Tapa Terminada (Lustrador)

Después que el Lustrador produce la Tapa Terminada, la recibimos.

### Acceder a la Recepción

```
Inventario → Operaciones → Recepciones
```

Buscar recepción de **Lustres & Acabados Premium**.

### Procesar Recepción

1. Abrir la recepción
2. Verificar producto: Tapa Madera Terminada 180x90 (Lustre Mate)
3. Click en **Validar**

### Resultado

- La Tapa Terminada entra al stock
- La Tapa Sin Terminar se consume automáticamente (estaba en ubicación del Lustrador)
- La Subcontract MO se completa

---

## 3.4 Verificar Quality Checks Completados

```
Calidad → Quality Checks
```

Filtrar por estado "Hecho":

| Check | Producto | Operación | Resultado |
|-------|----------|-----------|-----------|
| QC - Recepción Tapa Madera (DSC) | Tapa Sin Terminar 180x90 | DSC | Pass ✅ |

---

## 3.5 Ver Quality Alerts (si hubo fallas)

```
Calidad → Quality Alerts
```

Si el QC falló, aparecerá una alerta para gestionar:
- Asignar responsable
- Documentar el problema
- Definir acciones correctivas
- Cerrar cuando se resuelve

---

## Verificación Final

### Stock de Componentes

```
Inventario → Informes → Inventario
```

| Producto | Ubicación | Cantidad |
|----------|-----------|----------|
| Tapa Madera Terminada 180x90 (Lustre Mate) | WH/Stock | 1 |
| Base Acero Negro 180x90 | WH/Stock | 1 |
| Tapa Madera Sin Terminar 180x90 | Subcontract - Lustrador | 0 (consumida) |

### Estado de la MO

La MO principal (Mesa) debería mostrar componentes **disponibles**:

| Componente | Disponible |
|------------|------------|
| Tapa Madera Terminada | 1 ✅ |
| Base Acero Negro | 1 ✅ |

---

## Flujo Visual Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                     FLUJO DE RECEPCIONES                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Metalúrgica                    Carpintería → Lustrador         │
│      │                                │                         │
│      ▼                                ▼                         │
│  ┌───────┐                      ┌───────────┐                   │
│  │Recibir│                      │    DSC    │                   │
│  │ Base  │                      │  Picking  │                   │
│  └───┬───┘                      └─────┬─────┘                   │
│      │                                │                         │
│      │                                ▼                         │
│      │                          ┌───────────┐                   │
│      │                          │  QC Pass  │ ← Control Calidad │
│      │                          └─────┬─────┘                   │
│      │                                │                         │
│      ▼                                ▼                         │
│  ┌───────┐                      ┌───────────┐                   │
│  │ Stock │                      │ Lustrador │                   │
│  │ Base  │                      │  produce  │                   │
│  └───────┘                      └─────┬─────┘                   │
│                                       │                         │
│                                       ▼                         │
│                                 ┌───────────┐                   │
│                                 │  Recibir  │                   │
│                                 │Tapa Term. │                   │
│                                 └─────┬─────┘                   │
│                                       │                         │
│                                       ▼                         │
│                                 ┌───────────┐                   │
│                                 │   Stock   │                   │
│                                 │ Tapa Term │                   │
│                                 └───────────┘                   │
│                                                                 │
│                    ┌─────────────────────────┐                  │
│                    │  MO Mesa puede producir │                  │
│                    │  (componentes listos)   │                  │
│                    └─────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Resumen del Flujo Dropship Subcontractor

| Paso | Operación | Resultado |
|------|-----------|-----------|
| 1 | Confirmar PO Lustrador | Crea Subcontract MO |
| 2 | Subcontract MO detecta componente Dropship | Crea PO Carpintería |
| 3 | PO Carpintería genera | DSC Picking |
| 4 | Validar DSC Picking (con QC) | Tapa Sin Terminar llega a Lustrador |
| 5 | Lustrador produce | Tapa Terminada |
| 6 | Recibir de Lustrador | Tapa Terminada en Stock |

---

## Siguiente Paso

Con todos los componentes en stock, proceder a la producción de la Mesa.

➡️ [Producción](04-produccion.md)
