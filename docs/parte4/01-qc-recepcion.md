# 1. Control Points en Recepción

Configuramos controles de calidad automáticos para cuando recibimos productos de proveedores.

## Acceder a Control Points

```
Calidad → Control Points → Nuevo
```

---

## 1.1 Crear: QC Recepción Tapas Sin Terminar

Este control se activa al recibir tapas de madera de la Carpintería.

### Información Principal

| Campo | Valor |
|-------|-------|
| **Título** | Control Recepción Tapas Sin Terminar |
| **Referencia** | QC-REC-TAPA-CRUDA |

### Alcance

| Campo | Valor |
|-------|-------|
| **Productos** | Tapa Madera Sin Terminar 180x90, Tapa Madera Sin Terminar 220x100 |
| **Categorías de producto** | (dejar vacío si seleccionaste productos) |
| **Tipos de operación** | Recepciones (Receipts) |

!!! info "Tipos de Operación"
    Seleccionar el tipo de operación **Recepciones** (o Receipts).

    Esto hace que el control se active SOLO en recepciones,
    no en otros movimientos internos.

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
<p>Verificar:</p>
<ul>
  <li>Dimensiones correctas según orden</li>
  <li>Sin grietas ni nudos excesivos</li>
  <li>Humedad de la madera dentro de rango</li>
  <li>Sin manchas ni decoloraciones</li>
</ul>
```

### Mensaje de Falla

En **Failure Message**:

```html
<p>Rechazar lote y notificar a Carpintería Hnos. García</p>
```

**Guardar**

---

## 1.2 Crear: QC Recepción Tapas Lustradas

Control para tapas terminadas que vienen del Lustrador.

### Información Principal

| Campo | Valor |
|-------|-------|
| **Título** | Control Recepción Tapas Lustradas |
| **Referencia** | QC-REC-TAPA-LUSTRADA |

### Alcance

| Campo | Valor |
|-------|-------|
| **Productos** | Todas las variantes de Tapa Madera Terminada |
| **Tipos de operación** | Recepciones |

### Configuración

| Campo | Valor |
|-------|-------|
| **Tipo de test** | Pass - Fail |
| **Control per** | Product |
| **Control Frequency** | All |

### Instrucciones

```html
<p>Verificar:</p>
<ul>
  <li>Acabado uniforme sin burbujas ni marcas</li>
  <li>Brillo según especificación (Mate/Brillante/Natural)</li>
  <li>Sin rayaduras ni golpes</li>
  <li>Bordes bien terminados</li>
</ul>
```

**Guardar**

---

## 1.3 Crear: QC Recepción Bases Metálicas

### Información Principal

| Campo | Valor |
|-------|-------|
| **Título** | Control Recepción Bases Metálicas |
| **Referencia** | QC-REC-BASE |

### Alcance

| Campo | Valor |
|-------|-------|
| **Productos** | Todas las Bases Acero (4 productos) |
| **Tipos de operación** | Recepciones |

### Instrucciones

```html
<p>Verificar:</p>
<ul>
  <li>Soldaduras completas y limpias</li>
  <li>Pintura sin descascarado ni burbujas</li>
  <li>Color correcto (Negro/Dorado)</li>
  <li>Nivelación correcta (no balancea)</li>
  <li>Dimensiones según especificación</li>
</ul>
```

**Guardar**

---

## 1.4 Crear: QC Recepción Mármol

### Información Principal

| Campo | Valor |
|-------|-------|
| **Título** | Control Recepción Tapas Mármol |
| **Referencia** | QC-REC-MARMOL |

### Alcance

| Campo | Valor |
|-------|-------|
| **Productos** | Tapa Mármol Carrara 180x90, Tapa Mármol Carrara 220x100 |
| **Tipos de operación** | Recepciones |

### Instrucciones

```html
<p>Verificar:</p>
<ul>
  <li>Sin fisuras ni grietas</li>
  <li>Pulido uniforme</li>
  <li>Veteado según muestra aprobada</li>
  <li>Bordes bien terminados</li>
  <li>Espesor correcto</li>
</ul>
```

**Guardar**

---

## 1.5 Crear: QC Recepción Neolith

### Información Principal

| Campo | Valor |
|-------|-------|
| **Título** | Control Recepción Tapas Neolith |
| **Referencia** | QC-REC-NEOLITH |

### Alcance

| Campo | Valor |
|-------|-------|
| **Productos** | Tapa Neolith Negro 180x90, Tapa Neolith Negro 220x100 |
| **Tipos de operación** | Recepciones |

### Instrucciones

```html
<p>Verificar:</p>
<ul>
  <li>Espesor uniforme</li>
  <li>Bordes sin astillado</li>
  <li>Color negro uniforme</li>
  <li>Superficie sin defectos</li>
</ul>
```

**Guardar**

---

## Verificación

### Lista de Control Points

```
Calidad → Control Points
```

| Referencia | Título | Productos | Operación |
|------------|--------|-----------|-----------|
| QC-REC-TAPA-CRUDA | Control Recepción Tapas Sin Terminar | 2 | Recepciones |
| QC-REC-TAPA-LUSTRADA | Control Recepción Tapas Lustradas | 6 | Recepciones |
| QC-REC-BASE | Control Recepción Bases Metálicas | 4 | Recepciones |
| QC-REC-MARMOL | Control Recepción Tapas Mármol | 2 | Recepciones |
| QC-REC-NEOLITH | Control Recepción Tapas Neolith | 2 | Recepciones |

---

## Cómo Funciona

Cuando llegue una recepción:

1. Usuario va a **Inventario → Recepciones**
2. Abre la recepción pendiente
3. Antes de validar, aparece **Quality Check** pendiente
4. Click en el check → Completa Pass/Fail
5. Si Pass → Puede validar recepción
6. Si Fail → Se crea Quality Alert

---

## Resumen

| Control Points de Recepción | 5 |
|---------------------------|---|
| Productos cubiertos | 16 |
