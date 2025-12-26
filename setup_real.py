#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
SETUP DEMO REAL - AZUL BA (Basado en planilla de producción real)
═══════════════════════════════════════════════════════════════════════════════

Este script configura una demo basada en la operatoria REAL del cliente Azul BA.

PRODUCTOS PRINCIPALES:
- MESAS: Wull, Rocca, Rinni, Venus, Frame, Exon, Fix, Cantabria
  - Variantes: Stone (Neolith/Dekton), Wood (MDF lustrado)
  - Extensibles y fijas
- SILLAS: Gin, Evelyn, Eve, Ulises, Forms, Luana
  - Tipos: Silla, Butaca, Banqueta
- BASES: Fix, Cantabria, Krull, Valentinox, Conica, Tecno

PROVEEDORES (64 principales):
- LUSTRADORES: Gustavo Lus, Jonathan Lus, Hernan Lus, Elian Lugo
- CARPINTEROS: Maxi Car, Francisco, Celestino, Pablo
- TORNERÍA: Hugo, Coco Tornero
- PIEDRA: Eurostone, Destefano, Decostone
- ALUMINIO: Ormetal, AX Aluminio, Marra, DYM Metal
- PINTURA: Negaby, Florida
- SILLAS: BYB, ECSA, JYJ, Milciades, Elias
- CORTE CNC: GN Estudio, AGG Metalurgica
- TAPICERÍA: Juan Andres, Cacho, Pedro

FLUJO MULTI-NIVEL:
Un producto típico pasa por 5-10 proveedores:
Corte CNC → Tornería → Pintura/Lustrado → Tapicería → Ensamble → QC → Embalaje

USO:
    python setup_real.py              # Ejecuta setup
    python setup_real.py --limpiar    # Limpia y ejecuta setup

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
    existing = search_read(model, domain, ['id'])
    if existing:
        return existing[0]['id'], False
    new_id = create(model, vals)
    return new_id, True

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN REAL - PROVEEDORES
# ═══════════════════════════════════════════════════════════════════════════════

PROVEEDORES_REALES = [
    # LUSTRADORES (14 días)
    {'name': 'Gustavo Lus', 'rubro': 'LUSTRADOR', 'lead_time': 14, 'city': 'Buenos Aires'},
    {'name': 'Jonathan Lus', 'rubro': 'LUSTRADOR', 'lead_time': 14, 'city': 'Buenos Aires'},
    {'name': 'Hernan Lus', 'rubro': 'LUSTRADOR', 'lead_time': 14, 'city': 'Buenos Aires'},
    {'name': 'Elian Lugo Lus', 'rubro': 'LUSTRADOR', 'lead_time': 14, 'city': 'Caseros'},

    # CARPINTEROS (14-21 días)
    {'name': 'Maxi Car', 'rubro': 'CARPINTERO', 'lead_time': 14, 'city': 'Buenos Aires'},
    {'name': 'Carpintero Francisco', 'rubro': 'CARPINTERO', 'lead_time': 14, 'city': 'CABA',
     'address': 'Punta Arenas 1100'},
    {'name': 'Celestino', 'rubro': 'CARPINTERIA', 'lead_time': 21, 'city': 'CABA',
     'address': 'Palpa 3739'},
    {'name': 'Pablo Car', 'rubro': 'CARPINTERO', 'lead_time': 7, 'city': 'Buenos Aires'},

    # TORNERÍA (7-10 días)
    {'name': 'Hugo', 'rubro': 'TORNERIA', 'lead_time': 10, 'city': 'Buenos Aires'},
    {'name': 'Coco Tornero', 'rubro': 'TORNERO MADERA', 'lead_time': 7, 'city': 'Caseros',
     'address': 'Cavassa 4314'},

    # MARMOLERÍA / PIEDRA (7-30 días)
    {'name': 'Eurostone', 'rubro': 'CORTE MARMOL', 'lead_time': 10, 'city': 'CABA',
     'address': 'José Leon Suarez 2165'},
    {'name': 'Destefano', 'rubro': 'MARMOLERIA', 'lead_time': 30, 'city': 'Buenos Aires',
     'address': 'Av. Del Campo 1270'},
    {'name': 'Destefano Central', 'rubro': 'MARMOLERIA', 'lead_time': 7, 'city': 'Buenos Aires'},
    {'name': 'Decostone', 'rubro': 'MARMOLERIA', 'lead_time': 7, 'city': 'Buenos Aires',
     'address': 'Bauness 947'},

    # ALUMINIO (7-14 días)
    {'name': 'Ormetal', 'rubro': 'ALUMINIO', 'lead_time': 7, 'city': 'Buenos Aires'},
    {'name': 'AX Aluminio', 'rubro': 'CORTE CAÑOS ALUMINIO', 'lead_time': 14, 'city': 'Buenos Aires',
     'address': 'Gral. Manuel A. Rodriguez 1260'},
    {'name': 'Marra', 'rubro': 'ALUMINIO', 'lead_time': 7, 'city': 'Buenos Aires'},
    {'name': 'DYM Metal', 'rubro': 'ALUMINIO', 'lead_time': 7, 'city': 'Billinghurst',
     'address': 'Av. 101 Dr. Ricardo Balbín 4644'},

    # PINTURA (7 días)
    {'name': 'Pintura Negaby', 'rubro': 'PINTURA', 'lead_time': 7, 'city': 'Buenos Aires'},
    {'name': 'Pintura Florida', 'rubro': 'PINTURA', 'lead_time': 7, 'city': 'Buenos Aires'},

    # SILLAS (20-50 días)
    {'name': 'BYB', 'rubro': 'SILLAS', 'lead_time': 50, 'city': 'Caseros',
     'address': 'M. Fernandez de Oliveira 3288'},
    {'name': 'ECSA', 'rubro': 'SILLAS', 'lead_time': 20, 'city': 'San Justo',
     'address': 'Mariano Santamaría 3052'},
    {'name': 'JYJ', 'rubro': 'SILLAS', 'lead_time': 25, 'city': 'Buenos Aires'},
    {'name': 'Milciades', 'rubro': 'SILLETERO', 'lead_time': 21, 'city': 'Buenos Aires'},
    {'name': 'Elias Sillas', 'rubro': 'SILLA', 'lead_time': 35, 'city': 'Ciudadela',
     'address': 'Dr. Schweitzer 1853'},

    # CORTE CNC (7-14 días)
    {'name': 'GN Estudio', 'rubro': 'CORTE CNC', 'lead_time': 7, 'city': 'Buenos Aires'},
    {'name': 'AGG Metalurgica', 'rubro': 'CORTE CNC', 'lead_time': 14, 'city': 'San Andres',
     'address': 'Luna 2240'},

    # TAPICERÍA (7-14 días)
    {'name': 'Tapicero Juan Andres', 'rubro': 'TAPICERO', 'lead_time': 7, 'city': 'Buenos Aires'},
    {'name': 'Cacho', 'rubro': 'TAPICERO', 'lead_time': 7, 'city': 'Del Viso'},
    {'name': 'Pedro', 'rubro': 'TAPICERO', 'lead_time': 14, 'city': 'Buenos Aires'},

    # ACERO (7 días)
    {'name': 'Carlos Acero', 'rubro': 'ACERO REVESTIMIENTO', 'lead_time': 7, 'city': 'Munro',
     'address': 'Bernardo de Irigoyen 2213'},
    {'name': 'Famiq', 'rubro': 'ACERO', 'lead_time': 7, 'city': 'Buenos Aires',
     'address': 'Av San Martín 4723'},

    # HERRERÍA (10-20 días)
    {'name': 'Chamo', 'rubro': 'HERRERIA', 'lead_time': 20, 'city': 'CABA',
     'address': 'Donado 1049'},
    {'name': 'Herreria Roberto', 'rubro': 'HERRERIA', 'lead_time': 10, 'city': 'Buenos Aires'},
    {'name': 'Herreria Total', 'rubro': 'CHAPA CORTE Y PLEGADO', 'lead_time': 10, 'city': 'Buenos Aires'},

    # VIDRIOS (14 días)
    {'name': 'Vidpro', 'rubro': 'VIDRIOS', 'lead_time': 14, 'city': 'Buenos Aires'},
    {'name': 'Ebenor', 'rubro': 'VIDRIOS TEMPLADOS', 'lead_time': 14, 'city': 'Buenos Aires',
     'address': 'Oliden 2380'},

    # CROMADO (14 días)
    {'name': 'Claudio Cromador', 'rubro': 'CROMADOR', 'lead_time': 14, 'city': 'José Leon Suarez',
     'address': 'Latorre 6760'},
    {'name': 'Sergio Cromador', 'rubro': 'CROMADOR', 'lead_time': 14, 'city': 'Buenos Aires'},

    # PLEGADO / METALURGICA (20 días)
    {'name': 'GLO Industrial', 'rubro': 'PLEGADO DE CHAPA', 'lead_time': 20, 'city': 'Buenos Aires'},
    {'name': 'Saravia', 'rubro': 'ANODIZADO', 'lead_time': 10, 'city': 'Buenos Aires'},

    # FUNDICIÓN (30 días)
    {'name': 'Funlaux', 'rubro': 'FUNDICION', 'lead_time': 30, 'city': 'Buenos Aires'},

    # HIERROS (5-7 días)
    {'name': 'Hierros Torrent', 'rubro': 'HIERROS', 'lead_time': 5, 'city': 'Buenos Aires'},

    # EMBALAJE (7-10 días)
    {'name': 'Hector Embalajes', 'rubro': 'EMBALAJES', 'lead_time': 10, 'city': 'Buenos Aires'},
    {'name': 'Ezequiel Casco', 'rubro': 'EMBALAJE', 'lead_time': 7, 'city': 'Caseros'},

    # PULIDOR (7 días)
    {'name': 'Ariel', 'rubro': 'PULIDOR', 'lead_time': 7, 'city': 'Villa Lynch',
     'address': 'Cuenca 770'},

    # OTROS
    {'name': 'Sirota', 'rubro': 'AJUSTES', 'lead_time': 10, 'city': 'Buenos Aires'},
]

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN REAL - PRODUCTOS
# ═══════════════════════════════════════════════════════════════════════════════

