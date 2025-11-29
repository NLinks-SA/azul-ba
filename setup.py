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

FLUJO DE MADERA:
Carpintería (compra) → Lustrador (subcontratación) → Tapa Terminada → Mesa

USO:
    python setup_demo_completo.py [--limpiar]

    --limpiar: Archiva productos existentes antes de crear nuevos
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
    {'nombre': 'Lustre Mate', 'costo_adicional': 60},
    {'nombre': 'Lustre Brillante', 'costo_adicional': 80},
    {'nombre': 'Natural', 'costo_adicional': 40},
]

MATERIALES_TAPA = [
    {
        'nombre': 'Mármol Carrara',
        'codigo': 'MARMOL',
        'costo_base': 450,
        'proveedor': 'Marmolería Del Sur',
        'requiere_terminacion': False,
        'lead_time': 7,
    },
    {
        'nombre': 'Neolith Negro',
        'codigo': 'NEOLITH',
        'costo_base': 520,
        'proveedor': 'Neolith Argentina',
        'requiere_terminacion': False,
        'lead_time': 10,
    },
    {
        'nombre': 'Madera Paraíso',
        'codigo': 'MADERA',
        'costo_base': 200,
        'proveedor': 'Carpintería Artesanal Hnos. García',
        'requiere_terminacion': True,
        'proveedor_terminacion': 'Lustres & Acabados Premium',
        'lead_time': 5,
        'lead_time_terminacion': 3,
    },
]

