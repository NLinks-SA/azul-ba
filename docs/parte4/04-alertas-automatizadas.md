# Alertas Automatizadas

## Resumen

Este documento describe cómo configurar alertas automáticas para notificar al equipo de logística sobre:
1. **MO Completada**: Cuando una orden de manufactura se completa
2. **Entregas del Día**: Resumen diario de entregas programadas (email)

---

## Configuración Automática

El script `setup_real.py` crea automáticamente:

| Componente | Descripción |
|------------|-------------|
| **Grupo Logística** | Grupo de usuarios que reciben las alertas |
| **Acción MO Completada** | Notifica en chatter cuando MO → done |
| **Regla automatizada** | Trigger que dispara la acción cuando MO → done |
| **Acción Entregas Diarias** | Envía email con entregas del día |
| **Cron Entregas** | Ejecuta la acción todos los días a las 7:00 AM |

---

## Alerta 1: MO Completada (Configuración Manual)

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

## Alerta 2: Entregas del Día (Configuración Manual)

Esta alerta envía un email diario con todas las entregas programadas para el día.

### Paso 1: Crear Acción de Servidor

1. Activar **Modo desarrollador**
2. Ir a **Ajustes → Técnico → Acciones de servidor**
3. Click en **Nuevo**
4. Completar:

| Campo | Valor |
|-------|-------|
| **Nombre** | `Notificación Diaria: Entregas del Día` |
| **Modelo** | `Transferencia (stock.picking)` |
| **Tipo de acción** | `Ejecutar código Python` |

5. En el campo **Código Python**, pegar:

```python
# Notificación diaria: Entregas programadas para hoy
today = datetime.datetime.now().date()
today_start = datetime.datetime.combine(today, datetime.time.min)
today_end = datetime.datetime.combine(today, datetime.time.max)

pickings = env['stock.picking'].search([
    ('picking_type_code', '=', 'outgoing'),
    ('scheduled_date', '>=', today_start),
    ('scheduled_date', '<=', today_end),
    ('state', 'not in', ['done', 'cancel']),
])

if pickings:
    lines = ['<h2>ENTREGAS PROGRAMADAS PARA HOY (' + str(today) + ')</h2>', '<ul>']

    for p in pickings:
        line = '<li><b>' + (p.name or '') + '</b>'
        line += ' - Cliente: ' + (p.partner_id.name if p.partner_id else 'N/A')
        line += ' - Origen: ' + (p.origin or 'N/A') + '</li>'
        lines.append(line)

    lines.append('</ul>')
    lines.append('<p><b>Total: ' + str(len(pickings)) + ' entrega(s)</b></p>')

    msg = ''.join(lines)

    # Enviar email al grupo Logística
    logistica_group = env['res.groups'].search([('name', '=', 'Logística')], limit=1)
    if logistica_group:
        emails = logistica_group.user_ids.mapped('email')
        email_to = ','.join([e for e in emails if e])
        if email_to:
            mail = env['mail.mail'].create({
                'subject': 'Entregas del Día: ' + str(today),
                'body_html': msg,
                'email_to': email_to,
                'auto_delete': True,
            })
            mail.send()
```

6. **Guardar** y anotar el **ID** de la acción (visible en la URL)

### Paso 2: Crear Acción Programada (Cron)

1. Ir a **Ajustes → Técnico → Acciones programadas**
2. Click en **Nuevo**
3. Completar:

| Campo | Valor |
|-------|-------|
| **Nombre** | `Notificación Entregas del Día` |
| **Modelo** | `Transferencia (stock.picking)` |
| **Ejecutar cada** | `1 Días` |
| **Siguiente ejecución** | (fecha de mañana a las 10:00:00 UTC = 7:00 Argentina) |

4. En **Código Python**, pegar:

```python
model.env['ir.actions.server'].browse(ID_DE_LA_ACCION).run()
```

> **Nota:** Reemplazar `ID_DE_LA_ACCION` con el ID real de la acción creada en el paso anterior.

5. **Guardar**

### Diagrama de Funcionamiento

```
                                    SISTEMA (7:00 AM Argentina)
───────────────────────────────────────────────────────────────────────────────
                                         │
                                         ▼
                                  Cron se ejecuta
                                         │
                                         ▼
                                  Busca pickings de salida
                                  programados para HOY
                                         │
                          ┌──────────────┴──────────────┐
                          ▼                             ▼
                   Hay entregas                   No hay entregas
                          │                             │
                          ▼                             ▼
                   Genera lista HTML              No hace nada
                          │
                          ▼
                   Busca grupo "Logística"
                          │
                          ▼
                   Obtiene emails de usuarios
                          │
                          ▼
                   Envía email ─────────────────► LOGÍSTICA recibe email
                                                  con lista de entregas
```

### Ejemplo de Email Recibido

```
Asunto: Entregas del Día: 2025-12-29

ENTREGAS PROGRAMADAS PARA HOY (2025-12-29)

• WH/OUT/00001 - Cliente: Alejandro Herrero - Origen: S00001
• WH/OUT/00004 - Cliente: AX Aluminio - Origen: Devolución de WH/IN/00002

Total: 2 entrega(s)
```

### Cambiar Horario de Envío

1. Ir a **Ajustes → Técnico → Acciones programadas**
2. Buscar **"Notificación Entregas del Día"**
3. Modificar el campo **Siguiente ejecución**
4. **Guardar**

> **Nota sobre zona horaria:** Odoo usa UTC internamente. Para Argentina (UTC-3):
> - 7:00 AM Argentina = 10:00 UTC
> - 8:00 AM Argentina = 11:00 UTC
> - 9:00 AM Argentina = 12:00 UTC

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
| **Acciones programadas (Cron)** | `/odoo/ir.cron` |
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

### El email de entregas diarias no llega

1. Verificar que el cron esté **activo** (Ajustes → Técnico → Acciones programadas)
2. Verificar que los usuarios del grupo "Logística" tengan **email configurado**
3. Verificar que haya pickings de salida programados para el día
4. Revisar cola de emails: Ajustes → Técnico → Emails

### Probar el cron manualmente

1. Ir a **Ajustes → Técnico → Acciones programadas**
2. Buscar **"Notificación Entregas del Día"**
3. Click en botón **"Ejecutar ahora"** (ícono de play)
4. Verificar email recibido
