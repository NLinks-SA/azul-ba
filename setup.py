#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
SETUP DEMO COMPLETO - ODOO 19 MUEBLERÍA
═══════════════════════════════════════════════════════════════════════════════

Este script configura una demo completa de fabricación de muebles incluyendo:

PRODUCTOS:
- Mesa Comedor Premium con variantes (Material Tapa × Base × Medida)
- Tapas: Mármol, Neolith (compra directa), Madera (con terminaciones)
- Bases: Acero Negro, Acero Dorado (subcontratación metalúrgica)
- Terminaciones para madera: Lustre Mate, Lustre Brillante, Natural

PROVEEDORES:
- Marmolería Del Sur (tapas mármol)
- Neolith Argentina (tapas neolith)
- Carpintería Artesanal Hnos. García (tapas madera SIN terminar)
- Lustres & Acabados Premium (terminación de tapas madera)
- Metalúrgica Precisión S.A. (bases metálicas)

PLANIFICACIÓN:
- Work Centers con tiempos de setup/cleanup
- Operaciones (Routings) para cada producto
- Lead Times en proveedores y BoMs
- Capacidades de producción

FLUJO DE MADERA (Dropship Subcontractor):
SO → PO Lustrador → (confirm) → Subcontract MO → PO Carpintería → (dropship) → Lustrador
La PO a Carpintería queda vinculada a la cadena SO/PO Lustrador para trazabilidad completa

USO:
    python setup.py              # Solo ejecuta setup
    python setup.py --limpiar    # Limpia y ejecuta setup
    python setup.py --solo-limpiar  # Solo limpia (no ejecuta setup)