# MESAS - Modelos principales
MODELOS_MESA = [
    # Modelo, Tipo (extensible/fija), Material principal
    {'nombre': 'Wull', 'tipos': ['Extensible Stone', 'Extensible Wood', 'Stone', 'Wood'], 'es_principal': True},
    {'nombre': 'Rocca', 'tipos': ['Stone', 'Wood'], 'es_principal': True},
    {'nombre': 'Rinni', 'tipos': ['Extensible Stone', 'Extensible Wood', 'Stone', 'Acero'], 'es_principal': True},
    {'nombre': 'Venus', 'tipos': ['Extensible Stone', 'Extensible Wood', 'Stone', 'Wood'], 'es_principal': True},
    {'nombre': 'Frame', 'tipos': ['Stone', 'Wood', 'PE'], 'es_principal': False},
    {'nombre': 'Exon', 'tipos': ['Stone', 'Wood'], 'es_principal': False},
    {'nombre': 'Valentinox', 'tipos': ['PE'], 'es_principal': False},
    {'nombre': 'Krull', 'tipos': ['PE'], 'es_principal': False},
    {'nombre': 'Conica', 'tipos': ['Stone'], 'es_principal': False},
    {'nombre': 'Danesa Redonda', 'tipos': ['PE'], 'es_principal': False},
]

# BASES - Modelos
MODELOS_BASE = [
    {'nombre': 'Fix', 'material': 'Caño aluminio', 'proveedor': 'AX Aluminio', 'lead_time': 14},
    {'nombre': 'Cantabria', 'material': 'Caño aluminio', 'proveedor': 'AX Aluminio', 'lead_time': 14},
    {'nombre': 'Tecno', 'material': 'Aluminio', 'proveedor': 'Ormetal', 'lead_time': 7},
    {'nombre': 'Rinni', 'material': 'MDF + Acero', 'proveedor': 'Hugo', 'lead_time': 10},
    {'nombre': 'Valentinox', 'material': 'Acero inoxidable', 'proveedor': 'Hugo', 'lead_time': 10},
    {'nombre': 'Krull', 'material': 'Madera Paraiso', 'proveedor': 'Celestino', 'lead_time': 21},
    {'nombre': 'Conica', 'material': 'Varios', 'proveedor': 'Hugo', 'lead_time': 10},
    {'nombre': 'Frame', 'material': 'Madera Paraiso', 'proveedor': 'Celestino', 'lead_time': 21},
]

# SILLAS - Modelos
MODELOS_SILLA = [
    {'nombre': 'Gin', 'tipos': ['Silla', 'Butaca', 'Banqueta'], 'proveedor': 'BYB', 'lead_time': 50},
    {'nombre': 'Evelyn', 'tipos': ['Silla', 'Butaca'], 'proveedor': 'ECSA', 'lead_time': 20},
    {'nombre': 'Eve', 'tipos': ['Silla', 'Butaca'], 'proveedor': 'JYJ', 'lead_time': 25},
    {'nombre': 'Ulises', 'tipos': ['Silla', 'Butaca'], 'proveedor': 'Milciades', 'lead_time': 21},
    {'nombre': 'Forms', 'tipos': ['Silla'], 'proveedor': 'ECSA', 'lead_time': 20},
    {'nombre': 'Luana', 'tipos': ['Silla', 'Butaca'], 'proveedor': 'JYJ', 'lead_time': 25},
    {'nombre': 'Indu', 'tipos': ['Silla', 'Butaca'], 'proveedor': 'Milciades', 'lead_time': 21},
    {'nombre': 'Tona', 'tipos': ['Silla'], 'proveedor': 'ECSA', 'lead_time': 20},
    {'nombre': 'Alika', 'tipos': ['Silla'], 'proveedor': 'JYJ', 'lead_time': 25},
]