MATERIALES_BASE = [
    {'nombre': 'Acero Negro', 'codigo': 'NEGRO', 'costo_base': 180, 'lead_time': 5},
    {'nombre': 'Acero Dorado', 'codigo': 'DORADO', 'costo_base': 250, 'lead_time': 5},
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

WORK_CENTERS_CONFIG = [
    {
        'name': 'Carpintería Externa',
        'code': 'CARP',
        'time_efficiency': 100,
        'time_start': 30,
        'time_stop': 15,
        'color': 1,
        'note': '<p><strong>Proveedor:</strong> Carpintería Artesanal Hnos. García</p><p><strong>Lead Time:</strong> 5 días hábiles</p><p><strong>Especialidad:</strong> Tapas de madera sin terminar</p>',
    },
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
        'name': 'Marmolería Externa',
        'code': 'MARM',
        'time_efficiency': 100,
        'time_start': 60,
        'time_stop': 30,
        'color': 3,
        'note': '<p><strong>Proveedor:</strong> Marmolería Del Sur</p><p><strong>Lead Time:</strong> 7 días hábiles</p><p><strong>Especialidad:</strong> Corte y pulido de mármol</p>',
    },
    {
        'name': 'Metalurgia Externa',
        'code': 'META',
        'time_efficiency': 100,
        'time_start': 45,
        'time_stop': 20,
        'color': 4,
        'note': '<p><strong>Proveedor:</strong> Metalúrgica Precisión S.A.</p><p><strong>Lead Time:</strong> 5 días hábiles</p><p><strong>Especialidad:</strong> Bases de acero negro y dorado</p>',
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
    {'name': '1. Recepción y Verificación de Tapa', 'workcenter_code': 'QC', 'time_cycle_manual': 30, 'sequence': 10},
    {'name': '2. Recepción y Verificación de Base', 'workcenter_code': 'QC', 'time_cycle_manual': 20, 'sequence': 20},
    {'name': '3. Ensamble Tapa + Base', 'workcenter_code': 'ENSAM', 'time_cycle_manual': 60, 'sequence': 30},
    {'name': '4. Control de Calidad Final', 'workcenter_code': 'QC', 'time_cycle_manual': 15, 'sequence': 40},
    {'name': '5. Embalaje para Entrega', 'workcenter_code': 'ENSAM', 'time_cycle_manual': 30, 'sequence': 50},
]

OPERACIONES_LUSTRADO = [
    {'name': '1. Preparación y Envío a Lustrador', 'workcenter_code': 'LUST', 'time_cycle_manual': 30, 'sequence': 10},
    {'name': '2. Proceso de Lustrado (externo)', 'workcenter_code': 'LUST', 'time_cycle_manual': 480, 'sequence': 20},
    {'name': '3. Recepción y Verificación', 'workcenter_code': 'QC', 'time_cycle_manual': 20, 'sequence': 30},
]

# ═══════════════════════════════════════════════════════════════════════════════
# LIMPIEZA OPCIONAL
# ═══════════════════════════════════════════════════════════════════════════════
if '--limpiar' in sys.argv:
    print("\n" + "═"*70)
    print("LIMPIANDO DATOS EXISTENTES")
    print("═"*70)

    # Cancelar y eliminar MOs
    mos = search('mrp.production', [['state', 'not in', ['done', 'cancel']]])
    if mos:
        try:
            execute('mrp.production', 'action_cancel', [mos])
            execute('mrp.production', 'unlink', [mos])
            print(f"  {len(mos)} órdenes de fabricación eliminadas")
        except Exception as e:
            print(f"  No se pudieron eliminar MOs: {str(e)[:50]}")

    # Cancelar y eliminar POs
    pos = search('purchase.order', [['state', 'not in', ['done', 'cancel']]])
    if pos:
        try:
            execute('purchase.order', 'button_cancel', [pos])
            execute('purchase.order', 'unlink', [pos])
            print(f"  {len(pos)} órdenes de compra eliminadas")
        except Exception as e:
            print(f"  No se pudieron eliminar POs: {str(e)[:50]}")

    # Eliminar SOs en draft
    sos = search('sale.order', [['state', '=', 'draft']])
    if sos:
        execute('sale.order', 'unlink', [sos])
        print(f"  {len(sos)} cotizaciones eliminadas")

    # Eliminar Work Orders
    wos = search('mrp.workorder', [])
    if wos:
        try:
            execute('mrp.workorder', 'unlink', [wos])
            print(f"  {len(wos)} work orders eliminadas")
        except:
            pass

    # Eliminar operaciones de BoM
    ops = search('mrp.routing.workcenter', [])
    if ops:
        execute('mrp.routing.workcenter', 'unlink', [ops])
        print(f"  {len(ops)} operaciones eliminadas")

    # Eliminar capacidades
    caps = search('mrp.workcenter.capacity', [])
    if caps:
        execute('mrp.workcenter.capacity', 'unlink', [caps])
        print(f"  {len(caps)} capacidades eliminadas")

    # Archivar work centers (no eliminar por logs de productividad)
    wcs = search('mrp.workcenter', [])
    if wcs:
        write('mrp.workcenter', wcs, {'active': False})
        print(f"  {len(wcs)} work centers archivados")

    # Eliminar Quality Points de demo
    qc_points = search('quality.point', [['name', 'ilike', 'QC-%']])
    if qc_points:
        execute('quality.point', 'unlink', [qc_points])
        print(f"  {len(qc_points)} quality points eliminados")

    # Eliminar ubicaciones de subcontratación y tránsito creadas
    custom_locs = search('stock.location', [
        '|',
        ['name', 'ilike', 'Subcontract -%'],
        ['name', 'ilike', 'Transit:%']
    ])
    if custom_locs:
        try:
            execute('stock.location', 'unlink', [custom_locs])
            print(f"  {len(custom_locs)} ubicaciones personalizadas eliminadas")
        except:
            pass  # Pueden tener movimientos

    # Archivar productos de demo
    productos_demo = search('product.template', [
        '|', '|', '|', '|',
        ['name', 'ilike', 'Mesa Comedor%'],
        ['name', 'ilike', 'Tapa %'],
        ['name', 'ilike', 'Base Acero%'],
        ['default_code', 'ilike', 'MESA-%'],
        ['default_code', 'ilike', 'TAPA-%'],
    ])
    if productos_demo:
        # Primero eliminar BoMs
        boms = search('mrp.bom', [['product_tmpl_id', 'in', productos_demo]])
        if boms:
            execute('mrp.bom', 'unlink', [boms])
            print(f"  {len(boms)} BoMs eliminadas")

        write('product.template', productos_demo, {'active': False})
        print(f"  {len(productos_demo)} productos archivados")

# ═══════════════════════════════════════════════════════════════════════════════
# 0. CONFIGURACIÓN AVANZADA (Multi-step routes, Ubicaciones, QC)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("0. CONFIGURACIÓN AVANZADA DEL SISTEMA")
print("═"*70)

# 0.1 Multi-step routes en almacén
print("\n  0.1 Configurando Multi-step Routes...")
warehouse = search_read('stock.warehouse', [], ['id', 'name', 'reception_steps', 'delivery_steps'])
if warehouse:
    wh = warehouse[0]
    if wh['reception_steps'] != 'three_steps' or wh['delivery_steps'] != 'pick_pack_ship':
        write('stock.warehouse', [wh['id']], {
            'reception_steps': 'three_steps',  # Input → Quality Control → Stock
            'delivery_steps': 'pick_pack_ship',  # Pick → Pack → Ship
        })
        print(f"      ✓ Almacén {wh['name']}: three_steps / pick_pack_ship")
    else:
        print(f"      - Almacén {wh['name']}: ya configurado")

# 0.2 Ubicaciones de subcontratista
print("\n  0.2 Creando ubicaciones de subcontratista...")
supplier_loc = search_read('stock.location', [['usage', '=', 'supplier']], ['id'])
SUPPLIER_PARENT_ID = supplier_loc[0]['id'] if supplier_loc else 1

SUBCONTRACT_LOCATIONS = {}
subcontract_locs = [
    ('CARP', 'Subcontract - Carpintería Hnos. García'),
    ('LUST', 'Subcontract - Lustres & Acabados'),
    ('META', 'Subcontract - Metalúrgica Precisión'),
    ('MARM', 'Subcontract - Marmolería Del Sur'),
    ('NEOL', 'Subcontract - Neolith Argentina'),
]
for code, name in subcontract_locs:
    loc_id, created = get_or_create('stock.location',
        [['name', '=', name]],
        {'name': name, 'usage': 'internal', 'location_id': SUPPLIER_PARENT_ID, 'barcode': code}
    )
    SUBCONTRACT_LOCATIONS[code] = loc_id
    if created:
        print(f"      + {name}")

# 0.3 Ubicaciones de tránsito entre proveedores
print("\n  0.3 Creando ubicaciones de tránsito...")
transit_parent = search_read('stock.location', [['usage', '=', 'transit'], ['location_id', '=', False]], ['id'])
if not transit_parent:
    TRANSIT_PARENT_ID = create('stock.location', {'name': 'Transit Locations', 'usage': 'transit'})
else:
    TRANSIT_PARENT_ID = transit_parent[0]['id']

transit_locs = [
    ('TR-CARP-LUST', 'Transit: Carpintería → Lustrador'),
    ('TR-LUST-FAB', 'Transit: Lustrador → Fábrica'),
    ('TR-META-FAB', 'Transit: Metalúrgica → Fábrica'),
    ('TR-MARM-FAB', 'Transit: Marmolería → Fábrica'),
]
for code, name in transit_locs:
    loc_id, created = get_or_create('stock.location',
        [['name', '=', name]],
        {'name': name, 'usage': 'transit', 'location_id': TRANSIT_PARENT_ID, 'barcode': code}
    )
    if created:
        print(f"      + {name}")

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

print(f"  UoM: {UOM_ID}")
print(f"  Ruta Manufacture: {RUTA_MANUFACTURE}")
print(f"  Ruta Buy: {RUTA_BUY}")
print(f"  Ruta MTO: {RUTA_MTO}")

# Activar y configurar rutas
if RUTA_MTO:
    write('stock.route', [RUTA_MTO], {'active': True, 'product_selectable': True})
    print("  + MTO activada y seleccionable")
if RUTA_BUY:
    write('stock.route', [RUTA_BUY], {'product_selectable': True})
if RUTA_MANUFACTURE:
    write('stock.route', [RUTA_MANUFACTURE], {'product_selectable': True})

# Categorías
print("\n  Creando categorías...")
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
print("\n  Asociando ubicaciones de subcontratación...")
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

# Terminación
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
print("\n  Configurando capacidades...")

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

        if created:
            prov_id = PROVEEDOR_IDS.get('Metalúrgica Precisión S.A.')
            if prov_id:
                get_or_create('product.supplierinfo',
                    [['product_tmpl_id', '=', tmpl_id], ['partner_id', '=', prov_id]],
                    {'partner_id': prov_id, 'product_tmpl_id': tmpl_id, 'price': costo, 'delay': base_mat['lead_time']}
                )

                bom_id = create('mrp.bom', {
                    'product_tmpl_id': tmpl_id,
                    'product_id': variant_id,
                    'product_qty': 1,
                    'type': 'subcontract',
                    'subcontractor_ids': [(6, 0, [prov_id])],
                    'produce_delay': base_mat['lead_time'],
                })

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

# 8.1 Tapas SIN terminar
print("\n  8.1 Tapas SIN terminar (compra a Carpintería):")
TAPAS_SIN_TERMINAR = {}

for medida in MEDIDAS:
    nombre = f"Tapa Madera Sin Terminar {medida['codigo']}"
    codigo = f"TAPA-MADERA-RAW-{medida['codigo'].replace('x', '')}"
    costo = mat_madera['costo_base'] * medida['factor_precio']

    # Rutas: Buy + MTO
    rutas_componente = [r for r in [RUTA_BUY, RUTA_MTO] if r]

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
print("\n  8.2 Tapas CON terminación (subcontratación a Lustrador):")
TAPAS_TERMINADAS = {}

lustrador_id = PROVEEDOR_IDS.get(mat_madera['proveedor_terminacion'])

# Rutas: Buy + MTO para reabastecimiento automático
rutas_componente = [r for r in [RUTA_BUY, RUTA_MTO] if r]

for medida in MEDIDAS:
    nombre_base = f"Tapa Madera Terminada {medida['codigo']}"
    codigo_base = f"TAPA-MADERA-TERM-{medida['codigo'].replace('x', '')}"
    precio_terminada = (mat_madera['costo_base'] + 80) * medida['factor_precio']

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
            'standard_price': (mat_madera['costo_base'] + 60) * medida['factor_precio'],
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
        'list_price': 1500,
        'uom_id': UOM_ID,
        'purchase_ok': False,
        'sale_ok': True,
        'route_ids': [(6, 0, rutas_mesa)] if rutas_mesa else [],
        'sale_delay': 14,  # Lead time de entrega al cliente
        'description_sale': 'Mesa de comedor premium. Seleccione material de tapa, base y medidas.',
    })
    print(f"  + Mesa creada (ID: {mesa_tmpl_id})")

    for attr_name in ['Material Tapa', 'Material Base', 'Medidas']:
        attr_id = ATRIBUTOS[attr_name]
        values = [v for k, v in ATTR_VALUES.items() if k.startswith(f"{attr_name}|")]
        create('product.template.attribute.line', {
            'product_tmpl_id': mesa_tmpl_id,
            'attribute_id': attr_id,
            'value_ids': [(6, 0, values)],
        })
        print(f"    -> Atributo: {attr_name}")

