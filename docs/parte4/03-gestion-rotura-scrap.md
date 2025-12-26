# Gestión de Rotura y Scrap

## Resumen

Este documento describe cómo manejar material dañado o roto durante el proceso de producción, utilizando el módulo **Approvals** de Odoo Enterprise para controlar la autorización y el módulo de **Scrap** para registrar las pérdidas.

---

## Conceptos Clave

| Concepto | Descripción |
|----------|-------------|
| **Scrap** | Material que no puede usarse y debe descartarse o revisarse |
| **Approval** | Solicitud de autorización que requiere aprobación de un supervisor |
| **Ubicación Revisión** | Destino temporal para material que podría recuperarse |
| **Ubicación Descarte** | Destino final para material irrecuperable (pérdida contable) |
| **should_replenish** | Campo que controla si se repone automáticamente el material |

---

## Flujo de Rotura con Autorización

```
1. OPERARIO DETECTA ROTURA
   │
   ▼
2. CREA SOLICITUD DE APROBACIÓN
   └─ Categoría: "Autorización de Rotura/Scrap"
   └─ Incluye: Producto, cantidad, referencia MO/PO, monto pérdida
   └─ Estado: PENDING
   │
   ▼
3. SUPERVISOR REVISA
   └─ Accede a: Aprobaciones → Solicitudes pendientes
   └─ Opciones: Aprobar / Rechazar
   └─ Estado: APPROVED o REFUSED
   │
   ▼
4. SI APROBADO → REGISTRAR SCRAP
   └─ Crear scrap con referencia a MO original
   └─ Destino: "Revisión" o "Descarte"
   └─ should_replenish: True/False según decisión
   │
   ▼
5. IMPACTO CONTABLE
   └─ Movimiento genera asiento de pérdida
   └─ Valoración del inventario actualizada
```

### Diagrama de Actores

```
OPERARIO                    SUPERVISOR                  SISTEMA
────────────────────────────────────────────────────────────────
Detecta rotura
      │
      ▼
Crea solicitud ──────────► Recibe notificación
aprobación                        │
      │                           ▼
      │                    Revisa y aprueba
      │                           │
      ◄───────────────────────────┘
      │
      ▼
Crea Scrap
→ Revisión
      │
      ▼
(Evaluación técnica)
      │
      ▼
Crea Scrap                                           Registra pérdida
→ Descarte ──────────────────────────────────────►  Genera reposición
                                                    Asiento contable
```

### Diagrama de Decisión

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DE ROTURA EN ODOO                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ROTURA DETECTADA                                               │
│        │                                                        │
│        ▼                                                        │
│  ┌─────────────┐     ┌─────────────┐                           │
│  │  SOLICITUD  │────►│ SUPERVISOR  │                           │
│  │  APROBACIÓN │     │  APRUEBA    │                           │
│  └─────────────┘     └──────┬──────┘                           │
│                             │                                   │
│        ┌────────────────────┼────────────────────┐             │
│        ▼                    ▼                    ▼             │
│  ┌──────────┐        ┌──────────┐        ┌──────────┐         │
│  │ REVISIÓN │        │ DESCARTE │        │ RECHAZAR │         │
│  │(evaluar) │        │(pérdida) │        │(sin acc.)│         │
│  └────┬─────┘        └────┬─────┘        └──────────┘         │
│       │                   │                                    │
│       ▼                   ▼                                    │
│  ┌──────────┐        ┌──────────┐                              │
│  │Reproceso │        │ Asiento  │                              │
│  │o Descarte│        │ Contable │                              │
│  └──────────┘        │ Pérdida  │                              │
│                      └────┬─────┘                              │
│                           │                                    │
│                           ▼                                    │
│                    ┌──────────────┐                            │
│                    │  REPOSICIÓN  │                            │
│                    │ (nueva PO/MO)│                            │
│                    └──────────────┘                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Configuración

### 1. Ubicaciones de Scrap

El script `setup_real.py` crea automáticamente:

| Ubicación | Uso | Tipo |
|-----------|-----|------|
| `Inventory adjustment/Revisión` | Material pendiente de evaluar si se puede recuperar | inventory |
| `Inventory adjustment/Descarte` | Material descartado definitivamente (pérdida) | inventory |

### 2. Categoría de Aprobación

Se crea la categoría **"Autorización de Rotura/Scrap"** con:

| Campo | Configuración |
|-------|---------------|
| `has_product` | Requerido - Producto dañado |
| `has_quantity` | Requerido - Cantidad afectada |
| `has_reference` | Requerido - Referencia MO/PO original |
| `has_amount` | Opcional - Costo estimado de pérdida |
| `has_date` | Opcional - Fecha del incidente |
| `has_partner` | Opcional - Proveedor responsable |
| `requirer_document` | Opcional - Fotos del daño |
| `approval_minimum` | 1 - Mínimo un aprobador |

### 3. Aprobadores

Por defecto se configura al usuario que ejecuta el script como aprobador. Se pueden agregar más supervisores desde:

**Aprobaciones → Configuración → Tipos de aprobación → Autorización de Rotura/Scrap → Aprobadores**

---

## Operación Manual

### Paso 1: Crear Solicitud de Aprobación

1. Ir a **Aprobaciones → Nueva solicitud**
2. Seleccionar categoría: **"Autorización de Rotura/Scrap"**
3. Completar campos:
   - **Asunto**: Descripción breve (ej: "Rotura Tapa Piedra - Rayones")
   - **Producto**: Seleccionar el producto dañado
   - **Cantidad**: Número de unidades afectadas
   - **Referencia**: MO o PO relacionada
   - **Monto**: Costo estimado de la pérdida
   - **Descripción**: Detalles del incidente, causa, propuesta