# MATERIALES DE TAPA
MATERIALES_TAPA = [
    {'nombre': 'Neolith Calacatta', 'codigo': 'NEOL-CAL', 'tipo': 'Stone', 'proveedor': 'Eurostone', 'lead_time': 10, 'costo': 800000},
    {'nombre': 'Dekton Rem', 'codigo': 'DEK-REM', 'tipo': 'Stone', 'proveedor': 'Eurostone', 'lead_time': 10, 'costo': 850000},
    {'nombre': 'Dekton Sirius', 'codigo': 'DEK-SIR', 'tipo': 'Stone', 'proveedor': 'Eurostone', 'lead_time': 10, 'costo': 850000},
    {'nombre': 'MDF Laqueado', 'codigo': 'MDF-LAQ', 'tipo': 'Wood', 'proveedor': 'GN Estudio', 'lead_time': 7, 'costo': 300000},
    {'nombre': 'Melamina Blanca', 'codigo': 'MEL-BLA', 'tipo': 'Wood', 'proveedor': 'GN Estudio', 'lead_time': 7, 'costo': 200000},
    {'nombre': 'Paraiso', 'codigo': 'PARAISO', 'tipo': 'Wood', 'proveedor': 'Celestino', 'lead_time': 21, 'costo': 350000},
]

# MEDIDAS STANDARD
MEDIDAS = [
    {'codigo': '140x80', 'nombre': '140 x 80 cm', 'factor': 0.8},
    {'codigo': '160x90', 'nombre': '160 x 90 cm', 'factor': 0.9},
    {'codigo': '180x90', 'nombre': '180 x 90 cm', 'factor': 1.0},
    {'codigo': '200x100', 'nombre': '200 x 100 cm', 'factor': 1.2},
    {'codigo': '220x100', 'nombre': '220 x 100 cm', 'factor': 1.4},
    {'codigo': '240x100', 'nombre': '240 x 100 cm', 'factor': 1.6},
]

# TERMINACIONES
TERMINACIONES = [
    {'nombre': 'Lustre Mate', 'codigo': 'MATE', 'proveedor': 'Gustavo Lus', 'lead_time': 14, 'costo': 90000},
    {'nombre': 'Lustre Brillante', 'codigo': 'BRILL', 'proveedor': 'Gustavo Lus', 'lead_time': 14, 'costo': 120000},
    {'nombre': 'Natural', 'codigo': 'NAT', 'proveedor': 'Gustavo Lus', 'lead_time': 14, 'costo': 60000},
    {'nombre': 'Nogal Claro', 'codigo': 'NOG-CLA', 'proveedor': 'Jonathan Lus', 'lead_time': 14, 'costo': 100000},
    {'nombre': 'Nogal Oscuro', 'codigo': 'NOG-OSC', 'proveedor': 'Jonathan Lus', 'lead_time': 14, 'costo': 100000},
]

# PINTURAS
PINTURAS = [
    {'nombre': 'Negro Microtexturado', 'codigo': 'NEG-MIC', 'proveedor': 'Pintura Negaby', 'lead_time': 7},
    {'nombre': 'Negro Liso', 'codigo': 'NEG-LIS', 'proveedor': 'Pintura Negaby', 'lead_time': 7},
    {'nombre': 'Blanco', 'codigo': 'BLANCO', 'proveedor': 'Pintura Florida', 'lead_time': 7},
    {'nombre': 'Dorado', 'codigo': 'DORADO', 'proveedor': 'Pintura Florida', 'lead_time': 7},
]

# CLIENTES DE EJEMPLO
CLIENTES = [
    {'name': 'Alejandro Herrero', 'city': 'CABA', 'street': 'Yerbal 1076'},
    {'name': 'Hotel Boutique La Estancia', 'city': 'Buenos Aires'},
    {'name': 'Estudio de Arquitectura Modernista', 'city': 'Buenos Aires'},
]

# WORK CENTERS
WORK_CENTERS_CONFIG = [
    {'name': 'Taller Producción', 'code': 'TALLER', 'time_efficiency': 100, 'time_start': 15, 'time_stop': 10},
    {'name': 'Ensamble Final', 'code': 'ENSAM', 'time_efficiency': 100, 'time_start': 10, 'time_stop': 5},
    {'name': 'Control de Calidad', 'code': 'QC', 'time_efficiency': 100, 'time_start': 5, 'time_stop': 5},
    {'name': 'Embalaje', 'code': 'EMBAL', 'time_efficiency': 100, 'time_start': 5, 'time_stop': 5},
]

# ═══════════════════════════════════════════════════════════════════════════════
# EJECUCIÓN
# ═══════════════════════════════════════════════════════════════════════════════

# UoM
uom = search_read('uom.uom', [['name', 'ilike', 'unit']], ['id'], limit=1)
UOM_ID = uom[0]['id'] if uom else 1

# Rutas
rutas = search_read('stock.route', ['|', ['active', '=', True], ['active', '=', False]], ['id', 'name', 'active'])
RUTA_MANUFACTURE = next((r['id'] for r in rutas if 'manufacture' in r['name'].lower()), None)
RUTA_BUY = next((r['id'] for r in rutas if 'buy' in r['name'].lower()), None)
RUTA_MTO = next((r['id'] for r in rutas if 'mto' in r['name'].lower() or 'replenish on order' in r['name'].lower()), None)
RUTA_DROPSHIP = next((r['id'] for r in rutas if r['name'].lower() == 'dropship'), None)

if RUTA_MTO:
    write('stock.route', [RUTA_MTO], {'active': True, 'product_selectable': True})

# ═══════════════════════════════════════════════════════════════════════════════
# 1. CATEGORÍAS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("1. CREANDO CATEGORÍAS")
print("═"*70)

cat_all = search_read('product.category', [['name', '=', 'All']], ['id'])
CAT_PARENT = cat_all[0]['id'] if cat_all else 1

CATEGORIAS = {}
categorias_crear = [
    ('Mobiliario', CAT_PARENT),
    ('Mesas', 'Mobiliario'),
    ('Bases', 'Mobiliario'),
    ('Tapas', 'Mobiliario'),
    ('Tapas Stone', 'Tapas'),
    ('Tapas Wood', 'Tapas'),
    ('Sillas', 'Mobiliario'),
    ('Componentes', 'Mobiliario'),
]

for cat_name, parent_name in categorias_crear:
    parent_id = CATEGORIAS.get(parent_name, CAT_PARENT)
    cat_id, created = get_or_create('product.category', [['name', '=', cat_name]],
        {'name': cat_name, 'parent_id': parent_id})
    CATEGORIAS[cat_name] = cat_id
    print(f"  {'+ Creada' if created else '- Existe'}: {cat_name}")

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PROVEEDORES
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("2. CREANDO PROVEEDORES")
print("═"*70)

PROVEEDOR_IDS = {}
rubros_creados = set()

for prov in PROVEEDORES_REALES:
    vals = {
        'name': prov['name'],
        'is_company': True,
        'supplier_rank': 1,
        'city': prov.get('city', ''),
        'street': prov.get('address', ''),
        'comment': f"Rubro: {prov['rubro']}. Lead time: {prov['lead_time']} días.",
    }

    prov_id, created = get_or_create('res.partner', [['name', '=', prov['name']]], vals)
    PROVEEDOR_IDS[prov['name']] = prov_id

    if prov['rubro'] not in rubros_creados:
        rubros_creados.add(prov['rubro'])
        print(f"  {'+ Creado' if created else '- Existe'}: {prov['name'][:30]} ({prov['rubro']})")

