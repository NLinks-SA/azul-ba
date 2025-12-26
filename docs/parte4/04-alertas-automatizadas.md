# Alertas Automatizadas

## Resumen

Este documento describe cómo configurar alertas automáticas para notificar al equipo de logística cuando una orden de manufactura se completa.

---

## Configuración Automática

El script `setup_real.py` crea automáticamente:

| Componente | Descripción |
|------------|-------------|
| **Grupo Logística** | Grupo de usuarios que reciben las alertas |
| **Acción de servidor** | Código que envía la notificación |
| **Regla automatizada** | Trigger que dispara la acción cuando MO → done |

---

## Configuración Manual desde la UI

### Paso 1: Crear Grupo de Usuarios

1. Ir a **Ajustes → Usuarios y Compañías → Grupos**
2. Click en **Nuevo**
3. Completar:
   - **Nombre**: `Logística`
   - **Comentario**: `Equipo de logística - recibe alertas de producción completada`
4. **Guardar**

### Paso 2: Agregar Usuarios al Grupo

1. Ir a **Ajustes → Usuarios y Compañías → Usuarios**
2. Seleccionar el usuario deseado
3. En la pestaña **Permisos de acceso**, buscar el grupo "Logística"
4. Marcar la casilla para agregar al grupo
5. **Guardar**

### Paso 3: Crear Acción de Servidor

1. Activar **Modo desarrollador** (Ajustes → Activar modo desarrollador)
2. Ir a **Ajustes → Técnico → Acciones de servidor**
3. Click en **Nuevo**
4. Completar:

| Campo | Valor |
|-------|-------|
| **Nombre** | `Notificar Logística - MO Completada` |
| **Modelo** | `Orden de fabricación (mrp.production)` |
| **Tipo de acción** | `Ejecutar código Python` |

5. En el campo **Código Python**, pegar:

```python
# Notificar al grupo Logística (chatter + email opcional)
for record in records:
    logistica_group = env['res.groups'].search([('name', '=', 'Logística')], limit=1)
    if logistica_group:
        users = logistica_group.user_ids
        partner_ids = users.mapped('partner_id').ids

        msg = 'PRODUCCION COMPLETADA - Orden: ' + record.name + ' - Producto: ' + record.product_id.display_name + ' - Lista para logistica.'

        # Notificación en chatter (siempre)
        record.message_post(
            body=msg,
            partner_ids=partner_ids,
            message_type='notification',
        )

        # Email a los usuarios del grupo (opcional - descomentar si se desea)
        # record.message_notify(
        #     body=msg,
        #     partner_ids=partner_ids,
        #     subject='MO Completada: ' + record.name,
        # )
```

6. **Guardar**

### Paso 4: Crear Regla Automatizada

1. Ir a **Ajustes → Técnico → Reglas de automatización**
2. Click en **Nuevo**
3. Completar:

| Campo | Valor |
|-------|-------|
| **Nombre** | `Alerta Logística: MO Completada` |
| **Modelo** | `Orden de fabricación (mrp.production)` |
| **Disparador** | `Al actualizar` |
| **Aplicar en** | `[('state', '=', 'done')]` |
| **Antes de la actualización** | `[('state', '!=', 'done')]` |

4. En la sección **Acciones**, agregar la acción creada en el paso anterior
5. **Guardar**

---

## Diagrama de Funcionamiento

```
OPERADOR COMPLETA MO                    SISTEMA                         LOGÍSTICA
─────────────────────────────────────────────────────────────────────────────────
        │
        ▼
   MO → estado 'done'
        │
        └──────────────────────► Regla automatizada
                                 se dispara
                                        │
                                        ▼
                                 Acción de servidor
                                 se ejecuta
                                        │
                                        ▼
                                 Busca grupo
                                 "Logística"
                                        │
                                        ▼
                                 Envía notificación ──────────► Recibe mensaje
                                 en chatter                     en chatter de MO
                                        │
                                        ▼
                                 (Opcional)
                                 Envía email ─────────────────► Recibe email
```

---

## Activar Notificación por Email

Por defecto, solo se envía notificación en el chatter. Para activar también el envío de email:

1. Ir a **Ajustes → Técnico → Acciones de servidor**
2. Abrir **"Notificar Logística - MO Completada"**
3. En el código Python, descomentar las líneas:

```python
        # Email a los usuarios del grupo (opcional - descomentar si se desea)
        record.message_notify(
            body=msg,
            partner_ids=partner_ids,
            subject='MO Completada: ' + record.name,
        )
```

4. **Guardar**

---

## Personalización

### Cambiar el Mensaje

Editar la variable `msg` en el código de la acción de servidor:

```python
msg = 'PRODUCCION COMPLETADA - Orden: ' + record.name + ' - Producto: ' + record.product_id.display_name + ' - Lista para logistica.'
```

### Agregar Más Información

Campos disponibles de `record` (mrp.production):

| Campo | Descripción |
|-------|-------------|
| `record.name` | Número de la MO (ej: WH/MO/00001) |
| `record.product_id.display_name` | Nombre completo del producto |
| `record.product_qty` | Cantidad producida |
| `record.date_start` | Fecha de inicio |
| `record.date_finished` | Fecha de finalización |
| `record.origin` | Documento origen (ej: SO001) |
| `record.user_id.name` | Usuario responsable |

### Ejemplo con Más Detalles

```python
msg = 'PRODUCCION COMPLETADA\n'
msg += 'Orden: ' + record.name + '\n'
msg += 'Producto: ' + record.product_id.display_name + '\n'
msg += 'Cantidad: ' + str(record.product_qty) + '\n'
msg += 'Origen: ' + (record.origin or 'N/A') + '\n'
msg += 'Lista para logistica.'
```

---

## Otras Alertas Posibles

El mismo patrón se puede usar para otros eventos:

| Evento | Modelo | Filtro |
|--------|--------|--------|
| **PO Confirmada** | `purchase.order` | `state = 'purchase'` |
| **Recepción completa** | `stock.picking` | `state = 'done'` y `picking_type_code = 'incoming'` |
| **Entrega lista** | `stock.picking` | `state = 'assigned'` y `picking_type_code = 'outgoing'` |
| **SO Confirmada** | `sale.order` | `state = 'sale'` |
| **Scrap creado** | `stock.scrap` | `state = 'done'` |

---

## URLs de Acceso

| Función | URL |
|---------|-----|
| **Reglas automatización** | `/odoo/automated-actions` |
| **Acciones de servidor** | `/odoo/ir.actions.server` |
| **Grupos** | `/odoo/res.groups` |

---

## Troubleshooting

### La alerta no se dispara

1. Verificar que la regla automatizada esté **activa**
2. Verificar que los filtros sean correctos
3. Revisar que el grupo "Logística" tenga usuarios

### No aparece el mensaje en el chatter

1. Verificar que el usuario esté en el grupo "Logística"
2. Refrescar la página de la MO
3. Buscar el mensaje en la sección de chatter (puede estar colapsada)

### Error en el código Python

1. Ir a **Ajustes → Técnico → Acciones de servidor**
2. Abrir la acción y revisar el código
3. Verificar que no haya caracteres especiales o comillas mal escapadas