═══════════════════════════════════════════════════════════════════════════════
"""

import xmlrpc.client
import sys
import time
from config import ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD

# ═══════════════════════════════════════════════════════════════════════════════
# CONEXIÓN
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("CONECTANDO A ODOO")
print("═"*70)

common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

if not uid:
    print("Error de autenticación")
    sys.exit(1)

print(f"  Conectado como usuario ID: {uid}")
print(f"  URL: {ODOO_URL}")
print(f"  DB: {ODOO_DB}")

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def execute(model, method, *args, **kwargs):
    return models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, model, method, *args, **kwargs)

def install_module(module_name):
    """Instala un módulo si no está instalado"""
    module = execute('ir.module.module', 'search_read',
        [[['name', '=', module_name]]], {'fields': ['state']})
    if module and module[0]['state'] == 'installed':
        return False  # Ya instalado

    # Buscar el módulo
    module_ids = execute('ir.module.module', 'search', [[['name', '=', module_name]]])
    if not module_ids:
        print(f"      ✗ Módulo '{module_name}' no encontrado")
        return False

    # Instalar
    execute('ir.module.module', 'button_immediate_install', [module_ids])
    return True

def set_config_settings(settings_dict):
    """Aplica configuraciones via res.config.settings"""
    # Crear nuevo registro de settings
    settings_id = execute('res.config.settings', 'create', [settings_dict])
    # Ejecutar set_values para aplicar
    execute('res.config.settings', 'execute', [[settings_id]])
    return settings_id

def search(model, domain, **kwargs):
    return execute(model, 'search', [domain], kwargs)

def search_read(model, domain, fields=None, **kwargs):
    opts = kwargs.copy()
    if fields:
        opts['fields'] = fields
    return execute(model, 'search_read', [domain], opts)

def create(model, vals):
    return execute(model, 'create', [vals])

def write(model, ids, vals):
    if ids:
        return execute(model, 'write', [ids, vals])
    return False

def get_or_create(model, domain, vals):
    """Busca un registro, si no existe lo crea"""
    existing = search_read(model, domain, ['id'])
    if existing:
        return existing[0]['id'], False
    new_id = create(model, vals)
    return new_id, True

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════
MEDIDAS = [
    {'codigo': '180x90', 'nombre': '180x90 cm', 'factor_precio': 1.0},
    {'codigo': '220x100', 'nombre': '220x100 cm', 'factor_precio': 1.4},
]

TERMINACIONES = [
    {'nombre': 'Lustre Mate', 'costo_adicional': 90000},
    {'nombre': 'Lustre Brillante', 'costo_adicional': 120000},
    {'nombre': 'Natural', 'costo_adicional': 60000},
]

# Terminaciones para Mesa (incluye opción para no-madera)
TERMINACIONES_MESA = [
    {'nombre': 'Sin Terminación', 'costo_adicional': 0, 'aplica_madera': False},
    {'nombre': 'Lustre Mate', 'costo_adicional': 90000, 'aplica_madera': True},
    {'nombre': 'Lustre Brillante', 'costo_adicional': 120000, 'aplica_madera': True},
    {'nombre': 'Natural', 'costo_adicional': 60000, 'aplica_madera': True},
]

MATERIALES_TAPA = [
    {
        'nombre': 'Mármol Carrara',
        'codigo': 'MARMOL',
        'costo_base': 675000,
        'proveedor': 'Marmolería Del Sur',
        'requiere_terminacion': False,
        'lead_time': 7,
    },
    {
        'nombre': 'Neolith Negro',
        'codigo': 'NEOLITH',
        'costo_base': 780000,
        'proveedor': 'Neolith Argentina',
        'requiere_terminacion': False,
        'lead_time': 10,
    },
    {
        'nombre': 'Madera Paraíso',
        'codigo': 'MADERA',
        'costo_base': 300000,
        'proveedor': 'Carpintería Artesanal Hnos. García',
        'requiere_terminacion': True,
        'proveedor_terminacion': 'Lustres & Acabados Premium',
        'lead_time': 5,
        'lead_time_terminacion': 3,
    },
]

MATERIALES_BASE = [
    {'nombre': 'Acero Negro', 'codigo': 'NEGRO', 'costo_base': 270000, 'lead_time': 5},
    {'nombre': 'Acero Dorado', 'codigo': 'DORADO', 'costo_base': 375000, 'lead_time': 5},
]

PROVEEDORES = [
    {
        'name': 'Marmolería Del Sur',
        'email': 'contacto@marmoleriasur.com',
        'phone': '+54 11 4555-1234',
        'city': 'Buenos Aires',
        'comment': 'Especialista en mármol y piedras naturales.',
    },
    {
        'name': 'Carpintería Artesanal Hnos. García',
        'email': 'ventas@carpinteriagarcia.com',
        'phone': '+54 11 4666-5678',
        'city': 'San Martín',
        'comment': 'Carpintería especializada en maderas nobles. Entrega tapas SIN terminar.',
    },
    {
        'name': 'Neolith Argentina',
        'email': 'info@neolith.com.ar',
        'phone': '+54 11 4777-9012',
        'city': 'Tigre',
        'comment': 'Distribuidor oficial Neolith. Superficies sinterizadas.',
    },
    {
        'name': 'Metalúrgica Precisión S.A.',
        'email': 'comercial@metalprecision.com.ar',
        'phone': '+54 11 4888-3456',
        'city': 'Pilar',
        'comment': 'Fabricación de bases metálicas. Acero negro y dorado.',
    },
    {
        'name': 'Lustres & Acabados Premium',
        'email': 'info@lustrespremium.com',
        'phone': '+54 11 4999-7890',
        'city': 'Avellaneda',
        'comment': 'Servicio de lustrado y terminaciones para madera.',
    },
]

CLIENTES = [
    {
        'name': 'Estudio de Arquitectura Modernista',
        'email': 'proyectos@arquitecturamodernista.com',
        'phone': '+54 11 5555-1111',
        'city': 'Buenos Aires',
    },
    {
        'name': 'Hotel Boutique La Estancia',
        'email': 'compras@hotellaestancia.com',
        'phone': '+54 11 5555-2222',
        'city': 'Buenos Aires',
    },
]

# Solo Work Centers que se usan en operaciones de BoM
# (CARP, MARM, META eliminados - los proveedores no necesitan Work Centers)
WORK_CENTERS_CONFIG = [
    {
        'name': 'Lustrado y Acabados',
        'code': 'LUST',
        'time_efficiency': 100,
        'time_start': 20,
        'time_stop': 30,
        'color': 2,
        'note': '<p><strong>Proveedor:</strong> Lustres & Acabados Premium</p><p><strong>Lead Time:</strong> 3 días hábiles</p><p><strong>Especialidad:</strong> Lustre Mate, Brillante, Natural</p>',
    },
    {
        'name': 'Ensamble Final',
        'code': 'ENSAM',
        'time_efficiency': 100,
        'time_start': 15,
        'time_stop': 10,
        'color': 5,
        'note': '<p><strong>Centro interno</strong></p><p><strong>Capacidad:</strong> 2 mesas simultáneas</p><p><strong>Operaciones:</strong> Unión tapa+base, nivelación, ajustes</p>',
    },
    {
        'name': 'Control de Calidad',
        'code': 'QC',
        'time_efficiency': 100,
        'time_start': 5,
        'time_stop': 5,
        'color': 9,
        'note': '<p><strong>Centro interno</strong></p><p><strong>Inspecciones:</strong> Verificación de componentes, control final, embalaje</p>',
    },
]

OPERACIONES_MESA = [
    {'name': '1. Ensamble Tapa + Base', 'workcenter_code': 'ENSAM', 'time_cycle_manual': 60, 'sequence': 10},
    {'name': '2. Control de Calidad Final', 'workcenter_code': 'QC', 'time_cycle_manual': 15, 'sequence': 20},
    {'name': '3. Embalaje', 'workcenter_code': 'ENSAM', 'time_cycle_manual': 30, 'sequence': 30},
]

OPERACIONES_LUSTRADO = [
    {'name': '1. Preparación y Envío a Lustrador', 'workcenter_code': 'LUST', 'time_cycle_manual': 30, 'sequence': 10},
    {'name': '2. Proceso de Lustrado (externo)', 'workcenter_code': 'LUST', 'time_cycle_manual': 480, 'sequence': 20},
    {'name': '3. Recepción y Verificación', 'workcenter_code': 'QC', 'time_cycle_manual': 20, 'sequence': 30},
]

# ═══════════════════════════════════════════════════════════════════════════════
# INSTALACIÓN DE MÓDULOS Y CONFIGURACIÓN INICIAL
# ───────────────────────────────────────────────────────────────────────────────
# Esta sección instala los módulos necesarios y habilita las configuraciones
# requeridas para el flujo completo de la demo.
# ═══════════════════════════════════════════════════════════════════════════════
if '--skip-install' not in sys.argv:
    print("\n" + "═"*70)
    print("INSTALACIÓN DE MÓDULOS")
    print("═"*70)

    # Módulos requeridos para la demo
    MODULOS_REQUERIDOS = [
        'sale_management',                    # Ventas
        'purchase',                           # Compras
        'mrp',                                # Fabricación
        'mrp_subcontracting',                 # Subcontratación
        'stock_dropshipping',                 # Triangulación (Dropship)
        'mrp_subcontracting_dropshipping',    # Dropship Subcontractor
        'quality_control',                    # Control de Calidad
    ]

    for modulo in MODULOS_REQUERIDOS:
        print(f"  Verificando {modulo}...", end=" ")
        try:
            if install_module(modulo):
                print("✓ Instalado")
            else:
                print("- Ya instalado")
        except Exception as e:
            print(f"✗ Error: {str(e)[:40]}")

    print("\n" + "═"*70)
    print("CONFIGURACIÓN DE AJUSTES")
    print("═"*70)

    # Habilitar configuraciones necesarias
    print("  Aplicando configuraciones del sistema...")
    try:
        set_config_settings({
            # Variantes de producto
            'group_product_variant': True,
            # Triangulación (Dropship)
            'module_stock_dropshipping': True,
            # MTO - Reabastecer sobre pedido
            'replenish_on_order': True,
            # Ubicaciones de almacenamiento
            'group_stock_multi_locations': True,
            # Rutas multi-paso
            'group_stock_adv_location': True,
            # Reporte de recepción
            'group_stock_reception_report': True,
            # Control de calidad
            'module_quality_control': True,
            # Órdenes de trabajo (MRP)
            'group_mrp_routings': True,
            # Subcontratación
            'module_mrp_subcontracting': True,
        })
        print("      ✓ Variantes de producto habilitadas")
        print("      ✓ Triangulación (Dropship) habilitada")
        print("      ✓ MTO (Reabastecer sobre pedido) habilitado")
        print("      ✓ Ubicaciones de almacenamiento habilitadas")
        print("      ✓ Rutas multi-paso habilitadas")
        print("      ✓ Reporte de recepción habilitado")
        print("      ✓ Control de calidad habilitado")
        print("      ✓ Órdenes de trabajo habilitadas")
        print("      ✓ Subcontratación habilitada")
    except Exception as e:
        print(f"      ✗ Error aplicando configuraciones: {str(e)[:50]}")

# ═══════════════════════════════════════════════════════════════════════════════
# LIMPIEZA OPCIONAL
# ───────────────────────────────────────────────────────────────────────────────
# Solo limpia productos y sus dependencias directas (MOs, BoMs, orderpoints).
# El resto (rutas, picking types, ubicaciones, work centers) se maneja
# idempotentemente en el setup (get_or_create, reactivación de archivados).
# ═══════════════════════════════════════════════════════════════════════════════
if '--limpiar' in sys.argv or '--solo-limpiar' in sys.argv:
    print("\n" + "═"*70)
    print("LIMPIANDO DATOS EXISTENTES")
    print("═"*70)

    # Buscar productos de demo
    productos_demo = search('product.template', [
        '|', '|', '|', '|',
        ['name', 'ilike', 'Mesa Comedor%'],
        ['name', 'ilike', 'Tapa %'],
        ['name', 'ilike', 'Base Acero%'],
        ['default_code', 'ilike', 'MESA-%'],
        ['default_code', 'ilike', 'TAPA-%'],
    ])

    if productos_demo:
        # Cancelar y eliminar MOs de productos demo
        mos = search('mrp.production', [
            ['product_id.product_tmpl_id', 'in', productos_demo],
            ['state', 'not in', ['done', 'cancel']]
        ])
        if mos:
            try:
                execute('mrp.production', 'action_cancel', [mos])
                execute('mrp.production', 'unlink', [mos])
                print(f"  {len(mos)} órdenes de fabricación eliminadas")
            except Exception as e:
                print(f"  No se pudieron eliminar MOs: {str(e)[:50]}")

        # Eliminar orderpoints de productos demo
        orderpoints = search('stock.warehouse.orderpoint', [['product_id.product_tmpl_id', 'in', productos_demo]])
        if orderpoints:
            execute('stock.warehouse.orderpoint', 'unlink', [orderpoints])
            print(f"  {len(orderpoints)} orderpoints eliminados")

        # Eliminar BoMs de productos demo
        boms = search('mrp.bom', [['product_tmpl_id', 'in', productos_demo]])
        if boms:
            execute('mrp.bom', 'unlink', [boms])
            print(f"  {len(boms)} BoMs eliminadas")

        write('product.template', productos_demo, {'active': False})
        print(f"  {len(productos_demo)} productos archivados")

# Si es solo limpieza, terminar aquí
if '--solo-limpiar' in sys.argv:
    print("\n" + "═"*70)
    print("LIMPIEZA COMPLETADA")
    print("═"*70)
    sys.exit(0)

# ═══════════════════════════════════════════════════════════════════════════════
# 0. CONFIGURACIÓN AVANZADA (Multi-step routes, Ubicaciones, QC)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("0. CONFIGURACIÓN AVANZADA DEL SISTEMA")
print("═"*70)

# 0.1 Configurar almacén con 1 paso (simplificado)
print("\n" + "  0.1 Configurando Almacén (1 paso)...")
warehouse = search_read('stock.warehouse', [], ['id', 'name', 'reception_steps', 'delivery_steps', 'lot_stock_id'])
if warehouse:
    wh = warehouse[0]

    # Antes de cambiar a 1-step, vaciar ubicaciones intermedias
    if wh['reception_steps'] != 'one_step' or wh['delivery_steps'] != 'ship_only':
        # Buscar todas las ubicaciones intermedias del almacén que podrían tener stock
        intermediate_locs = search_read('stock.location', [
            '|', '|', '|', '|',
            ['name', 'ilike', 'Quality Control'],
            ['name', 'ilike', 'Input'],
            ['name', 'ilike', 'Output'],
            ['name', 'ilike', 'Pack'],
            ['name', 'ilike', 'Pick'],
        ], ['id', 'name'])

        for loc in intermediate_locs:
            quants = search('stock.quant', [
                ['location_id', '=', loc['id']],
                ['quantity', '!=', 0]
            ])

            if quants:
                print(f"      Vaciando {len(quants)} quants de {loc['name']}...")
                # Poner cantidades en cero para poder desactivar la ubicación
                write('stock.quant', quants, {'quantity': 0})

    if wh['reception_steps'] != 'one_step' or wh['delivery_steps'] != 'ship_only':
        write('stock.warehouse', [wh['id']], {
            'reception_steps': 'one_step',   # Recepción directa a Stock
            'delivery_steps': 'ship_only',   # Envío directo desde Stock
        })
        print(f"      ✓ Almacén {wh['name']}: one_step / ship_only")
    else:
        print(f"      - Almacén {wh['name']}: ya configurado")

# 0.2 Ubicaciones de subcontratista
print("\n" + "  0.2 Creando ubicaciones de subcontratista...")

# IMPORTANTE: Las ubicaciones de subcontratista deben ser hijas de "Subcontratación"
# para que la ruta "Subcontratista de reabastecimiento" funcione correctamente
subcontract_parent = search_read('stock.location', [['name', '=', 'Subcontratación']], ['id'])
if subcontract_parent:
    SUBCONTRACT_PARENT_ID = subcontract_parent[0]['id']
else:
    # Crear ubicación padre si no existe
    SUBCONTRACT_PARENT_ID = create('stock.location', {
        'name': 'Subcontratación',
        'usage': 'internal',
    })
print(f"      Ubicación padre 'Subcontratación': ID {SUBCONTRACT_PARENT_ID}")

SUBCONTRACT_LOCATIONS = {}
subcontract_locs = [
    ('CARP', 'Subcontract - Carpintería Hnos. García'),
    ('LUST', 'Subcontract - Lustres & Acabados'),
    ('META', 'Subcontract - Metalúrgica Precisión'),
    ('MARM', 'Subcontract - Marmolería Del Sur'),
    ('NEOL', 'Subcontract - Neolith Argentina'),
]
for code, name in subcontract_locs:
    # Buscar incluyendo archivadas (pueden haber sido archivadas en limpieza)
    existing = search_read('stock.location', [['name', '=', name], '|', ['active', '=', True], ['active', '=', False]], ['id', 'active'])
    if existing:
        loc_id = existing[0]['id']
        # Reactivar si estaba archivada y asegurar parent correcto
        write('stock.location', [loc_id], {'active': True, 'location_id': SUBCONTRACT_PARENT_ID})
        print(f"      ✓ {name}")
    else:
        loc_id = create('stock.location', {
            'name': name, 'usage': 'internal', 'location_id': SUBCONTRACT_PARENT_ID, 'barcode': code
        })
        print(f"      + {name}")
    SUBCONTRACT_LOCATIONS[code] = loc_id

# 0.2.1 Corregir jerarquía de ubicaciones para rutas Dropship/Resupply
# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTANTE: Odoo puede crear múltiples ubicaciones "Subcontratación" desconectadas.
# Las reglas de stock (Dropship, Resupply Subcontractor) deben apuntar a la misma
# ubicación padre que contiene las ubicaciones de los subcontratistas.
# Si no coinciden, el flujo de Dropship Subcontractor no funciona porque el código
# de _adjust_procure_method sube la jerarquía de ubicaciones y no encuentra las reglas.
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "  0.2.1 Corrigiendo jerarquía de ubicaciones para Dropship Subcontractor...")

# Verificar si la compañía tiene configurada una ubicación de subcontratación diferente
companies = search_read('res.company', [], ['id', 'name', 'subcontracting_location_id'])
for company in companies:
    company_sub_loc = company.get('subcontracting_location_id')
    if company_sub_loc and company_sub_loc[0] != SUBCONTRACT_PARENT_ID:
        # La compañía usa una ubicación diferente - actualizar
        print(f"      Compañía '{company['name']}': actualizando subcontracting_location_id")
        print(f"        [{company_sub_loc[0]}] → [{SUBCONTRACT_PARENT_ID}]")
        write('res.company', [company['id']], {'subcontracting_location_id': SUBCONTRACT_PARENT_ID})

        # También actualizar todas las reglas que usan la ubicación incorrecta
        old_loc_id = company_sub_loc[0]

        # Reglas con location_src_id incorrecto
        rules_src = search_read('stock.rule', [['location_src_id', '=', old_loc_id]], ['id', 'name'])
        for rule in rules_src:
            write('stock.rule', [rule['id']], {'location_src_id': SUBCONTRACT_PARENT_ID})
            print(f"      ✓ Regla '{rule['name']}': location_src_id corregido")

        # Reglas con location_dest_id incorrecto
        rules_dest = search_read('stock.rule', [['location_dest_id', '=', old_loc_id]], ['id', 'name'])
        for rule in rules_dest:
            write('stock.rule', [rule['id']], {'location_dest_id': SUBCONTRACT_PARENT_ID})
            print(f"      ✓ Regla '{rule['name']}': location_dest_id corregido")

        if not rules_src and not rules_dest:
            print(f"      (sin reglas que corregir)")
    elif company_sub_loc:
        print(f"      Compañía '{company['name']}': jerarquía correcta")
    else:
        # Configurar la ubicación si no está configurada
        print(f"      Compañía '{company['name']}': configurando subcontracting_location_id")
        write('res.company', [company['id']], {'subcontracting_location_id': SUBCONTRACT_PARENT_ID})

# 0.2.2 Corregir Picking Type "Dropship Subcontractor" (DSC)
# ═══════════════════════════════════════════════════════════════════════════════
# El Picking Type DSC debe tener default_location_dest_id apuntando a la misma
# ubicación padre (SUBCONTRACT_PARENT_ID) que contiene las ubicaciones específicas
# de los subcontratistas.
#
# Si usa una ubicación diferente, los pickings DSC irán a "Subcontratación" genérica
# en lugar de "Subcontratación/Subcontract - Lustrador" (ubicación específica).
#
# El código de purchase.py._get_destination_location() usa dest_address_id para
# obtener la ubicación específica del subcontratista, pero solo funciona si
# la ubicación padre es correcta.
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "  0.2.2 Corrigiendo Picking Type 'Dropship Subcontractor' (DSC)...")

dsc_picking_type = search_read('stock.picking.type', [['sequence_code', '=', 'DSC']],
    ['id', 'name', 'default_location_dest_id'])

if dsc_picking_type:
    pt = dsc_picking_type[0]
    current_dest = pt.get('default_location_dest_id')
    if current_dest and current_dest[0] != SUBCONTRACT_PARENT_ID:
        write('stock.picking.type', [pt['id']], {'default_location_dest_id': SUBCONTRACT_PARENT_ID})
        print(f"      ✓ Picking Type '{pt['name']}': default_location_dest_id corregido")
        print(f"        [{current_dest[0]}] → [{SUBCONTRACT_PARENT_ID}]")
    elif current_dest:
        print(f"      Picking Type '{pt['name']}': ubicación correcta")
    else:
        write('stock.picking.type', [pt['id']], {'default_location_dest_id': SUBCONTRACT_PARENT_ID})
        print(f"      ✓ Picking Type '{pt['name']}': default_location_dest_id configurado")
else:
    print("      (Picking Type DSC no encontrado - se creará con el módulo)")

# ═══════════════════════════════════════════════════════════════════════════════
# 1. DATOS BASE
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("1. CONFIGURANDO DATOS BASE")
print("═"*70)

# UoM
uom = search_read('uom.uom', [['name', 'ilike', 'unit']], ['id'], limit=1)
UOM_ID = uom[0]['id'] if uom else 1

# Rutas (incluyendo inactivas)
rutas = search_read('stock.route', ['|', ['active', '=', True], ['active', '=', False]], ['id', 'name', 'active'])
RUTA_MANUFACTURE = next((r['id'] for r in rutas if 'manufacture' in r['name'].lower()), None)
RUTA_BUY = next((r['id'] for r in rutas if 'buy' in r['name'].lower()), None)
RUTA_MTO = next((r['id'] for r in rutas if 'mto' in r['name'].lower() or 'replenish on order' in r['name'].lower()), None)
RUTA_RESUPPLY_SUBCONTRACTOR = next((r['id'] for r in rutas if 'subcontratista de reabastecimiento' in r['name'].lower()), None)
RUTA_DROPSHIP = next((r['id'] for r in rutas if r['name'].lower() == 'dropship'), None)

print(f"  UoM: {UOM_ID}")
print(f"  Ruta Manufacture: {RUTA_MANUFACTURE}")
print(f"  Ruta Buy: {RUTA_BUY}")
print(f"  Ruta MTO: {RUTA_MTO}")
print(f"  Ruta Resupply Subcontractor: {RUTA_RESUPPLY_SUBCONTRACTOR}")
print(f"  Ruta Dropship: {RUTA_DROPSHIP}")

# Activar y configurar rutas
if RUTA_MTO:
    write('stock.route', [RUTA_MTO], {'active': True, 'product_selectable': True})
    print("  + MTO activada y seleccionable")
if RUTA_BUY:
    write('stock.route', [RUTA_BUY], {'product_selectable': True})
if RUTA_MANUFACTURE:
    write('stock.route', [RUTA_MANUFACTURE], {'product_selectable': True})

# Categorías
print("\n" + "  Creando categorías...")
cat_all = search_read('product.category', [['name', '=', 'All']], ['id'])
CAT_PARENT = cat_all[0]['id'] if cat_all else 1

CATEGORIAS = {}
for cat_name in ['Mobiliario', 'Mesas', 'Tapas', 'Tapas Intermedias', 'Bases']:
    parent = CATEGORIAS.get('Mobiliario', CAT_PARENT) if cat_name != 'Mobiliario' else CAT_PARENT
    cat_id, created = get_or_create(
        'product.category',
        [['name', '=', cat_name]],
        {'name': cat_name, 'parent_id': parent}
    )
    CATEGORIAS[cat_name] = cat_id
    print(f"    {'+ Creada' if created else '- Existe'}: {cat_name}")

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PROVEEDORES
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("2. CREANDO PROVEEDORES")
print("═"*70)

PROVEEDOR_IDS = {}
for prov in PROVEEDORES:
    prov_id, created = get_or_create(
        'res.partner',
        [['name', '=', prov['name']]],
        {**prov, 'is_company': True, 'supplier_rank': 1}
    )
    PROVEEDOR_IDS[prov['name']] = prov_id
    print(f"  {'+ Creado' if created else '- Existe'}: {prov['name']}")

# Asociar ubicaciones de subcontratación a proveedores
print("\n" + "  Asociando ubicaciones de subcontratación...")
PROV_LOC_MAP = {
    'Carpintería Artesanal Hnos. García': 'CARP',
    'Lustres & Acabados Premium': 'LUST',
    'Metalúrgica Precisión S.A.': 'META',
    'Marmolería Del Sur': 'MARM',
    'Neolith Argentina': 'NEOL',
}
for prov_name, loc_code in PROV_LOC_MAP.items():
    if prov_name in PROVEEDOR_IDS and loc_code in SUBCONTRACT_LOCATIONS:
        write('res.partner', [PROVEEDOR_IDS[prov_name]], {
            'property_stock_subcontractor': SUBCONTRACT_LOCATIONS[loc_code]
        })
        print(f"    ✓ {prov_name[:30]} → {loc_code}")

# ═══════════════════════════════════════════════════════════════════════════════
# 3. CLIENTES
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("3. CREANDO CLIENTES")
print("═"*70)

CLIENTE_IDS = []
for cli in CLIENTES:
    cli_id, created = get_or_create(
        'res.partner',
        [['name', '=', cli['name']]],
        {**cli, 'is_company': True, 'customer_rank': 1}
    )
    CLIENTE_IDS.append(cli_id)
    print(f"  {'+ Creado' if created else '- Existe'}: {cli['name']}")

# ═══════════════════════════════════════════════════════════════════════════════
# 4. ATRIBUTOS DE PRODUCTO
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("4. CREANDO ATRIBUTOS DE PRODUCTO")
print("═"*70)

ATRIBUTOS = {}
ATTR_VALUES = {}

# Material Tapa
attr_id, _ = get_or_create('product.attribute', [['name', '=', 'Material Tapa']], {
    'name': 'Material Tapa', 'create_variant': 'always', 'display_type': 'radio'
})
ATRIBUTOS['Material Tapa'] = attr_id
print(f"  Material Tapa (ID: {attr_id})")

for mat in MATERIALES_TAPA:
    val_id, _ = get_or_create('product.attribute.value',
        [['name', '=', mat['nombre']], ['attribute_id', '=', attr_id]],
        {'name': mat['nombre'], 'attribute_id': attr_id}
    )
    ATTR_VALUES[f"Material Tapa|{mat['nombre']}"] = val_id
    print(f"      - {mat['nombre']}")

# Material Base
attr_id, _ = get_or_create('product.attribute', [['name', '=', 'Material Base']], {
    'name': 'Material Base', 'create_variant': 'always', 'display_type': 'radio'
})
ATRIBUTOS['Material Base'] = attr_id
print(f"  Material Base (ID: {attr_id})")

for mat in MATERIALES_BASE:
    val_id, _ = get_or_create('product.attribute.value',
        [['name', '=', mat['nombre']], ['attribute_id', '=', attr_id]],
        {'name': mat['nombre'], 'attribute_id': attr_id}
    )
    ATTR_VALUES[f"Material Base|{mat['nombre']}"] = val_id
    print(f"      - {mat['nombre']}")

# Medidas
attr_id, _ = get_or_create('product.attribute', [['name', '=', 'Medidas']], {
    'name': 'Medidas', 'create_variant': 'always', 'display_type': 'select'
})
ATRIBUTOS['Medidas'] = attr_id
print(f"  Medidas (ID: {attr_id})")

for med in MEDIDAS:
    val_id, _ = get_or_create('product.attribute.value',
        [['name', '=', med['nombre']], ['attribute_id', '=', attr_id]],
        {'name': med['nombre'], 'attribute_id': attr_id}
    )
    ATTR_VALUES[f"Medidas|{med['nombre']}"] = val_id
    print(f"      - {med['nombre']}")

# Terminación (para Tapas de madera y Mesa)
attr_id, _ = get_or_create('product.attribute', [['name', '=', 'Terminación']], {
    'name': 'Terminación', 'create_variant': 'always', 'display_type': 'radio'
})
ATRIBUTOS['Terminación'] = attr_id
print(f"  Terminación (ID: {attr_id})")

for term in TERMINACIONES:
    val_id, _ = get_or_create('product.attribute.value',
        [['name', '=', term['nombre']], ['attribute_id', '=', attr_id]],
        {'name': term['nombre'], 'attribute_id': attr_id}
    )
    ATTR_VALUES[f"Terminación|{term['nombre']}"] = val_id
    print(f"      - {term['nombre']}")

# Terminación para Mesa (incluye "Sin Terminación")
print(f"  Terminación Mesa (valores adicionales):")
for term in TERMINACIONES_MESA:
    val_id, _ = get_or_create('product.attribute.value',
        [['name', '=', term['nombre']], ['attribute_id', '=', attr_id]],
        {'name': term['nombre'], 'attribute_id': attr_id}
    )
    ATTR_VALUES[f"Terminación|{term['nombre']}"] = val_id
    if term['nombre'] == 'Sin Terminación':
        print(f"      + {term['nombre']} (para Mármol/Neolith)")

# ═══════════════════════════════════════════════════════════════════════════════
# 5. WORK CENTERS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("5. CREANDO WORK CENTERS")
print("═"*70)

WORK_CENTERS = {}

for wc in WORK_CENTERS_CONFIG:
    wc_id, created = get_or_create('mrp.workcenter',
        [['code', '=', wc['code']]],
        wc
    )
    WORK_CENTERS[wc['code']] = wc_id
    print(f"  {'+ Creado' if created else '- Existe'}: {wc['name']} ({wc['code']})")

# Configurar capacidades
print("\n" + "  Configurando capacidades...")

capacity_id, created = get_or_create('mrp.workcenter.capacity',
    [['workcenter_id', '=', WORK_CENTERS['ENSAM']], ['product_id', '=', False]],
    {
        'workcenter_id': WORK_CENTERS['ENSAM'],
        'product_id': False,
        'product_uom_id': UOM_ID,
        'capacity': 2,
        'time_start': 15,
        'time_stop': 10,
    }
)
print(f"    {'+ Creada' if created else '- Existe'}: Ensamble = 2 unidades")

capacity_id, created = get_or_create('mrp.workcenter.capacity',
    [['workcenter_id', '=', WORK_CENTERS['QC']], ['product_id', '=', False]],
    {
        'workcenter_id': WORK_CENTERS['QC'],
        'product_id': False,
        'product_uom_id': UOM_ID,
        'capacity': 5,
        'time_start': 5,
        'time_stop': 5,
    }
)
print(f"    {'+ Creada' if created else '- Existe'}: QC = 5 unidades")

# ═══════════════════════════════════════════════════════════════════════════════
# 6. BASES METÁLICAS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("6. CREANDO BASES METÁLICAS")
print("═"*70)

BASES = {}

for base_mat in MATERIALES_BASE:
    for medida in MEDIDAS:
        nombre = f"Base {base_mat['nombre']} {medida['codigo']}"
        codigo = f"BASE-{base_mat['codigo']}-{medida['codigo'].replace('x', '')}"
        costo = base_mat['costo_base'] * medida['factor_precio']

        # Rutas: Buy + MTO para reabastecimiento automático
        rutas_componente = [r for r in [RUTA_BUY, RUTA_MTO] if r]

        tmpl_id, created = get_or_create('product.template',
            [['default_code', '=', codigo]],
            {
                'name': nombre,
                'default_code': codigo,
                'is_storable': True,
                'categ_id': CATEGORIAS['Bases'],
                'list_price': costo * 1.5,
                'standard_price': costo,
                'uom_id': UOM_ID,
                'purchase_ok': True,
                'sale_ok': False,
                'route_ids': [(6, 0, rutas_componente)] if rutas_componente else [],
            }
        )

        variant = search_read('product.product', [['product_tmpl_id', '=', tmpl_id]], ['id'], limit=1)
        variant_id = variant[0]['id'] if variant else None
        BASES[(base_mat['nombre'], medida['codigo'])] = variant_id

        # Configurar proveedor (Metalúrgica)
        # NO crear BoM - las bases son compra directa sin subcontratación
        # (el proveedor no necesita componentes nuestros)
        prov_id = PROVEEDOR_IDS.get('Metalúrgica Precisión S.A.')
        if prov_id:
            get_or_create('product.supplierinfo',
                [['product_tmpl_id', '=', tmpl_id], ['partner_id', '=', prov_id]],
                {'partner_id': prov_id, 'product_tmpl_id': tmpl_id, 'price': costo, 'delay': base_mat['lead_time']}
            )

        print(f"  {'+ Creada' if created else '- Existe'}: {nombre}")

# ═══════════════════════════════════════════════════════════════════════════════
# 7. TAPAS MÁRMOL Y NEOLITH
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("7. CREANDO TAPAS MÁRMOL Y NEOLITH")
print("═"*70)

TAPAS_SIMPLES = {}

for mat in MATERIALES_TAPA:
    if mat['requiere_terminacion']:
        continue

    for medida in MEDIDAS:
        nombre = f"Tapa {mat['nombre']} {medida['codigo']}"
        codigo = f"TAPA-{mat['codigo']}-{medida['codigo'].replace('x', '')}"
        costo = mat['costo_base'] * medida['factor_precio']

        # Rutas: Buy + MTO
        rutas_componente = [r for r in [RUTA_BUY, RUTA_MTO] if r]

        tmpl_id, created = get_or_create('product.template',
            [['default_code', '=', codigo]],
            {
                'name': nombre,
                'default_code': codigo,
                'is_storable': True,
                'categ_id': CATEGORIAS['Tapas'],
                'list_price': costo * 1.5,
                'standard_price': costo,
                'uom_id': UOM_ID,
                'purchase_ok': True,
                'sale_ok': False,
                'route_ids': [(6, 0, rutas_componente)] if rutas_componente else [],
            }
        )

        # Asegurar rutas si ya existe
        if not created and rutas_componente:
            write('product.template', [tmpl_id], {'route_ids': [(6, 0, rutas_componente)]})

        variant = search_read('product.product', [['product_tmpl_id', '=', tmpl_id]], ['id'], limit=1)
        variant_id = variant[0]['id'] if variant else None
        TAPAS_SIMPLES[(mat['nombre'], medida['codigo'])] = variant_id

        # Configurar proveedor
        prov_id = PROVEEDOR_IDS.get(mat['proveedor'])
        if prov_id:
            get_or_create('product.supplierinfo',
                [['product_tmpl_id', '=', tmpl_id], ['partner_id', '=', prov_id]],
                {'partner_id': prov_id, 'product_tmpl_id': tmpl_id, 'price': costo, 'delay': mat['lead_time']}
            )

        print(f"  {'+ Creada' if created else '- Existe'}: {nombre}")

# ═══════════════════════════════════════════════════════════════════════════════
# 8. TAPAS DE MADERA CON TERMINACIÓN
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("8. CREANDO TAPAS DE MADERA (flujo con terminación)")
print("═"*70)

mat_madera = next(m for m in MATERIALES_TAPA if m['requiere_terminacion'])

# 8.1 Tapas SIN terminar (componente para Lustrador)
# ═══════════════════════════════════════════════════════════════════════════════
# FLUJO DROPSHIP DIRECTO: Carpintería → Lustrador (1 paso)
#
# La ruta "Dropship" configura automáticamente el flujo:
# 1. Cuando se confirma PO al Lustrador, se crea Subcontract MO
# 2. El Subcontract MO necesita componentes (Tapa Sin Terminar)
# 3. Gracias a la ruta Dropship, se genera PO a Carpintería automáticamente
# 4. El picking es DSC (Dropship Subcontractor): Vendors → Subcontratación
#    Va DIRECTO al Lustrador sin pasar por Stock
# 5. La PO a Carpintería queda vinculada al origen (Lustrador/SO)
#
# IMPORTANTE:
# - Solo usar ruta Dropship (sin MTO)
# - Si se agrega MTO, la regla "Stock → Subcontratación" tiene prioridad
#   y el flujo pasa por Stock (2 pasos) en lugar de ir directo (1 paso)
# - Las ubicaciones de subcontratación deben estar correctamente
#   jerarquizadas (ver sección 0.2.1)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "  8.1 Tapas SIN terminar (componente para Lustrador - Dropship):")
TAPAS_SIN_TERMINAR = {}

for medida in MEDIDAS:
    nombre = f"Tapa Madera Sin Terminar {medida['codigo']}"
    codigo = f"TAPA-MADERA-RAW-{medida['codigo'].replace('x', '')}"
    costo = mat_madera['costo_base'] * medida['factor_precio']

    # Rutas: SOLO Dropship (sin MTO)
    # La ruta Dropship tiene regla "Vendors → Subcontratación" con procure_method: mts_else_mto
    # que ya maneja "si no hay stock, crear orden de compra"
    # Si se agrega MTO, la regla "Stock → Subcontratación" de MTO tiene prioridad
    # y el flujo pasa por Stock en lugar de ir directo
    rutas_componente = [RUTA_DROPSHIP] if RUTA_DROPSHIP else []

    tmpl_id, created = get_or_create('product.template',
        [['default_code', '=', codigo]],
        {
            'name': nombre,
            'default_code': codigo,
            'is_storable': True,
            'categ_id': CATEGORIAS['Tapas Intermedias'],
            'list_price': costo,
            'standard_price': costo,
            'uom_id': UOM_ID,
            'purchase_ok': True,
            'sale_ok': False,
            'route_ids': [(6, 0, rutas_componente)] if rutas_componente else [],
        }
    )

    # Asegurar rutas si ya existe
    if not created and rutas_componente:
        write('product.template', [tmpl_id], {'route_ids': [(6, 0, rutas_componente)]})

    variant = search_read('product.product', [['product_tmpl_id', '=', tmpl_id]], ['id'], limit=1)
    variant_id = variant[0]['id'] if variant else None
    TAPAS_SIN_TERMINAR[medida['codigo']] = {'tmpl_id': tmpl_id, 'variant_id': variant_id, 'costo': costo}

    # Configurar proveedor (Carpintería)
    prov_id = PROVEEDOR_IDS.get(mat_madera['proveedor'])
    if prov_id:
        get_or_create('product.supplierinfo',
            [['product_tmpl_id', '=', tmpl_id], ['partner_id', '=', prov_id]],
            {'partner_id': prov_id, 'product_tmpl_id': tmpl_id, 'price': costo, 'delay': mat_madera['lead_time']}
        )

    print(f"      {'+ Creada' if created else '- Existe'}: {nombre}")

# 8.2 Tapas CON terminación
print("\n" + "  8.2 Tapas CON terminación (subcontratación a Lustrador):")
TAPAS_TERMINADAS = {}

lustrador_id = PROVEEDOR_IDS.get(mat_madera['proveedor_terminacion'])

# Rutas: Buy + MTO para reabastecimiento automático
rutas_componente = [r for r in [RUTA_BUY, RUTA_MTO] if r]

for medida in MEDIDAS:
    nombre_base = f"Tapa Madera Terminada {medida['codigo']}"
    codigo_base = f"TAPA-MADERA-TERM-{medida['codigo'].replace('x', '')}"
    costo_terminacion_promedio = 90000
    precio_terminada = (mat_madera['costo_base'] + costo_terminacion_promedio) * medida['factor_precio']

    existing = search_read('product.template', [['default_code', '=', codigo_base]], ['id'])

    if existing:
        tmpl_id = existing[0]['id']
        print(f"      - Existe: {nombre_base}")
        # Asegurar rutas Buy + MTO
        write('product.template', [tmpl_id], {
            'route_ids': [(6, 0, rutas_componente)],
            'purchase_ok': True,  # Necesario para generar PO
        })
    else:
        tmpl_id = create('product.template', {
            'name': nombre_base,
            'default_code': codigo_base,
            'is_storable': True,
            'categ_id': CATEGORIAS['Tapas'],
            'list_price': precio_terminada,
            'standard_price': (mat_madera['costo_base'] + 60000) * medida['factor_precio'],
            'uom_id': UOM_ID,
            'purchase_ok': True,  # Necesario para generar PO automática
            'sale_ok': False,
            'route_ids': [(6, 0, rutas_componente)] if rutas_componente else [],
        })

        term_values = [ATTR_VALUES[f"Terminación|{t['nombre']}"] for t in TERMINACIONES]
        create('product.template.attribute.line', {
            'product_tmpl_id': tmpl_id,
            'attribute_id': ATRIBUTOS['Terminación'],
            'value_ids': [(6, 0, term_values)],
        })
        print(f"      + Creada: {nombre_base} ({len(TERMINACIONES)} variantes)")

    # IMPORTANTE: Configurar proveedor (Lustrador) para PO automática
    if lustrador_id:
        get_or_create('product.supplierinfo',
            [['product_tmpl_id', '=', tmpl_id], ['partner_id', '=', lustrador_id]],
            {
                'partner_id': lustrador_id,
                'product_tmpl_id': tmpl_id,
                'price': precio_terminada,
                'delay': mat_madera['lead_time_terminacion']
            }
        )

    # Obtener variantes y crear BoMs
    variantes = search_read('product.product',
        [['product_tmpl_id', '=', tmpl_id]],
        ['id', 'display_name', 'product_template_variant_value_ids']
    )

    tapa_sin_terminar = TAPAS_SIN_TERMINAR[medida['codigo']]

    for var in variantes:
        var_values = search_read('product.template.attribute.value',
            [['id', 'in', var['product_template_variant_value_ids']]],
            ['name']
        )
        terminacion = var_values[0]['name'] if var_values else 'Unknown'
        TAPAS_TERMINADAS[(medida['codigo'], terminacion)] = var['id']

        existing_bom = search_read('mrp.bom',
            [['product_id', '=', var['id']], ['type', '=', 'subcontract']],
            ['id']
        )

        if not existing_bom and lustrador_id:
            bom_id = create('mrp.bom', {
                'product_tmpl_id': tmpl_id,
                'product_id': var['id'],
                'product_qty': 1,
                'type': 'subcontract',
                'subcontractor_ids': [(6, 0, [lustrador_id])],
                'produce_delay': mat_madera['lead_time_terminacion'],
            })

            create('mrp.bom.line', {
                'bom_id': bom_id,
                'product_id': tapa_sin_terminar['variant_id'],
                'product_qty': 1,
            })
            print(f"        -> BoM subcontratación: {terminacion}")

# ═══════════════════════════════════════════════════════════════════════════════
# 9. MESA COMEDOR PREMIUM
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("9. CREANDO MESA COMEDOR PREMIUM")
print("═"*70)

MESA_NOMBRE = "Mesa Comedor Premium"
MESA_CODIGO = "MESA-COMEDOR"

existing_mesa = search_read('product.template', [['default_code', '=', MESA_CODIGO]], ['id'])

if existing_mesa:
    mesa_tmpl_id = existing_mesa[0]['id']
    print(f"  - Mesa ya existe (ID: {mesa_tmpl_id})")
else:
    # Rutas: Manufacture + MTO para fabricación bajo pedido
    rutas_mesa = [r for r in [RUTA_MANUFACTURE, RUTA_MTO] if r]

    mesa_tmpl_id = create('product.template', {
        'name': MESA_NOMBRE,
        'default_code': MESA_CODIGO,
        'is_storable': True,
        'categ_id': CATEGORIAS['Mesas'],
        'list_price': 2250000,
        'uom_id': UOM_ID,
        'purchase_ok': False,
        'sale_ok': True,
        'route_ids': [(6, 0, rutas_mesa)] if rutas_mesa else [],
        'sale_delay': 14,  # Lead time de entrega al cliente
        'description_sale': 'Mesa de comedor premium. Seleccione material de tapa, base y medidas.',
    })
    print(f"  + Mesa creada (ID: {mesa_tmpl_id})")

    # Orden de atributos: Material Tapa → Terminación → Material Base → Medidas
    atributos_orden = [
        ('Material Tapa', 10),
        ('Terminación', 20),
        ('Material Base', 30),
        ('Medidas', 40),
    ]

    for attr_name, sequence in atributos_orden:
        attr_id = ATRIBUTOS[attr_name]
        if attr_name == 'Terminación':
            values = [ATTR_VALUES[f"Terminación|{t['nombre']}"] for t in TERMINACIONES_MESA]
        else:
            values = [v for k, v in ATTR_VALUES.items() if k.startswith(f"{attr_name}|")]
        create('product.template.attribute.line', {
            'product_tmpl_id': mesa_tmpl_id,
            'attribute_id': attr_id,
            'value_ids': [(6, 0, values)],
            'sequence': sequence,
        })
        print(f"    -> Atributo: {attr_name} (seq: {sequence})")

# Asegurar rutas Manufacture + MTO (fabricación bajo pedido)
rutas_mesa = [r for r in [RUTA_MANUFACTURE, RUTA_MTO] if r]
write('product.template', [mesa_tmpl_id], {
    'route_ids': [(6, 0, rutas_mesa)] if rutas_mesa else [],
    'sale_delay': 14,
})

mesa_variantes = search_read('product.product',
    [['product_tmpl_id', '=', mesa_tmpl_id]],
    ['id', 'display_name', 'product_template_variant_value_ids']
)
print(f"\n  Total variantes de Mesa: {len(mesa_variantes)}")

# ═══════════════════════════════════════════════════════════════════════════════
# 9.1 EXCLUSIONES DE ATRIBUTOS (Terminación solo visible para Madera)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "  Configurando exclusiones de atributos...")

# Obtener los product.template.attribute.value (PTAV) para Mesa
mesa_ptavs = search_read('product.template.attribute.value',
    [['product_tmpl_id', '=', mesa_tmpl_id]],
    ['id', 'name', 'attribute_id', 'product_attribute_value_id']
)

# Mapear PTAV por nombre de atributo|valor
ptav_map = {}
for ptav in mesa_ptavs:
    attr_name = ptav['attribute_id'][1] if ptav['attribute_id'] else ''
    key = f"{attr_name}|{ptav['name']}"
    ptav_map[key] = ptav['id']

# Definir exclusiones:
# - Mármol/Neolith excluyen terminaciones con lustre
# - Madera excluye "Sin Terminación"
exclusiones = [
    # Material Tapa -> excluye estas Terminaciones
    ('Material Tapa|Mármol Carrara', ['Terminación|Lustre Mate', 'Terminación|Lustre Brillante', 'Terminación|Natural']),
    ('Material Tapa|Neolith Negro', ['Terminación|Lustre Mate', 'Terminación|Lustre Brillante', 'Terminación|Natural']),
    ('Material Tapa|Madera Paraíso', ['Terminación|Sin Terminación']),
]

exclusiones_creadas = 0
for material_key, terminaciones_excluir in exclusiones:
    material_ptav_id = ptav_map.get(material_key)
    if not material_ptav_id:
        continue

    # Obtener IDs de terminaciones a excluir
    term_ids = [ptav_map.get(t) for t in terminaciones_excluir if ptav_map.get(t)]
    if not term_ids:
        continue

    # Verificar si ya existe esta exclusión
    existing = search_read('product.template.attribute.exclusion',
        [['product_tmpl_id', '=', mesa_tmpl_id],
         ['product_template_attribute_value_id', '=', material_ptav_id]],
        ['id', 'value_ids']
    )

    if existing:
        # Actualizar exclusión existente
        write('product.template.attribute.exclusion', [existing[0]['id']], {
            'value_ids': [(6, 0, term_ids)]
        })
    else:
        # Crear nueva exclusión
        create('product.template.attribute.exclusion', {
            'product_tmpl_id': mesa_tmpl_id,
            'product_template_attribute_value_id': material_ptav_id,
            'value_ids': [(6, 0, term_ids)],
        })
    exclusiones_creadas += 1

print(f"    -> {exclusiones_creadas} exclusiones configuradas")
print("    -> Mármol/Neolith: solo 'Sin Terminación' disponible")
print("    -> Madera: solo terminaciones de lustre disponibles")

# ═══════════════════════════════════════════════════════════════════════════════
# 10. BoMs PARA MESA
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("10. CREANDO BoMs PARA VARIANTES DE MESA")
print("═"*70)

boms_creadas = 0

for variante in mesa_variantes:
    existing_bom = search_read('mrp.bom', [['product_id', '=', variante['id']]], ['id'])
    if existing_bom:
        continue

    var_values = search_read('product.template.attribute.value',
        [['id', 'in', variante['product_template_variant_value_ids']]],
        ['name', 'attribute_id']
    )

    material_tapa = None
    material_base = None
    medida_codigo = None
    terminacion = None

    for vv in var_values:
        attr = search_read('product.attribute', [['id', '=', vv['attribute_id'][0]]], ['name'])[0]
        if attr['name'] == 'Material Tapa':
            material_tapa = vv['name']
        elif attr['name'] == 'Material Base':
            material_base = vv['name']
        elif attr['name'] == 'Medidas':
            medida_codigo = vv['name'].replace(' cm', '')
        elif attr['name'] == 'Terminación':
            terminacion = vv['name']

    if not all([material_tapa, material_base, medida_codigo, terminacion]):
        continue

    # Validar combinación válida:
    # - Madera + Lustre/Natural = OK
    # - Madera + Sin Terminación = SKIP (combinación no válida)
    # - Mármol/Neolith + Sin Terminación = OK
    # - Mármol/Neolith + Lustre/Natural = SKIP (combinación no válida)
    es_madera = (material_tapa == 'Madera Paraíso')
    es_terminacion_lustre = (terminacion != 'Sin Terminación')

    if es_madera and not es_terminacion_lustre:
        continue  # Madera sin terminación no es válida
    if not es_madera and es_terminacion_lustre:
        continue  # Mármol/Neolith con lustre no es válida

    # Determinar componente tapa según material y terminación
    if material_tapa == 'Madera Paraíso':
        # Madera usa la tapa terminada con el lustre seleccionado
        tapa_id = TAPAS_TERMINADAS.get((medida_codigo, terminacion))
    else:
        # Mármol/Neolith usa tapa simple (sin terminación)
        tapa_id = TAPAS_SIMPLES.get((material_tapa, medida_codigo))

    base_id = BASES.get((material_base, medida_codigo))

    if not tapa_id or not base_id:
        print(f"  ! Componentes no encontrados: {variante['display_name'][:50]}")
        continue

    bom_id = create('mrp.bom', {
        'product_tmpl_id': mesa_tmpl_id,
        'product_id': variante['id'],
        'product_qty': 1,
        'type': 'normal',
        'produce_delay': 1,
        'days_to_prepare_mo': 2,
    })

    create('mrp.bom.line', {'bom_id': bom_id, 'product_id': tapa_id, 'product_qty': 1})
    create('mrp.bom.line', {'bom_id': bom_id, 'product_id': base_id, 'product_qty': 1})

    # Agregar operaciones
    for op in OPERACIONES_MESA:
        wc_id = WORK_CENTERS.get(op['workcenter_code'])
        if wc_id:
            create('mrp.routing.workcenter', {
                'bom_id': bom_id,
                'name': op['name'],
                'workcenter_id': wc_id,
                'time_mode': 'manual',
                'time_cycle_manual': op['time_cycle_manual'],
                'sequence': op['sequence'],
            })

    boms_creadas += 1

print(f"  + {boms_creadas} BoMs creadas con operaciones")

# ═══════════════════════════════════════════════════════════════════════════════
# 11. OPERACIONES PARA TAPAS DE MADERA
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("11. AGREGANDO OPERACIONES A TAPAS DE MADERA")
print("═"*70)

tapa_boms = search_read('mrp.bom',
    [['product_tmpl_id.name', 'ilike', 'Tapa Madera Terminada%'], ['type', '=', 'subcontract']],
    ['id', 'product_id']
)

ops_creadas = 0
for bom in tapa_boms:
    existing_ops = search_read('mrp.routing.workcenter', [['bom_id', '=', bom['id']]], ['id'])
    if existing_ops:
        continue

    for op in OPERACIONES_LUSTRADO:
        wc_id = WORK_CENTERS.get(op['workcenter_code'])
        if wc_id:
            create('mrp.routing.workcenter', {
                'bom_id': bom['id'],
                'name': op['name'],
                'workcenter_id': wc_id,
                'time_mode': 'manual',
                'time_cycle_manual': op['time_cycle_manual'],
                'sequence': op['sequence'],
            })
    ops_creadas += 1

print(f"  + {ops_creadas} BoMs de tapas con operaciones")

# Configurar todas las BoMs con consumo estricto y disponibilidad requerida
all_boms = search('mrp.bom', [])
if all_boms:
    write('mrp.bom', all_boms, {
        'consumption': 'strict',
        'ready_to_produce': 'asap',  # MO lista cuando componentes de 1ra operación están disponibles
    })
    print(f"  + {len(all_boms)} BoMs: consumo estricto + ready_to_produce=asap")

# ═══════════════════════════════════════════════════════════════════════════════
# 12. CONTROL DE CALIDAD EN DROPSHIP SUBCONTRACTOR
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("12. CONTROL DE CALIDAD (DSC - Dropship Subcontractor)")
print("═"*70)

# Buscar Picking Type DSC (Dropship Subcontractor)
dsc_picking_type = search_read('stock.picking.type', [
    ['sequence_code', '=', 'DSC']
], ['id', 'name'])

# Buscar productos Tapa Madera Sin Terminar
tapas_sin_terminar = search_read('product.product', [
    ['name', 'ilike', 'Tapa Madera Sin Terminar%']
], ['id', 'name'])

# Buscar test type Pass/Fail
passfail_type = search('quality.point.test_type', [['technical_name', '=', 'passfail']])

if dsc_picking_type and tapas_sin_terminar and passfail_type:
    dsc_pt_id = dsc_picking_type[0]['id']
    product_ids = [t['id'] for t in tapas_sin_terminar]

    qc_id, created = get_or_create('quality.point',
        [['name', '=', 'QC - Recepción Tapa Madera (DSC)']],
        {
            'name': 'QC - Recepción Tapa Madera (DSC)',
            'title': 'Control de Calidad - Tapa Madera Sin Terminar',
            'picking_type_ids': [(6, 0, [dsc_pt_id])],
            'product_ids': [(6, 0, product_ids)],
            'test_type_id': passfail_type[0],
            'measure_on': 'move_line',
            'note': '''<p><strong>Control de calidad al recibir Tapa Madera en el Lustrador:</strong></p>
<p>Verificar la tapa de madera SIN terminar antes de aceptar el envío.</p>
<ul>
    <li>Dimensiones correctas (180x90 o 220x100)</li>
    <li>Calidad de la madera (sin nudos, grietas)</li>
    <li>Humedad adecuada (&lt;12%)</li>
    <li>Sin defectos visibles</li>
    <li>Corte y cepillado correctos</li>
</ul>
<p><strong>Si NO pasa el QC, rechazar el envío.</strong></p>''',
        }
    )
    if created:
        print(f"  + QC - Recepción Tapa Madera (DSC) creado")
        print(f"    → Aplica al Picking Type: Dropship Subcontractor (DSC)")
        print(f"    → Productos: {len(tapas_sin_terminar)} tapas sin terminar")
    else:
        # Actualizar para asegurar configuración correcta
        write('quality.point', [qc_id], {
            'picking_type_ids': [(6, 0, [dsc_pt_id])],
            'product_ids': [(6, 0, product_ids)],
        })
        print(f"  ✓ QC - Recepción Tapa Madera (DSC) actualizado")
else:
    print("  ! No se pudo crear QC (faltan datos)")
    if not dsc_picking_type:
        print("    - Falta Picking Type DSC")
    if not tapas_sin_terminar:
        print("    - Faltan productos Tapa Madera Sin Terminar")
    if not passfail_type:
        print("    - Falta test type Pass/Fail")

# ═══════════════════════════════════════════════════════════════════════════════
# 13. ORDEN DE DEMO (MTO genera MO y POs automáticamente)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("13. CREANDO ORDEN DE DEMO (FLUJO AUTOMÁTICO MTO)")
print("═"*70)

# Buscar variante de madera CON terminación Lustre Mate
mesa_madera = None
for var in mesa_variantes:
    # Buscar variante: Madera Paraíso + cualquier base + cualquier medida + Lustre Mate
    if 'Madera' in var['display_name'] and 'Lustre Mate' in var['display_name']:
        mesa_madera = var
        break

DEMO_SO_NAME = None
DEMO_MO_NAME = None
DEMO_POS = []

if mesa_madera:
    so_id, created = get_or_create('sale.order',
        [['client_order_ref', '=', 'DEMO-MUEBLERIA-001']],
        {
            'partner_id': CLIENTE_IDS[0],
            'client_order_ref': 'DEMO-MUEBLERIA-001',
        }
    )

    if created:
        create('sale.order.line', {
            'order_id': so_id,
            'product_id': mesa_madera['id'],
            'product_uom_qty': 2,
        })
        so_data = search_read('sale.order', [['id', '=', so_id]], ['name'])[0]
        DEMO_SO_NAME = so_data['name']
        print(f"  + Cotización: {DEMO_SO_NAME}")
        print(f"    Producto: {mesa_madera['display_name'][:50]}...")

        # Confirmar venta - MTO genera MO automáticamente
        execute('sale.order', 'action_confirm', [[so_id]])
        print(f"    Estado: sale (confirmada)")

        # Buscar MO generada automáticamente por MTO
        time.sleep(1)  # Dar tiempo a Odoo para procesar

        mos = search_read('mrp.production',
            [['origin', 'ilike', DEMO_SO_NAME]],
            ['id', 'name', 'state', 'move_raw_ids', 'workorder_ids']
        )

        if mos:
            mo = mos[0]
            DEMO_MO_NAME = mo['name']
            print(f"\n  + MO generada automáticamente: {DEMO_MO_NAME}")
            print(f"    Estado: {mo['state']}")

            # Confirmar MO - esto dispara POs automáticamente vía MTO
            if mo['state'] == 'draft':
                execute('mrp.production', 'action_confirm', [[mo['id']]])
                mo = search_read('mrp.production', [['id', '=', mo['id']]],
                    ['state', 'workorder_ids'])[0]
                print(f"    Estado después de confirmar: {mo['state']}")

            print(f"    Work Orders: {len(mo.get('workorder_ids', []))}")

            # Buscar POs generadas automáticamente
            time.sleep(1)
            pos = search_read('purchase.order',
                [['origin', 'ilike', DEMO_MO_NAME]],
                ['name', 'partner_id', 'state']
            )

            if pos:
                print(f"\n  Órdenes de Compra generadas automáticamente:")
                for po in pos:
                    print(f"    + {po['name']}: {po['partner_id'][1]} ({po['state']})")
                    DEMO_POS.append(po['name'])
            else:
                print(f"\n  ! No se generaron POs automáticamente")
                print(f"    Verificar configuración de rutas MTO + Buy en componentes")
        else:
            print(f"\n  ! No se generó MO automáticamente")
            print(f"    Verificar ruta MTO + Manufacture en Mesa")
    else:
        so_data = search_read('sale.order', [['id', '=', so_id]], ['name'])[0]
        DEMO_SO_NAME = so_data['name']
        print(f"  - Cotización ya existe: {DEMO_SO_NAME}")

# ═══════════════════════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("SETUP COMPLETADO")
print("═"*70)

total_boms = len(search('mrp.bom', []))
total_wcs = len(search('mrp.workcenter', []))
total_ops = len(search('mrp.routing.workcenter', []))

print(f"""
  CONFIGURACIÓN AVANZADA:
  ────────────────────────────────────────────────────────────────────
  Almacén: 1 paso (one_step / ship_only)
  Ubicaciones Subcontratista: 5 (por proveedor)
  Dropship Subcontractor: Habilitado (DSC Picking Type configurado)
  Control de Calidad: QC en validación de DSC Picking

  PRODUCTOS:
  ────────────────────────────────────────────────────────────────────
  Mesa Comedor Premium: {len(mesa_variantes)} variantes
    (3 materiales tapa x 2 bases x 2 medidas x 4 terminaciones)
    Combinaciones válidas con BoM:
    - Mármol/Neolith + Sin Terminación: 8 variantes
    - Madera + Lustre (Mate/Brillante/Natural): 12 variantes

  Tapas Mármol/Neolith: 4 productos
  Tapas Madera Sin Terminar: 2 productos (Dropship a Lustrador)
  Tapas Madera Terminadas: 6 variantes (subcontratación)
  Bases Metálicas: 4 productos

  RUTAS:
  ────────────────────────────────────────────────────────────────────
  Mesa:                  Manufacture + MTO
  Bases:                 Buy + MTO
  Tapas Simples:         Buy + MTO
  Tapas Madera:          Buy + MTO
  Tapa Sin Terminar:     Dropship (envío directo a Lustrador)

  FLUJO DROPSHIP SUBCONTRACTOR (Madera):
  ────────────────────────────────────────────────────────────────────
  SO → MO Mesa → PO Lustrador (subcontratación)
                            ↓ (confirmar PO)
                 Subcontract MO (necesita Tapa Sin Terminar)
                            ↓ (ruta Dropship)
                 PO Carpintería → DSC Picking → Lustrador

  SELECCIÓN DE TERMINACIÓN:
  ────────────────────────────────────────────────────────────────────
  Al crear una venta de Mesa, el usuario puede elegir:
  - Material Tapa: Mármol Carrara, Neolith Negro, Madera Paraíso
  - Material Base: Acero Negro, Acero Dorado
  - Medidas: 180x90 cm, 220x100 cm
  - Terminación: Sin Terminación (para Mármol/Neolith)
                 Lustre Mate, Lustre Brillante, Natural (para Madera)

  PLANIFICACIÓN:
  ────────────────────────────────────────────────────────────────────
  Work Centers: {total_wcs}
    - Lustrado y Acabados (LUST) - Subcontratista
    - Ensamble Final (ENSAM) - Capacidad: 2 uds
    - Control de Calidad (QC) - Capacidad: 5 uds

  Operaciones: {total_ops}
    Mesa: 3 operaciones (ENSAM -> QC -> ENSAM)
    Tapa Terminada: 3 operaciones (LUST -> LUST -> QC)

  LEAD TIMES:
  ────────────────────────────────────────────────────────────────────
  | Proceso                | Lead Time |
  |------------------------|-----------|
  | Carpintería (madera)   | 5 días    |
  | Lustrador (terminación)| 3 días    |
  | Marmolería             | 7 días    |
  | Metalúrgica            | 5 días    |
  | Neolith                | 10 días   |
  | Ensamble Mesa          | 1 día     |
  | Entrega al cliente     | 14 días   |

  FLUJO DE MADERA (Dropship Subcontractor):
  ────────────────────────────────────────────────────────────────────

  ┌─────────────────┐                      ┌─────────────────────┐     ┌─────────────────┐
  │   CARPINTERÍA   │   Picking: DSC       │     LUSTRADOR       │     │     STOCK       │
  │   Hnos. García  │═════════════════════>│  Lustres & Acabados │────>│   Disponible    │
  │                 │   (dropship + QC)    │                     │     │                 │
  │   Tapa Madera   │                      │   (produce Tapa     │     │   (Tapa         │
  │   SIN Terminar  │   QC al validar →    │    Terminada)       │     │    Terminada)   │
  │                 │   Pass/Fail          │                     │     │                 │
  └─────────────────┘                      └─────────────────────┘     └─────────────────┘

  ════════════════════════════════════════════════════════════════════

  ORDEN DE DEMO:
  ────────────────────────────────────────────────────────────────────
  Cotización: {DEMO_SO_NAME or 'N/A'}
  MO:         {DEMO_MO_NAME or 'N/A'} (generada automáticamente)
  POs:        {', '.join(DEMO_POS) if DEMO_POS else 'Pendiente confirmar MO'}

  ════════════════════════════════════════════════════════════════════

  URLS PARA VERIFICAR:
  ────────────────────────────────────────────────────────────────────
  Productos:     {ODOO_URL}/odoo/product-template
  BoMs:          {ODOO_URL}/odoo/mrp-bom
  Work Centers:  {ODOO_URL}/odoo/mrp-workcenter
  Gantt:         {ODOO_URL}/odoo/mrp-production?view_type=gantt
  Work Orders:   {ODOO_URL}/odoo/mrp-workorder
  Compras:       {ODOO_URL}/odoo/purchase-order
  Ventas:        {ODOO_URL}/odoo/sale-order
  Quality:       {ODOO_URL}/odoo/quality-point
  Ubicaciones:   {ODOO_URL}/odoo/stock-location

  ════════════════════════════════════════════════════════════════════
""")