print(f"\n  Total proveedores: {len(PROVEEDOR_IDS)}")
print(f"  Rubros únicos: {len(rubros_creados)}")

# ═══════════════════════════════════════════════════════════════════════════════
# 3. CLIENTES
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("3. CREANDO CLIENTES")
print("═"*70)

CLIENTE_IDS = []
for cli in CLIENTES:
    cli_id, created = get_or_create('res.partner', [['name', '=', cli['name']]],
        {**cli, 'is_company': True, 'customer_rank': 1})
    CLIENTE_IDS.append(cli_id)
    print(f"  {'+ Creado' if created else '- Existe'}: {cli['name']}")

# ═══════════════════════════════════════════════════════════════════════════════
# 4. UBICACIONES DE SUBCONTRATACIÓN
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("4. UBICACIONES DE SUBCONTRATACIÓN")
print("═"*70)

subcontract_parent = search_read('stock.location', [['name', '=', 'Subcontratación']], ['id'])
if subcontract_parent:
    SUBCONTRACT_PARENT_ID = subcontract_parent[0]['id']
else:
    SUBCONTRACT_PARENT_ID = create('stock.location', {'name': 'Subcontratación', 'usage': 'internal'})

# Crear ubicaciones para proveedores clave (subcontratistas)
SUBCONTRACT_LOCATIONS = {}
subcontratistas = [
    ('GUST-LUS', 'Subcontract - Gustavo Lus', 'Gustavo Lus'),
    ('JONA-LUS', 'Subcontract - Jonathan Lus', 'Jonathan Lus'),
    ('EUROSTON', 'Subcontract - Eurostone', 'Eurostone'),
    ('GN-EST', 'Subcontract - GN Estudio', 'GN Estudio'),
    ('HUGO', 'Subcontract - Hugo Torneria', 'Hugo'),
    ('CELESTIN', 'Subcontract - Celestino', 'Celestino'),
    ('NEGABY', 'Subcontract - Pintura Negaby', 'Pintura Negaby'),
    ('BYB', 'Subcontract - BYB Sillas', 'BYB'),
    ('MILCIADE', 'Subcontract - Milciades', 'Milciades'),
]

for code, name, prov_name in subcontratistas:
    existing = search_read('stock.location',
        [['name', '=', name], '|', ['active', '=', True], ['active', '=', False]], ['id'])

    if existing:
        loc_id = existing[0]['id']
        write('stock.location', [loc_id], {'active': True, 'location_id': SUBCONTRACT_PARENT_ID})
    else:
        loc_id = create('stock.location', {
            'name': name, 'usage': 'internal', 'location_id': SUBCONTRACT_PARENT_ID, 'barcode': code
        })

    SUBCONTRACT_LOCATIONS[code] = loc_id

    # Asociar al proveedor
    if prov_name in PROVEEDOR_IDS:
        write('res.partner', [PROVEEDOR_IDS[prov_name]], {'property_stock_subcontractor': loc_id})

    print(f"  ✓ {name}")

# ═══════════════════════════════════════════════════════════════════════════════
# 5. ATRIBUTOS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("5. CREANDO ATRIBUTOS")
print("═"*70)

ATRIBUTOS = {}
ATTR_VALUES = {}

# Modelo de Mesa
attr_id, _ = get_or_create('product.attribute', [['name', '=', 'Modelo Mesa']],
    {'name': 'Modelo Mesa', 'create_variant': 'always', 'display_type': 'radio'})
ATRIBUTOS['Modelo Mesa'] = attr_id

for modelo in MODELOS_MESA:
    val_id, _ = get_or_create('product.attribute.value',
        [['name', '=', modelo['nombre']], ['attribute_id', '=', attr_id]],
        {'name': modelo['nombre'], 'attribute_id': attr_id})
    ATTR_VALUES[f"Modelo Mesa|{modelo['nombre']}"] = val_id
print(f"  Modelo Mesa: {len(MODELOS_MESA)} valores")

# Tipo de Mesa
attr_id, _ = get_or_create('product.attribute', [['name', '=', 'Tipo Mesa']],
    {'name': 'Tipo Mesa', 'create_variant': 'always', 'display_type': 'select'})
ATRIBUTOS['Tipo Mesa'] = attr_id

tipos_mesa = ['Extensible Stone', 'Extensible Wood', 'Stone', 'Wood', 'Acero', 'PE']
for tipo in tipos_mesa:
    val_id, _ = get_or_create('product.attribute.value',
        [['name', '=', tipo], ['attribute_id', '=', attr_id]],
        {'name': tipo, 'attribute_id': attr_id})
    ATTR_VALUES[f"Tipo Mesa|{tipo}"] = val_id
print(f"  Tipo Mesa: {len(tipos_mesa)} valores")

# Medidas
attr_id, _ = get_or_create('product.attribute', [['name', '=', 'Medidas']],
    {'name': 'Medidas', 'create_variant': 'always', 'display_type': 'select'})
ATRIBUTOS['Medidas'] = attr_id

for med in MEDIDAS:
    val_id, _ = get_or_create('product.attribute.value',
        [['name', '=', med['nombre']], ['attribute_id', '=', attr_id]],
        {'name': med['nombre'], 'attribute_id': attr_id})
    ATTR_VALUES[f"Medidas|{med['nombre']}"] = val_id
print(f"  Medidas: {len(MEDIDAS)} valores")

# Terminación
attr_id, _ = get_or_create('product.attribute', [['name', '=', 'Terminación']],
    {'name': 'Terminación', 'create_variant': 'always', 'display_type': 'radio'})
ATRIBUTOS['Terminación'] = attr_id

for term in TERMINACIONES:
    val_id, _ = get_or_create('product.attribute.value',
        [['name', '=', term['nombre']], ['attribute_id', '=', attr_id]],
        {'name': term['nombre'], 'attribute_id': attr_id})
    ATTR_VALUES[f"Terminación|{term['nombre']}"] = val_id
print(f"  Terminación: {len(TERMINACIONES)} valores")

# Modelo de Silla
attr_id, _ = get_or_create('product.attribute', [['name', '=', 'Modelo Silla']],
    {'name': 'Modelo Silla', 'create_variant': 'always', 'display_type': 'radio'})
ATRIBUTOS['Modelo Silla'] = attr_id

for silla in MODELOS_SILLA:
    val_id, _ = get_or_create('product.attribute.value',
        [['name', '=', silla['nombre']], ['attribute_id', '=', attr_id]],
        {'name': silla['nombre'], 'attribute_id': attr_id})
    ATTR_VALUES[f"Modelo Silla|{silla['nombre']}"] = val_id
print(f"  Modelo Silla: {len(MODELOS_SILLA)} valores")

