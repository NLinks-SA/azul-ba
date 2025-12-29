#!/usr/bin/env python3
"""
Test del cron de notificación diaria de entregas
"""
import xmlrpc.client
from datetime import datetime
from config import ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD

# Conexión
common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

print("=" * 60)
print("TEST CRON: Notificación Entregas del Día")
print("=" * 60)

# 1. Buscar pickings de salida para hoy
today = datetime.now().date()
today_str = today.strftime('%Y-%m-%d')
print(f"\n1. Buscando pickings de salida para hoy ({today_str})...")

pickings = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
    'stock.picking', 'search_read',
    [[
        ('picking_type_code', '=', 'outgoing'),
        ('scheduled_date', '>=', f'{today_str} 00:00:00'),
        ('scheduled_date', '<=', f'{today_str} 23:59:59'),
        ('state', 'not in', ['done', 'cancel']),
    ]],
    {'fields': ['name', 'partner_id', 'origin', 'scheduled_date', 'state']})

if pickings:
    print(f"   Encontrados: {len(pickings)} picking(s)")
    for p in pickings:
        partner = p['partner_id'][1] if p['partner_id'] else 'N/A'
        print(f"   - {p['name']} | Cliente: {partner} | Origen: {p['origin'] or 'N/A'} | Estado: {p['state']}")
else:
    print("   No hay pickings de salida programados para hoy.")
    print("\n   Creando un picking de prueba para el test...")

    # Buscar tipo de picking de salida
    pick_type = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
        'stock.picking.type', 'search_read',
        [[('code', '=', 'outgoing')]],
        {'fields': ['id', 'name', 'default_location_src_id', 'default_location_dest_id'], 'limit': 1})

    if pick_type:
        pick_type = pick_type[0]
        # Buscar un partner
        partner = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
            'res.partner', 'search_read',
            [[('customer_rank', '>', 0)]],
            {'fields': ['id', 'name'], 'limit': 1})

        partner_id = partner[0]['id'] if partner else False

        # Buscar un producto
        product = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
            'product.product', 'search_read',
            [[('detailed_type', '=', 'consu')]],
            {'fields': ['id', 'name', 'uom_id'], 'limit': 1})

        if not product:
            product = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                'product.product', 'search_read',
                [[]],
                {'fields': ['id', 'name', 'uom_id'], 'limit': 1})

        if product:
            # Buscar ubicación de cliente
            customer_loc = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                'stock.location', 'search_read',
                [[('usage', '=', 'customer')]],
                {'fields': ['id'], 'limit': 1})

            src_loc_id = pick_type['default_location_src_id'][0] if pick_type.get('default_location_src_id') else False
            dest_loc_id = customer_loc[0]['id'] if customer_loc else (pick_type['default_location_dest_id'][0] if pick_type.get('default_location_dest_id') else False)

            # Crear picking de prueba
            picking_vals = {
                'picking_type_id': pick_type['id'],
                'partner_id': partner_id,
                'scheduled_date': f'{today_str} 14:00:00',
                'origin': 'TEST-CRON-ENTREGAS',
                'location_id': src_loc_id,
                'location_dest_id': dest_loc_id,
                'move_ids': [(0, 0, {
                    'name': product[0]['name'],
                    'product_id': product[0]['id'],
                    'product_uom_qty': 1,
                    'product_uom': product[0]['uom_id'][0],
                    'location_id': src_loc_id,
                    'location_dest_id': dest_loc_id,
                })]
            }
            new_picking_id = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                'stock.picking', 'create', [picking_vals])
            print(f"   Picking de prueba creado: ID {new_picking_id}")

            # Confirmar el picking
            models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                'stock.picking', 'action_confirm', [[new_picking_id]])
            print("   Picking confirmado.")

            pickings = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                'stock.picking', 'search_read',
                [[('id', '=', new_picking_id)]],
                {'fields': ['name', 'partner_id', 'origin', 'scheduled_date', 'state']})

            if pickings:
                p = pickings[0]
                partner = p['partner_id'][1] if p['partner_id'] else 'N/A'
                print(f"   - {p['name']} | Cliente: {partner} | Origen: {p['origin']} | Estado: {p['state']}")

