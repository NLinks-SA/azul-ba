# 1. Work Centers

Los Work Centers (Centros de Trabajo) representan estaciones donde se realizan operaciones de fabricación **internas**.

## Acceder a Work Centers

```
Manufactura → Configuración → Work Centers
```

---

## 1.1 Work Centers a Crear

Solo necesitamos Work Centers para operaciones que hacemos **nosotros**:

| Work Center | Código | Uso |
|-------------|--------|-----|
| Ensamble Final | ENSAM | Interno - donde se ensambla la mesa |
| Control de Calidad | QC | Interno - inspección |

!!! info "¿Por qué NO creamos Work Centers para proveedores?"
    Los proveedores externos (Carpintería, Lustrador, Metalúrgica, etc.) son **subcontratistas**.
    El trabajo lo hacen ellos, no nosotros. Por eso:

    - No controlamos sus operaciones internas
    - El tiempo de entrega se define en el Lead Time del proveedor
    - El costo está en la PO, no en operaciones

---

## 1.2 Crear Work Center: Ensamble Final

Click en **Nuevo**

### Pestaña: Información General

| Campo | Valor |
|-------|-------|
| **Nombre** | Ensamble Final |
| **Código** | ENSAM |
| **Tiempo antes de producción** | 15 min |
| **Tiempo después de producción** | 10 min |

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

## 1.4 Configurar Capacidades Específicas (Opcional)

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

---

## Resumen

| Tipo | Cantidad |
|------|----------|
| Work Centers internos | 2 |
| **Total** | **2** |

---

## Siguiente Paso

Con los Work Centers creados, pasamos a configurar las **BoMs de Mesa**.

➡️ [BoMs de Mesa](02-bom-mesa.md)