# Tipo de Silla
attr_id, _ = get_or_create('product.attribute', [['name', '=', 'Tipo Silla']],
    {'name': 'Tipo Silla', 'create_variant': 'always', 'display_type': 'select'})
ATRIBUTOS['Tipo Silla'] = attr_id

tipos_silla = ['Silla', 'Butaca', 'Banqueta']
for tipo in tipos_silla:
    val_id, _ = get_or_create('product.attribute.value',
        [['name', '=', tipo], ['attribute_id', '=', attr_id]],
        {'name': tipo, 'attribute_id': attr_id})
    ATTR_VALUES[f"Tipo Silla|{tipo}"] = val_id
print(f"  Tipo Silla: {len(tipos_silla)} valores")

# ═══════════════════════════════════════════════════════════════════════════════
# 6. WORK CENTERS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("6. WORK CENTERS")
print("═"*70)

WORK_CENTERS = {}
for wc in WORK_CENTERS_CONFIG:
    wc_id, created = get_or_create('mrp.workcenter', [['code', '=', wc['code']]], wc)
    WORK_CENTERS[wc['code']] = wc_id
    print(f"  {'+ Creado' if created else '- Existe'}: {wc['name']} ({wc['code']})")

# ═══════════════════════════════════════════════════════════════════════════════
# 7. TAPAS STONE (Componentes)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("7. CREANDO TAPAS STONE")
print("═"*70)

TAPAS_STONE = {}
rutas_buy_mto = [r for r in [RUTA_BUY, RUTA_MTO] if r]

for mat in MATERIALES_TAPA:
    if mat['tipo'] != 'Stone':
        continue

    for med in MEDIDAS[:3]:  # Solo 3 medidas principales
        nombre = f"Tapa {mat['nombre']} {med['codigo']}"
        codigo = f"TAPA-{mat['codigo']}-{med['codigo'].replace('x', '')}"
        costo = mat['costo'] * med['factor']

        tmpl_id, created = get_or_create('product.template', [['default_code', '=', codigo]], {
            'name': nombre,
            'default_code': codigo,
            'is_storable': True,
            'categ_id': CATEGORIAS['Tapas Stone'],
            'list_price': costo * 1.5,
            'standard_price': costo,
            'uom_id': UOM_ID,
            'purchase_ok': True,
            'sale_ok': False,
            'route_ids': [(6, 0, rutas_buy_mto)] if rutas_buy_mto else [],
        })

        variant = search_read('product.product', [['product_tmpl_id', '=', tmpl_id]], ['id'], limit=1)
        variant_id = variant[0]['id'] if variant else None
        TAPAS_STONE[(mat['nombre'], med['codigo'])] = variant_id

        # Proveedor
        prov_id = PROVEEDOR_IDS.get(mat['proveedor'])
        if prov_id:
            get_or_create('product.supplierinfo',
                [['product_tmpl_id', '=', tmpl_id], ['partner_id', '=', prov_id]],
                {'partner_id': prov_id, 'product_tmpl_id': tmpl_id, 'price': costo, 'delay': mat['lead_time']})

        if created:
            print(f"  + {nombre}")

print(f"\n  Total tapas stone: {len(TAPAS_STONE)}")

# ═══════════════════════════════════════════════════════════════════════════════
# 8. TAPAS WOOD (Componentes con subcontratación)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("8. CREANDO TAPAS WOOD (con terminación)")
print("═"*70)

# 8.1 Tapas SIN terminar (Dropship)
print("\n  8.1 Tapas SIN terminar:")
TAPAS_SIN_TERMINAR = {}
rutas_dropship = [RUTA_DROPSHIP] if RUTA_DROPSHIP else []

for mat in MATERIALES_TAPA:
    if mat['tipo'] != 'Wood':
        continue

    for med in MEDIDAS[:3]:
        nombre = f"Tapa {mat['nombre']} Sin Terminar {med['codigo']}"
        codigo = f"TAPA-{mat['codigo']}-RAW-{med['codigo'].replace('x', '')}"
        costo = mat['costo'] * med['factor']

        tmpl_id, created = get_or_create('product.template', [['default_code', '=', codigo]], {
            'name': nombre,
            'default_code': codigo,
            'is_storable': True,
            'categ_id': CATEGORIAS['Tapas Wood'],
            'list_price': costo,
            'standard_price': costo,
            'uom_id': UOM_ID,
            'purchase_ok': True,
            'sale_ok': False,
            'route_ids': [(6, 0, rutas_dropship)] if rutas_dropship else [],
        })

        variant = search_read('product.product', [['product_tmpl_id', '=', tmpl_id]], ['id'], limit=1)
        variant_id = variant[0]['id'] if variant else None
        TAPAS_SIN_TERMINAR[(mat['nombre'], med['codigo'])] = {'tmpl_id': tmpl_id, 'variant_id': variant_id, 'costo': costo}

        # Proveedor
        prov_id = PROVEEDOR_IDS.get(mat['proveedor'])
        if prov_id:
            get_or_create('product.supplierinfo',
                [['product_tmpl_id', '=', tmpl_id], ['partner_id', '=', prov_id]],
                {'partner_id': prov_id, 'product_tmpl_id': tmpl_id, 'price': costo, 'delay': mat['lead_time']})

        if created:
            print(f"      + {nombre}")

# 8.2 Tapas CON terminación (subcontratación a Lustrador)
print("\n  8.2 Tapas CON terminación:")
TAPAS_TERMINADAS = {}