# Asegurar rutas Manufacture + MTO (fabricación bajo pedido)
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

    for vv in var_values:
        attr = search_read('product.attribute', [['id', '=', vv['attribute_id'][0]]], ['name'])[0]
        if attr['name'] == 'Material Tapa':
            material_tapa = vv['name']
        elif attr['name'] == 'Material Base':
            material_base = vv['name']
        elif attr['name'] == 'Medidas':
            medida_codigo = vv['name'].replace(' cm', '')

    if not all([material_tapa, material_base, medida_codigo]):
        continue

    # Determinar componente tapa
    if material_tapa == 'Madera Paraíso':
        tapa_id = TAPAS_TERMINADAS.get((medida_codigo, 'Lustre Mate'))
    else:
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

# ═══════════════════════════════════════════════════════════════════════════════
# 12. CONTROL POINTS DE CALIDAD
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("12. CONFIGURANDO CONTROL POINTS DE CALIDAD")
print("═"*70)

# Obtener IDs necesarios
quality_team = search_read('quality.alert.team', [], ['id'], limit=1)
QUALITY_TEAM_ID = quality_team[0]['id'] if quality_team else 1

picking_types = search_read('stock.picking.type', [], ['id', 'code'])
RECEIPTS_PT = next((pt['id'] for pt in picking_types if pt['code'] == 'incoming'), None)
MFG_PT = next((pt['id'] for pt in picking_types if pt['code'] == 'mrp_operation'), None)

