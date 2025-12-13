# 1. Control de Calidad en Dropship Subcontractor

Configuramos control de calidad automático para cuando se valida el picking DSC (Dropship Subcontractor).

## ¿Cuándo se dispara el QC?

El control de calidad se activa al validar el picking **DSC** (Dropship Subcontractor), que es cuando la Tapa Madera Sin Terminar llega de Carpintería al Lustrador.

```
PO Carpintería → DSC Picking (aquí se hace QC) → Lustrador
```

## Acceder a Control Points

```
Calidad → Control Points → Nuevo
```

---

## 1.1 Crear: QC - Recepción Tapa Madera (DSC)

Este control se activa al validar el picking DSC con tapas de madera sin terminar.

### Información Principal

| Campo | Valor |
|-------|-------|
| **Nombre** | QC - Recepción Tapa Madera (DSC) |
| **Título** | Control de Calidad - Tapa Madera Sin Terminar |

### Alcance

| Campo | Valor |
|-------|-------|
| **Productos** | Tapa Madera Sin Terminar 180x90, Tapa Madera Sin Terminar 220x100 |
| **Tipos de operación** | Dropship Subcontractor (DSC) |

!!! info "Tipo de Operación DSC"
    Seleccionar el tipo de operación **Dropship Subcontractor** (código DSC).

    Este picking type se crea automáticamente al instalar el módulo
    `mrp_subcontracting_dropshipping`.

### Configuración del Control

| Campo | Valor |
|-------|-------|
| **Tipo de test** | Pass - Fail |
| **Equipo** | Main Quality Team |
| **Control per** | Product (por producto) |
| **Control Frequency** | All (todos) |

### Instrucciones

En el campo **Nota** o **Instructions**:

```html
<p><strong>Control de calidad al recibir Tapa Madera en el Lustrador:</strong></p>
<p>Verificar la tapa de madera SIN terminar antes de aceptar el envío.</p>
<ul>
    <li>Dimensiones correctas (180x90 o 220x100)</li>
    <li>Calidad de la madera (sin nudos, grietas)</li>
    <li>Humedad adecuada (&lt;12%)</li>
    <li>Sin defectos visibles</li>
    <li>Corte y cepillado correctos</li>
</ul>
<p><strong>Si NO pasa el QC, rechazar el envío.</strong></p>
```

**Guardar**

---

## Verificación

### Lista de Control Points

```
Calidad → Control Points
```

| Nombre | Productos | Operación |
|--------|-----------|-----------|
| QC - Recepción Tapa Madera (DSC) | 2 | Dropship Subcontractor |

---

## Cómo Funciona

Cuando se valida un picking DSC con Tapa Madera Sin Terminar:

1. Usuario va a **Inventario → Operaciones → Dropship Subcontractor**
2. Abre el picking pendiente (ej: `ptest-scripting/DSC/00001`)
3. Antes de validar, aparece **Quality Check** pendiente
4. Click en el check → Completa Pass/Fail
5. Si **Pass** → Puede validar el picking, material llega al Lustrador
6. Si **Fail** → Se crea Quality Alert, el envío se rechaza

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Carpintería   │────▶│  DSC Picking    │────▶│   Lustrador     │
│                 │     │   + QC Check    │     │                 │
│   Tapa Madera   │     │   Pass/Fail     │     │   (produce)     │
│   Sin Terminar  │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## Flujo Completo con QC

```
1. SO Mesa Madera
      │
      ▼
2. MO Mesa (MTO)
      │
      ▼
3. PO Lustrador (subcontratación)
      │
      ▼ (confirmar PO)
4. Subcontract MO
      │
      ▼ (necesita Tapa Sin Terminar - ruta Dropship)
5. PO Carpintería
      │
      ▼ (confirmar PO)
6. DSC Picking + QC ◄── Control de Calidad aquí
      │
      ▼ (si Pass)
7. Tapa llega a Lustrador
      │
      ▼
8. Lustrador produce Tapa Terminada
      │
      ▼
9. MO Mesa puede continuar
```

---

## Resumen

| Control Points | 1 |
|----------------|---|
| Productos cubiertos | 2 (Tapas Sin Terminar) |
| Tipo de operación | Dropship Subcontractor (DSC) |