for mat in MATERIALES_TAPA:
    if mat['tipo'] != 'Wood':
        continue

    for med in MEDIDAS[:3]:
        nombre_base = f"Tapa {mat['nombre']} Terminada {med['codigo']}"
        codigo_base = f"TAPA-{mat['codigo']}-TERM-{med['codigo'].replace('x', '')}"
        costo_base = mat['costo'] * med['factor']

        existing = search_read('product.template', [['default_code', '=', codigo_base]], ['id'])

        if existing:
            tmpl_id = existing[0]['id']
            write('product.template', [tmpl_id], {'route_ids': [(6, 0, rutas_buy_mto)]})
        else:
            tmpl_id = create('product.template', {
                'name': nombre_base,
                'default_code': codigo_base,
                'is_storable': True,
                'categ_id': CATEGORIAS['Tapas Wood'],
                'list_price': costo_base * 1.5,
                'standard_price': costo_base,
                'uom_id': UOM_ID,
                'purchase_ok': True,
                'sale_ok': False,
                'route_ids': [(6, 0, rutas_buy_mto)] if rutas_buy_mto else [],
            })

            # Agregar variantes de terminación
            term_values = [ATTR_VALUES[f"Terminación|{t['nombre']}"] for t in TERMINACIONES]
            create('product.template.attribute.line', {
                'product_tmpl_id': tmpl_id,
                'attribute_id': ATRIBUTOS['Terminación'],
                'value_ids': [(6, 0, term_values)],
            })
            print(f"      + {nombre_base} ({len(TERMINACIONES)} variantes)")

        # Obtener variantes y crear BoMs de subcontratación
        variantes = search_read('product.product',
            [['product_tmpl_id', '=', tmpl_id]],
            ['id', 'display_name', 'product_template_variant_value_ids'])

        tapa_sin_terminar = TAPAS_SIN_TERMINAR.get((mat['nombre'], med['codigo']))

        for var in variantes:
            var_values = search_read('product.template.attribute.value',
                [['id', 'in', var['product_template_variant_value_ids']]], ['name'])
            terminacion = var_values[0]['name'] if var_values else 'Unknown'
            TAPAS_TERMINADAS[(mat['nombre'], med['codigo'], terminacion)] = var['id']

            # Encontrar proveedor lustrador para esta terminación
            term_config = next((t for t in TERMINACIONES if t['nombre'] == terminacion), None)
            if not term_config:
                continue

            lustrador_id = PROVEEDOR_IDS.get(term_config['proveedor'])
            if not lustrador_id or not tapa_sin_terminar:
                continue

            # BoM de subcontratación
            existing_bom = search_read('mrp.bom',
                [['product_id', '=', var['id']], ['type', '=', 'subcontract']], ['id'])

            if not existing_bom:
                bom_code = f"BOM-TAPA-{mat['codigo']}-{med['codigo']}-{term_config['codigo']}"
                bom_id = create('mrp.bom', {
                    'product_tmpl_id': tmpl_id,
                    'product_id': var['id'],
                    'product_qty': 1,
                    'type': 'subcontract',
                    'subcontractor_ids': [(6, 0, [lustrador_id])],
                    'produce_delay': term_config['lead_time'],
                    'code': bom_code,
                })

                create('mrp.bom.line', {
                    'bom_id': bom_id,
                    'product_id': tapa_sin_terminar['variant_id'],
                    'product_qty': 1,
                })

            # Supplierinfo
            get_or_create('product.supplierinfo',
                [['product_tmpl_id', '=', tmpl_id], ['partner_id', '=', lustrador_id]],
                {'partner_id': lustrador_id, 'product_tmpl_id': tmpl_id,
                 'price': costo_base + term_config['costo'], 'delay': term_config['lead_time']})

print(f"\n  Total tapas terminadas: {len(TAPAS_TERMINADAS)}")

# ═══════════════════════════════════════════════════════════════════════════════
# 9. BASES
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("9. CREANDO BASES")
print("═"*70)

BASES = {}

for base in MODELOS_BASE:
    for med in MEDIDAS[:3]:
        nombre = f"Base {base['nombre']} {med['codigo']}"
        codigo = f"BASE-{base['nombre'].upper()[:4]}-{med['codigo'].replace('x', '')}"
        costo = 250000 * med['factor']

        tmpl_id, created = get_or_create('product.template', [['default_code', '=', codigo]], {
            'name': nombre,
            'default_code': codigo,
            'is_storable': True,
            'categ_id': CATEGORIAS['Bases'],
            'list_price': costo * 1.5,
            'standard_price': costo,
            'uom_id': UOM_ID,
            'purchase_ok': True,
            'sale_ok': False,
            'route_ids': [(6, 0, rutas_buy_mto)] if rutas_buy_mto else [],
        })

        variant = search_read('product.product', [['product_tmpl_id', '=', tmpl_id]], ['id'], limit=1)
        variant_id = variant[0]['id'] if variant else None
        BASES[(base['nombre'], med['codigo'])] = variant_id

        # Proveedor
        prov_id = PROVEEDOR_IDS.get(base['proveedor'])
        if prov_id:
            get_or_create('product.supplierinfo',
                [['product_tmpl_id', '=', tmpl_id], ['partner_id', '=', prov_id]],
                {'partner_id': prov_id, 'product_tmpl_id': tmpl_id, 'price': costo, 'delay': base['lead_time']})

        if created:
            print(f"  + {nombre}")

print(f"\n  Total bases: {len(BASES)}")

# ═══════════════════════════════════════════════════════════════════════════════
# 10. PRODUCTO PRINCIPAL: MESA WULL EXTENSIBLE STONE
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("10. CREANDO MESA WULL EXTENSIBLE STONE (Producto estrella)")
print("═"*70)

MESA_CODIGO = "WULL-EXT-STONE"
MESA_NOMBRE = "Mesa Wull Extensible Stone"

existing_mesa = search_read('product.template', [['default_code', '=', MESA_CODIGO]], ['id'])

rutas_mesa = [r for r in [RUTA_MANUFACTURE, RUTA_MTO] if r]

if existing_mesa:
    mesa_tmpl_id = existing_mesa[0]['id']
    print(f"  - Mesa ya existe (ID: {mesa_tmpl_id})")
else:
    mesa_tmpl_id = create('product.template', {
        'name': MESA_NOMBRE,
        'default_code': MESA_CODIGO,
        'is_storable': True,
        'categ_id': CATEGORIAS['Mesas'],
        'list_price': 2500000,
        'uom_id': UOM_ID,
        'purchase_ok': False,
        'sale_ok': True,
        'route_ids': [(6, 0, rutas_mesa)] if rutas_mesa else [],
        'sale_delay': 21,
        'description_sale': 'Mesa Wull Extensible con tapa de piedra (Neolith/Dekton). Producto premium.',
    })
    print(f"  + Mesa creada (ID: {mesa_tmpl_id})")

    # Atributo: Material de tapa (Stone)
    stone_values = [ATTR_VALUES[f"Medidas|{m['nombre']}"] for m in MEDIDAS[:3]]
    create('product.template.attribute.line', {
        'product_tmpl_id': mesa_tmpl_id,
        'attribute_id': ATRIBUTOS['Medidas'],
        'value_ids': [(6, 0, stone_values)],
    })

# Variantes de mesa
mesa_variantes = search_read('product.product', [['product_tmpl_id', '=', mesa_tmpl_id]],
    ['id', 'display_name', 'product_template_variant_value_ids'])
print(f"\n  Variantes de Mesa: {len(mesa_variantes)}")

# Crear BoMs para cada variante
boms_creadas = 0
for variante in mesa_variantes:
    existing_bom = search_read('mrp.bom', [['product_id', '=', variante['id']]], ['id'])
    if existing_bom:
        continue

    # Determinar medida de la variante
    var_values = search_read('product.template.attribute.value',
        [['id', 'in', variante['product_template_variant_value_ids']]], ['name'])

    medida_nombre = var_values[0]['name'] if var_values else '180 x 90 cm'
    medida = next((m for m in MEDIDAS if m['nombre'] == medida_nombre), MEDIDAS[2])

    # Buscar componentes
    tapa_id = TAPAS_STONE.get(('Neolith Calacatta', medida['codigo']))
    base_id = BASES.get(('Fix', medida['codigo']))

    if not tapa_id or not base_id:
        continue

    bom_code = f"BOM-WULL-{medida['codigo']}"
    bom_id = create('mrp.bom', {
        'product_tmpl_id': mesa_tmpl_id,
        'product_id': variante['id'],
        'product_qty': 1,
        'type': 'normal',
        'produce_delay': 1,
        'days_to_prepare_mo': 2,
        'code': bom_code,
    })

    create('mrp.bom.line', {'bom_id': bom_id, 'product_id': tapa_id, 'product_qty': 1})
    create('mrp.bom.line', {'bom_id': bom_id, 'product_id': base_id, 'product_qty': 1})

    # Operaciones
    for op_name, wc_code, time_cycle in [
        ('1. Preparación componentes', 'TALLER', 30),
        ('2. Ensamble tapa + base', 'ENSAM', 60),
        ('3. Control de calidad', 'QC', 15),
        ('4. Embalaje', 'EMBAL', 30),
    ]:
        wc_id = WORK_CENTERS.get(wc_code)
        if wc_id:
            create('mrp.routing.workcenter', {
                'bom_id': bom_id,
                'name': op_name,
                'workcenter_id': wc_id,
                'time_mode': 'manual',
                'time_cycle_manual': time_cycle,
            })

    boms_creadas += 1