test_types = search_read('quality.point.test_type', [['technical_name', '=', 'passfail']], ['id'])
PASSFAIL_TEST = test_types[0]['id'] if test_types else 7

# Obtener productos para los control points
tapas_sin_terminar = search_read('product.product', [['name', 'ilike', 'Tapa Madera Sin Terminar%']], ['id'])
tapas_terminadas = search_read('product.product', [['name', 'ilike', 'Tapa Madera Terminada%']], ['id'])
bases_productos = search_read('product.product', [['name', 'ilike', 'Base Acero%']], ['id'])
tapas_marmol = search_read('product.product', [['name', 'ilike', 'Tapa Mármol%']], ['id'])
tapas_neolith = search_read('product.product', [['name', 'ilike', 'Tapa Neolith%']], ['id'])
mesas_productos = search_read('product.product', [['name', 'ilike', 'Mesa Comedor%']], ['id'])

# Definir Control Points
QUALITY_POINTS = [
    {
        'name': 'QC-REC-TAPA-CRUDA',
        'title': 'Control Recepción Tapas Sin Terminar',
        'products': tapas_sin_terminar,
        'picking_type': RECEIPTS_PT,
        'note': '<p>Verificar:<br/>- Dimensiones correctas<br/>- Sin grietas ni nudos excesivos<br/>- Humedad de la madera</p>',
    },
    {
        'name': 'QC-REC-TAPA-LUSTRADA',
        'title': 'Control Recepción Tapas Lustradas',
        'products': tapas_terminadas,
        'picking_type': RECEIPTS_PT,
        'note': '<p>Verificar:<br/>- Acabado uniforme sin burbujas<br/>- Brillo según especificación<br/>- Sin marcas ni rayaduras</p>',
    },
    {
        'name': 'QC-REC-BASE',
        'title': 'Control Recepción Bases Metálicas',
        'products': bases_productos,
        'picking_type': RECEIPTS_PT,
        'note': '<p>Verificar:<br/>- Soldaduras completas y limpias<br/>- Pintura sin descascarado<br/>- Nivelación correcta</p>',
    },
    {
        'name': 'QC-REC-MARMOL',
        'title': 'Control Recepción Tapas Mármol',
        'products': tapas_marmol,
        'picking_type': RECEIPTS_PT,
        'note': '<p>Verificar:<br/>- Sin fisuras ni grietas<br/>- Pulido uniforme<br/>- Veteado según muestra aprobada</p>',
    },
    {
        'name': 'QC-REC-NEOLITH',
        'title': 'Control Recepción Tapas Neolith',
        'products': tapas_neolith,
        'picking_type': RECEIPTS_PT,
        'note': '<p>Verificar:<br/>- Espesor uniforme<br/>- Bordes sin astillado<br/>- Color según especificación</p>',
    },
    {
        'name': 'QC-MFG-ENSAMBLE',
        'title': 'Control Pre-Ensamblado Mesa',
        'products': mesas_productos,
        'picking_type': MFG_PT,
        'note': '<p>Verificar antes de ensamblar:<br/>- Componentes completos<br/>- Tapa y base compatibles en medida<br/>- Sin defectos visibles</p>',
    },
]

