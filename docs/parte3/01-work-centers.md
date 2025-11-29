# 1. Work Centers

Los Work Centers (Centros de Trabajo) representan estaciones donde se realizan operaciones de fabricación.

## Acceder a Work Centers

```
Manufactura → Configuración → Work Centers
```

---

## 1.1 Work Centers a Crear

Necesitamos estos centros de trabajo:

| Work Center | Código | Uso |
|-------------|--------|-----|
| Carpintería Externa | CARP | Referencia al proveedor |
| Lustrado y Acabados | LUST | Referencia al proveedor |
| Marmolería Externa | MARM | Referencia al proveedor |
| Metalurgia Externa | META | Referencia al proveedor |
| Ensamble Final | ENSAM | Interno - donde se ensambla la mesa |
| Control de Calidad | QC | Interno - inspección |

!!! info "¿Por qué Work Centers para proveedores externos?"
    Aunque son externos, los Work Centers permiten:

    - Planificar tiempos de producción
    - Ver todo en el Gantt
    - Calcular fechas de entrega
    - Costear operaciones

---

## 1.2 Crear Work Center: Ensamble Final

Click en **Nuevo**

### Pestaña: Información General

| Campo | Valor |
|-------|-------|
| **Nombre** | Ensamble Final |
| **Código** | ENSAM |
| **Tiempo antes de producción** | 0.00 |
| **Tiempo después de producción** | 0.00 |

### Pestaña: Capacidad

| Campo | Valor |
|-------|-------|
| **Capacidad** | 2 |
| **Eficiencia del tiempo** | 100% |

!!! info "Capacidad"
    Indica cuántas operaciones simultáneas puede manejar.
    Capacidad 2 = puede ensamblar 2 mesas a la vez.

### Pestaña: Costes

| Campo | Valor |
|-------|-------|
| **Coste por hora** | 50.00 |

**Guardar**

---

## 1.3 Crear Work Center: Control de Calidad

| Campo | Valor |
|-------|-------|
| **Nombre** | Control de Calidad |
| **Código** | QC |
| **Capacidad** | 5 |
| **Coste por hora** | 30.00 |

**Guardar**

---

## 1.4 Crear Work Centers Externos

Para los proveedores externos, crear Work Centers de referencia:

### Carpintería Externa

| Campo | Valor |
|-------|-------|
| **Nombre** | Carpintería Externa |
| **Código** | CARP |
| **Capacidad** | 10 |
| **Coste por hora** | 0.00 (el costo está en la PO) |

### Lustrado y Acabados

| Campo | Valor |
|-------|-------|
| **Nombre** | Lustrado y Acabados |
| **Código** | LUST |
| **Capacidad** | 10 |
| **Coste por hora** | 0.00 |

### Marmolería Externa

| Campo | Valor |
|-------|-------|
| **Nombre** | Marmolería Externa |
| **Código** | MARM |
| **Capacidad** | 5 |
| **Coste por hora** | 0.00 |

### Metalurgia Externa

| Campo | Valor |
|-------|-------|
| **Nombre** | Metalurgia Externa |
| **Código** | META |
| **Capacidad** | 10 |
| **Coste por hora** | 0.00 |

---

## 1.5 Configurar Capacidades Específicas (Opcional)

Si un Work Center tiene capacidad diferente por producto:

```
Manufactura → Configuración → Work Centers → [Seleccionar WC] → Capacidades
```

| Producto | Capacidad | Unidad de tiempo |
|----------|-----------|------------------|
| Mesa Comedor Premium | 2 | Por día |

---

## Verificación

### Lista de Work Centers

```
Manufactura → Configuración → Work Centers
```

| Work Center | Código | Capacidad | Costo/hora |
|-------------|--------|-----------|------------|
| Ensamble Final | ENSAM | 2 | $50 |
| Control de Calidad | QC | 5 | $30 |
| Carpintería Externa | CARP | 10 | $0 |
| Lustrado y Acabados | LUST | 10 | $0 |
| Marmolería Externa | MARM | 5 | $0 |
| Metalurgia Externa | META | 10 | $0 |

---

## Resumen

| Tipo | Cantidad |
|------|----------|
| Work Centers internos | 2 |
| Work Centers externos (referencia) | 4 |
| **Total** | **6** |