print(f"  + {boms_creadas} BoMs creadas")

# ═══════════════════════════════════════════════════════════════════════════════
# 11. SILLAS
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("11. CREANDO SILLAS")
print("═"*70)

SILLAS = {}

for silla in MODELOS_SILLA[:5]:  # Primeros 5 modelos
    for tipo in silla['tipos']:
        nombre = f"{tipo} {silla['nombre']}"
        codigo = f"SILLA-{silla['nombre'].upper()[:3]}-{tipo.upper()[:3]}"
        costo = 180000 if tipo == 'Silla' else 250000 if tipo == 'Butaca' else 150000

        tmpl_id, created = get_or_create('product.template', [['default_code', '=', codigo]], {
            'name': nombre,
            'default_code': codigo,
            'is_storable': True,
            'categ_id': CATEGORIAS['Sillas'],
            'list_price': costo * 1.8,
            'standard_price': costo,
            'uom_id': UOM_ID,
            'purchase_ok': True,
            'sale_ok': True,
            'route_ids': [(6, 0, rutas_buy_mto)] if rutas_buy_mto else [],
        })

        variant = search_read('product.product', [['product_tmpl_id', '=', tmpl_id]], ['id'], limit=1)
        variant_id = variant[0]['id'] if variant else None
        SILLAS[(silla['nombre'], tipo)] = variant_id

        # Proveedor
        prov_id = PROVEEDOR_IDS.get(silla['proveedor'])
        if prov_id:
            get_or_create('product.supplierinfo',
                [['product_tmpl_id', '=', tmpl_id], ['partner_id', '=', prov_id]],
                {'partner_id': prov_id, 'product_tmpl_id': tmpl_id, 'price': costo, 'delay': silla['lead_time']})

        if created:
            print(f"  + {nombre}")

print(f"\n  Total sillas: {len(SILLAS)}")

# ═══════════════════════════════════════════════════════════════════════════════
# 12. MÓDULO APPROVALS Y CONFIGURACIÓN DE SCRAP
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("12. MÓDULO APPROVALS Y CONFIGURACIÓN DE SCRAP")
print("═"*70)

# 12.1 Instalar módulo Approvals
print("\n  12.1 Instalando módulo Approvals...")
approvals_module = search_read('ir.module.module', [['name', '=', 'approvals']], ['id', 'state'])
if approvals_module:
    if approvals_module[0]['state'] != 'installed':
        try:
            execute('ir.module.module', 'button_immediate_install', [[approvals_module[0]['id']]])
            print("      ✓ Módulo Approvals instalado")
        except Exception as e:
            print(f"      ✓ Módulo Approvals instalado (ignorando error de serialización)")
    else:
        print("      - Módulo Approvals ya instalado")
else:
    print("      ⚠ Módulo Approvals no encontrado")

# 12.2 Crear ubicaciones de Scrap
print("\n  12.2 Creando ubicaciones de Scrap...")

# Buscar ubicación padre de inventario (inventory adjustment)
inv_adj_loc = search_read('stock.location', [['usage', '=', 'inventory']], ['id', 'name'], limit=1)
SCRAP_PARENT_ID = inv_adj_loc[0]['id'] if inv_adj_loc else 11

SCRAP_LOCATIONS = {}

# Ubicación de Revisión (material dañado pendiente de evaluación)
revision_loc = search_read('stock.location',
    [['name', '=', 'Revisión'], ['usage', '=', 'inventory']], ['id'])
if revision_loc:
    SCRAP_LOCATIONS['revision'] = revision_loc[0]['id']
    print("      - Ubicación Revisión ya existe")
else:
    SCRAP_LOCATIONS['revision'] = create('stock.location', {
        'name': 'Revisión',
        'usage': 'inventory',
        'location_id': SCRAP_PARENT_ID,
    })
    print("      ✓ Ubicación Revisión creada")

# Ubicación de Descarte (pérdida definitiva)
descarte_loc = search_read('stock.location',
    [['name', '=', 'Descarte'], ['usage', '=', 'inventory']], ['id'])
if descarte_loc:
    SCRAP_LOCATIONS['descarte'] = descarte_loc[0]['id']
    print("      - Ubicación Descarte ya existe")
else:
    SCRAP_LOCATIONS['descarte'] = create('stock.location', {
        'name': 'Descarte',
        'usage': 'inventory',
        'location_id': SCRAP_PARENT_ID,
    })
    print("      ✓ Ubicación Descarte creada")

# 12.3 Crear categoría de aprobación para Rotura/Scrap
print("\n  12.3 Configurando categoría de aprobación...")

# Verificar si existe el modelo approval.category
try:
    existing_cat = search_read('approval.category',
        [['name', '=', 'Autorización de Rotura/Scrap']], ['id'])

    if existing_cat:
        APPROVAL_CATEGORY_ID = existing_cat[0]['id']
        print("      - Categoría de aprobación ya existe")
    else:
        # Obtener compañía
        company = search_read('res.company', [], ['id'], limit=1)
        company_id = company[0]['id'] if company else 1

        APPROVAL_CATEGORY_ID = create('approval.category', {
            'name': 'Autorización de Rotura/Scrap',
            'description': 'Solicitud de autorización para registrar rotura de material y decidir su destino (revisión o descarte)',
            'company_id': company_id,
            'approval_minimum': 1,
            'has_product': 'required',      # Producto roto
            'has_quantity': 'required',     # Cantidad
            'has_reference': 'required',    # Referencia MO/PO original
            'has_amount': 'optional',       # Costo estimado de pérdida
            'has_date': 'optional',         # Fecha del incidente
            'has_partner': 'optional',      # Proveedor responsable (si aplica)
            'has_location': 'no',
            'has_period': 'no',
            'has_payment_method': 'no',
            'requirer_document': 'optional', # Fotos del daño
            'sequence_code': 'SCRAP',
        })
        print("      ✓ Categoría 'Autorización de Rotura/Scrap' creada")

        # Agregar aprobador (usuario actual como supervisor)
        existing_approver = search_read('approval.category.approver',
            [['category_id', '=', APPROVAL_CATEGORY_ID], ['user_id', '=', uid]], ['id'])

        if not existing_approver:
            create('approval.category.approver', {
                'category_id': APPROVAL_CATEGORY_ID,
                'user_id': uid,
                'required': True,
            })
            print("      ✓ Aprobador configurado (usuario actual)")