qc_creados = 0
for qc in QUALITY_POINTS:
    if not qc['products'] or not qc['picking_type']:
        continue
    qc_id, created = get_or_create('quality.point',
        [['name', '=', qc['name']]],
        {
            'name': qc['name'],
            'title': qc['title'],
            'product_ids': [(6, 0, [p['id'] for p in qc['products']])],
            'picking_type_ids': [(6, 0, [qc['picking_type']])],
            'measure_on': 'operation' if 'MFG' in qc['name'] else 'product',
            'measure_frequency_type': 'all',
            'test_type_id': PASSFAIL_TEST,
            'team_id': QUALITY_TEAM_ID,
            'note': qc['note'],
            'failure_message': '<p>Rechazar y notificar al proveedor</p>',
        }
    )
    if created:
        qc_creados += 1
        print(f"  + {qc['title']}")
    else:
        print(f"  - {qc['title']} (existente)")

print(f"\n  Total: {qc_creados} Control Points creados")

# ═══════════════════════════════════════════════════════════════════════════════
# 13. ORDEN DE DEMO (MTO genera MO y POs automáticamente)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("13. CREANDO ORDEN DE DEMO (FLUJO AUTOMÁTICO MTO)")
print("═"*70)

# Buscar variante de madera
mesa_madera = None
for var in mesa_variantes:
    if 'Madera' in var['display_name']:
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
total_qc = len(search('quality.point', []))