# 2. Verificar grupo Logística y sus usuarios
print("\n2. Verificando grupo Logística...")
logistica_group = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
    'res.groups', 'search_read',
    [[('name', '=', 'Logística')]],
    {'fields': ['id', 'name', 'user_ids']})

if logistica_group:
    group = logistica_group[0]
    print(f"   Grupo encontrado: ID {group['id']}")

    if group['user_ids']:
        users = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
            'res.users', 'search_read',
            [[('id', 'in', group['user_ids'])]],
            {'fields': ['name', 'partner_id']})
        print(f"   Usuarios en el grupo: {len(users)}")
        for u in users:
            print(f"   - {u['name']}")
    else:
        print("   ⚠ No hay usuarios en el grupo Logística!")
        print("   Agregando usuario actual al grupo...")
        models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
            'res.groups', 'write', [[group['id']], {'user_ids': [(4, uid)]}])
        print("   Usuario agregado.")
else:
    print("   ⚠ Grupo Logística no encontrado!")

# 3. Buscar el cron
print("\n3. Buscando cron de notificación...")
cron = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
    'ir.cron', 'search_read',
    [[('name', 'ilike', 'Entrega')]],
    {'fields': ['id', 'name', 'active', 'nextcall', 'ir_actions_server_id']})

if cron:
    cron = cron[0]
    print(f"   Cron encontrado: {cron['name']} (ID: {cron['id']})")
    print(f"   Activo: {cron['active']}")
    print(f"   Próxima ejecución: {cron['nextcall']}")

    # 4. Ejecutar el cron manualmente
    print("\n4. Ejecutando cron manualmente...")
    try:
        # Ejecutar el método del cron directamente
        models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
            'ir.cron', 'method_direct_trigger', [[cron['id']]])
        print("   ✓ Cron ejecutado exitosamente!")
    except Exception as e:
        print(f"   ✗ Error al ejecutar cron: {e}")
        # Intentar con la acción de servidor
        if cron.get('ir_actions_server_id'):
            print("   Intentando con acción de servidor...")
            try:
                action_id = cron['ir_actions_server_id'][0]
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                    'ir.actions.server', 'run', [[action_id]])
                print("   ✓ Acción ejecutada exitosamente!")
            except Exception as e2:
                print(f"   ✗ Error: {e2}")
else:
    print("   ⚠ Cron no encontrado!")
    print("   Buscando acción de servidor...")

    action = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
        'ir.actions.server', 'search_read',
        [[('name', 'ilike', 'Entrega')]],
        {'fields': ['id', 'name']})

    if action:
        action = action[0]
        print(f"   Acción encontrada: {action['name']} (ID: {action['id']})")
        print("\n4. Ejecutando acción de servidor...")
        try:
            models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
                'ir.actions.server', 'run', [[action['id']]])
            print("   ✓ Acción ejecutada exitosamente!")
        except Exception as e:
            print(f"   ✗ Error: {e}")
    else:
        print("   ⚠ No se encontró acción de servidor relacionada.")

# 5. Verificar si se crearon mensajes
print("\n5. Verificando mensajes enviados...")
messages = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD,
    'mail.message', 'search_read',
    [[
        ('body', 'ilike', 'ENTREGAS'),
        ('create_date', '>=', f'{today_str} 00:00:00')
    ]],
    {'fields': ['body', 'create_date', 'author_id'], 'limit': 5})

if messages:
    print(f"   Encontrados {len(messages)} mensaje(s) de entregas:")
    for m in messages:
        # Limpiar HTML del body
        body = m['body']
        if '<' in body:
            import re
            body = re.sub('<[^<]+?>', '', body)
        body = body[:150] + '...' if len(body) > 150 else body
        print(f"   - {m['create_date']}")
        print(f"     {body}")
else:
    print("   No se encontraron mensajes de entregas para hoy.")

print("\n" + "=" * 60)
print("Test completado")
print("=" * 60)