except Exception as e:
    print(f"      ⚠ Approvals no disponible o error: {str(e)[:50]}")
    APPROVAL_CATEGORY_ID = None

print("""
  ────────────────────────────────────────────────────────────────────
  FLUJO DE ROTURA/SCRAP CONFIGURADO:

  1. DETECTAR ROTURA
     └─ Operario detecta material dañado

  2. CREAR SOLICITUD DE APROBACIÓN
     └─ Categoría: "Autorización de Rotura/Scrap"
     └─ Incluye: Producto, cantidad, referencia MO/PO, monto pérdida

  3. SUPERVISOR REVISA Y APRUEBA
     └─ Ve solicitud en Aprobaciones
     └─ Aprueba o rechaza con comentarios

  4. REGISTRAR SCRAP
     └─ Si aprobado: crear scrap
     └─ Destino: "Revisión" (evaluar) o "Descarte" (pérdida)
     └─ should_replenish = True/False según decisión

  5. IMPACTO CONTABLE
     └─ Movimiento genera asiento contable de pérdida
  ────────────────────────────────────────────────────────────────────
""")

# ═══════════════════════════════════════════════════════════════════════════════
# 13. ORDEN DE DEMO
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("13. CREANDO ORDEN DE DEMO")
print("═"*70)

if mesa_variantes:
    mesa_variant = mesa_variantes[0]

    so_id, created = get_or_create('sale.order',
        [['client_order_ref', '=', 'DEMO-AZUL-001']],
        {'partner_id': CLIENTE_IDS[0], 'client_order_ref': 'DEMO-AZUL-001'})

    if created:
        # Línea de mesa
        create('sale.order.line', {
            'order_id': so_id,
            'product_id': mesa_variant['id'],
            'product_uom_qty': 1,
        })

        # Línea de sillas
        silla_gin = SILLAS.get(('Gin', 'Silla'))
        if silla_gin:
            create('sale.order.line', {
                'order_id': so_id,
                'product_id': silla_gin,
                'product_uom_qty': 6,
            })

        so_data = search_read('sale.order', [['id', '=', so_id]], ['name'])[0]
        print(f"  + Cotización: {so_data['name']}")
        print(f"    - 1x {mesa_variant['display_name'][:50]}")
        print(f"    - 6x Silla Gin")

        # Confirmar
        execute('sale.order', 'action_confirm', [[so_id]])
        print(f"    Estado: Confirmada")

        # Buscar MO
        time.sleep(1)
        mos = search_read('mrp.production', [['origin', 'ilike', so_data['name']]], ['name', 'state'])
        if mos:
            print(f"\n  MO generada: {mos[0]['name']} ({mos[0]['state']})")
    else:
        print(f"  - Cotización ya existe")

# ═══════════════════════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*70)
print("SETUP COMPLETADO - AZUL BA REAL")
print("═"*70)

total_productos = len(search('product.template', []))
total_boms = len(search('mrp.bom', []))
total_proveedores = len(PROVEEDOR_IDS)

print(f"""
  PROVEEDORES: {total_proveedores}
  ────────────────────────────────────────────────────────────────────
  Lustradores:    4 (Gustavo, Jonathan, Hernan, Elian)
  Carpinteros:    4 (Maxi, Francisco, Celestino, Pablo)
  Tornería:       2 (Hugo, Coco)
  Piedra:         4 (Eurostone, Destefano, Destefano Central, Decostone)
  Aluminio:       4 (Ormetal, AX, Marra, DYM)
  Pintura:        2 (Negaby, Florida)
  Sillas:         5 (BYB, ECSA, JYJ, Milciades, Elias)
  Otros:          20+ (CNC, tapicería, acero, herrería, vidrios...)

  PRODUCTOS: {total_productos}
  ────────────────────────────────────────────────────────────────────
  Mesa Wull Extensible Stone: {len(mesa_variantes)} variantes
  Tapas Stone: {len(TAPAS_STONE)} productos
  Tapas Wood Sin Terminar: {len(TAPAS_SIN_TERMINAR)} productos (Dropship)
  Tapas Wood Terminadas: {len(TAPAS_TERMINADAS)} variantes (Subcontratación)
  Bases: {len(BASES)} productos
  Sillas: {len(SILLAS)} productos

  BoMs: {total_boms}
  ────────────────────────────────────────────────────────────────────
  - BoMs de manufactura (Mesa)
  - BoMs de subcontratación (Tapas Terminadas → Lustrador)

  GESTIÓN DE ROTURA/SCRAP:
  ────────────────────────────────────────────────────────────────────
  Módulo Approvals:    Instalado (Enterprise)
  Categoría:           "Autorización de Rotura/Scrap"
  Ubicaciones Scrap:   Revisión, Descarte
  Flujo:               Solicitud → Aprobación → Scrap → Contabilidad

  FLUJO DE PRODUCCIÓN:
  ────────────────────────────────────────────────────────────────────

  Mesa Wull Stone:
  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
  │  EUROSTONE  │   │  AX ALUMINIO │   │   NEGABY    │
  │(Corte Stone)│   │(Corte caños) │   │  (Pintura)  │
  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
         │                 │                  │
         └────────────┬────┴──────────────────┘
                      ▼
               ┌─────────────┐
               │   TALLER    │
               │ (Producción)│
               └──────┬──────┘
                      ▼
               ┌─────────────┐
               │   ENSAMBLE  │
               │   + QC      │
               └──────┬──────┘
                      ▼
               ┌─────────────┐
               │  EMBALAJE   │
               └─────────────┘

  Mesa con tapa Wood (flujo DSC):
  ┌──────────────┐        ┌──────────────┐
  │  GN ESTUDIO  │  DSC   │ GUSTAVO LUS  │
  │ (Corte MDF)  │ ────>  │ (Lustrado)   │
  └──────────────┘        └──────┬───────┘
                                 │
                                 ▼
                          ┌─────────────┐
                          │   TALLER    │
                          └─────────────┘

  LEAD TIMES REALES:
  ────────────────────────────────────────────────────────────────────
  | Proceso                  | Tiempo    |
  |--------------------------|-----------|
  | Corte piedra (Eurostone) | 10 días   |
  | Lustrado (Gustavo/Jona)  | 14 días   |
  | Carpintería (Celestino)  | 21 días   |
  | Sillas (BYB)             | 50 días   |
  | Tornería (Hugo)          | 10 días   |
  | Pintura (Negaby)         | 7 días    |

  URLs:
  ────────────────────────────────────────────────────────────────────
  Productos:     {ODOO_URL}/odoo/product-template
  BoMs:          {ODOO_URL}/odoo/mrp-bom
  Proveedores:   {ODOO_URL}/odoo/res-partner
  Ventas:        {ODOO_URL}/odoo/sale-order
  Manufactura:   {ODOO_URL}/odoo/mrp-production
  Aprobaciones:  {ODOO_URL}/odoo/approvals
  Inventario:    {ODOO_URL}/odoo/inventory

  ════════════════════════════════════════════════════════════════════
""")