4. **Enviar** la solicitud

### Paso 2: Aprobar/Rechazar (Supervisor)

1. Supervisor recibe notificación
2. Accede a **Aprobaciones → Por aprobar**
3. Revisa la solicitud
4. **Aprobar** o **Rechazar** con comentarios

### Paso 3: Registrar Scrap (Si Aprobado)

1. Ir a **Inventario → Operaciones → Scrap**
2. Crear nuevo scrap:
   - **Producto**: El producto dañado
   - **Cantidad**: Unidades a descartar
   - **Ubicación origen**: Donde está el material (ej: WH/Stock)
   - **Ubicación destino**: Revisión o Descarte
   - **Orden de manufactura**: Enlazar a la MO original
   - **Documento origen**: Referencia al pedido (ej: "S00001 - ROTURA")
   - **Reponer cantidades**: Desmarcar si no se quiere regenerar automáticamente
3. **Validar** el scrap

---

## Campos del Modelo stock.scrap

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `product_id` | many2one | Producto a descartar |
| `scrap_qty` | float | Cantidad a descartar |
| `location_id` | many2one | Ubicación de origen |
| `scrap_location_id` | many2one | Ubicación destino (Revisión/Descarte) |
| `production_id` | many2one | Enlace a Orden de Manufactura |
| `origin` | char | Documento de origen (referencia) |
| `should_replenish` | boolean | Si debe generar reposición automática |
| `scrap_reason_tag_ids` | many2many | Etiquetas de motivo de scrap |
| `state` | selection | Estado: draft, done |

---

## Escenarios de Uso

### Escenario 1: Tapa de Piedra con Rayones

```
Situación: Tapa Neolith llegó con rayones de transporte

1. Operario crea solicitud:
   - Producto: Tapa Neolith Calacatta 180x90
   - Cantidad: 1
   - Referencia: WH/SBC/00005 / S00003
   - Monto: $850,000
   - Descripción: "Rayones visibles en superficie. Posible recuperación con pulido."

2. Supervisor aprueba → decide enviar a Revisión

3. Se crea scrap:
   - Origen: WH/Stock
   - Destino: Revisión
   - should_replenish: False (esperar evaluación)

4. Técnico evalúa:
   - Si recuperable: Reproceso (nuevo lustrado)
   - Si irrecuperable: Nuevo scrap a Descarte + should_replenish=True
```

### Escenario 2: Base con Defecto de Soldadura

```
Situación: Base Acero con soldadura defectuosa del proveedor

1. Operario detecta en QC y crea solicitud:
   - Producto: Base Fix 180x90
   - Cantidad: 1
   - Referencia: WH/IN/00010 (recepción)
   - Contacto: AX Aluminio (proveedor)
   - Descripción: "Soldadura irregular. Reclamar al proveedor."

2. Supervisor aprueba → decide descartar

3. Se crea scrap:
   - Origen: WH/Stock
   - Destino: Descarte
   - should_replenish: True (generar nueva PO)

4. Sistema genera automáticamente nueva PO al proveedor
```

### Escenario 3: Error en Lustrado

```
Situación: Tapa de madera con lustre disparejo

1. Operario crea solicitud:
   - Producto: Tapa MDF Terminada 200x100 (Lustre Mate)
   - Referencia: WH/SBC/00008
   - Contacto: Gustavo Lus (subcontratista)

2. Supervisor aprueba → decide reprocesar

3. Se crea scrap:
   - Origen: WH/Stock
   - Destino: Revisión
   - should_replenish: False

4. Se crea nueva Subcontract MO para re-lustrar
```

---

## Impacto Contable

Cuando se valida un scrap a ubicación tipo `inventory`:

1. **Movimiento de stock**: Producto sale del almacén
2. **Asiento contable**:
   - Débito: Cuenta de pérdidas por scrap
   - Crédito: Cuenta de inventario
3. **Valoración**: Costo del producto registrado como pérdida

!!! note "Configuración Contable"
    La cuenta de pérdidas se configura en:
    **Inventario → Configuración → Categorías de producto → Propiedades contables**

---

## URLs de Acceso

| Función | URL |
|---------|-----|
| **Aprobaciones** | `/odoo/approvals` |
| **Crear solicitud** | `/odoo/approvals/new` |
| **Scrap** | `/odoo/inventory` → Operaciones → Scrap |
| **Ubicaciones** | `/odoo/stock-location` |

---

## Checklist de Implementación

- [ ] Módulo Approvals instalado
- [ ] Ubicación "Revisión" creada
- [ ] Ubicación "Descarte" creada
- [ ] Categoría "Autorización de Rotura/Scrap" configurada
- [ ] Aprobadores asignados
- [ ] Cuentas contables de pérdida configuradas
- [ ] Equipo capacitado en el flujo

---

## Troubleshooting

### Error: "No se encontró regla de reabastecimiento"

**Causa**: El producto no tiene ruta de compra/manufactura configurada.

**Solución**: Configurar ruta en el producto:
1. Ir al producto → Pestaña Inventario
2. Agregar ruta "Comprar" o "Fabricar"
3. Configurar proveedor con precio y lead time

### Scrap no genera asiento contable

**Causa**: Producto no es "almacenable" o categoría sin cuentas.

**Solución**:
1. Verificar que el producto sea `is_storable = True`
2. Configurar cuentas en la categoría del producto