print(f"""
  CONFIGURACIÓN AVANZADA:
  ────────────────────────────────────────────────────────────────────
  Almacén: Multi-step Routes (three_steps / pick_pack_ship)
  Ubicaciones Subcontratista: 5 (por proveedor)
  Ubicaciones Tránsito: 4 (entre proveedores)
  Quality Control Points: {total_qc}

  PRODUCTOS:
  ────────────────────────────────────────────────────────────────────
  Mesa Comedor Premium: {len(mesa_variantes)} variantes
    (3 materiales tapa x 2 bases x 2 medidas)
  Tapas Mármol/Neolith: 4 productos
  Tapas Madera Sin Terminar: 2 productos
  Tapas Madera Terminadas: 6 variantes (con terminación)
  Bases Metálicas: 4 productos

  RUTAS MTO (Replenish on Order):
  ────────────────────────────────────────────────────────────────────
  Mesa:           Manufacture + MTO
  Bases:          Buy + MTO
  Tapas Simples:  Buy + MTO
  Tapas Madera:   Buy + MTO

  Flujo automático:
  Venta confirmada → MO automática → POs automáticas (por MTO)

  PLANIFICACIÓN:
  ────────────────────────────────────────────────────────────────────
  Work Centers: {total_wcs}
    - Carpintería Externa (CARP)
    - Lustrado y Acabados (LUST)
    - Marmolería Externa (MARM)
    - Metalurgia Externa (META)
    - Ensamble Final (ENSAM) - Capacidad: 2 uds
    - Control de Calidad (QC) - Capacidad: 5 uds

  Operaciones: {total_ops}
    Mesa: 5 operaciones (QC -> ENSAM -> QC -> ENSAM)
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

  FLUJO DE MADERA:
  ────────────────────────────────────────────────────────────────────

  ┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
  │   CARPINTERÍA   │     │     LUSTRADOR       │     │     STOCK       │
  │   Hnos. García  │────>│  Lustres & Acabados │────>│   Disponible    │
  └─────────────────┘     └─────────────────────┘     └─────────────────┘
         │                         │                         │
    Tapa Madera              Tapa Madera               Tapa Madera
    SIN Terminar             CON Terminación           Terminada
    (Compra PO)              (Subcontratación)         (Para MO Mesa)

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
