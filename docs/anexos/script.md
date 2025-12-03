# Script de Automatización

Script Python para automatizar toda la configuración del demo.

## Descripción

El script `setup.py` automatiza:

- Configuración del sistema
- Creación de proveedores
- Creación de productos y variantes
- Creación de BoMs
- Creación de Work Centers
- Creación de Control Points de calidad
- Reglas de reabastecimiento (orderpoints) para PO automáticas
- Orden de demo para verificar el flujo

---

## Requisitos

- Python 3.8+
- Acceso XML-RPC a la instancia de Odoo
- Usuario con permisos de administrador
- Módulos instalados: Sales, Inventory, Purchase, Manufacturing, Quality

---

## Uso

### Ejecución Normal

```bash
python setup.py
```

Crea toda la configuración sin eliminar datos existentes.

### Limpiar y Recrear

```bash
python setup.py --limpiar
```

Elimina los datos de demo anteriores y los recrea.

---

## Configuración

Crear archivo `config.py` con las credenciales (copiar de `config.example.py`):

```python
# config.py
ODOO_URL = "https://tu-instancia.odoo.com"
ODOO_DB = "nombre_base_datos"
ODOO_USERNAME = "admin"
ODOO_PASSWORD = "tu_password"
```

!!! warning "Seguridad"
    El archivo `config.py` está en `.gitignore` para no exponer credenciales.

---

## Estructura del Script

```
setup.py
│
├── Sección 0: Configuración Avanzada
│   ├── Multi-step routes
│   ├── Ubicaciones de subcontratista
│   ├── Ubicaciones de tránsito
│   └── Picking Type "Envío a Lustrador" + Ruta resupply
│
├── Sección 1: Datos Base
│   ├── Rutas (MTO, Buy, Manufacture)
│   └── Categorías de productos
│
├── Sección 2: Proveedores
│   └── 5 proveedores con ubicaciones
│
├── Sección 3: Clientes
│   └── 2 clientes demo
│
├── Sección 4: Atributos
│   └── 4 atributos con valores
│       ├── Material Tapa (3 valores)
│       ├── Material Base (2 valores)
│       ├── Medidas (2 valores)
│       └── Terminación (4 valores incl. Sin Terminación)
│
├── Sección 5: Work Centers
│   └── 6 centros de trabajo
│
├── Sección 6: Bases Metálicas
│   └── 4 productos con BoM subcontratación
│
├── Sección 7: Tapas Mármol/Neolith
│   └── 4 productos con BoM subcontratación
│
├── Sección 8: Tapas de Madera
│   ├── Tapas Sin Terminar (2 productos + orderpoints + ruta resupply)
│   └── Tapas Terminadas (6 variantes con BoM)
│
├── Sección 9: Producto Final
│   └── Mesa Comedor Premium
│       ├── 48 variantes totales
│       └── 20 con BoM (combinaciones válidas)
│
├── Sección 10: BoMs Mesa
│   └── 20 BoMs con operaciones
│
├── Sección 11: Control de Calidad
│   └── 6 Control Points
│
└── Sección 12: Orden de Demo
    └── SO para verificar flujo
```

---

## Código del Script

```python
#!/usr/bin/env python3
"""
Setup Demo Completo - Odoo 19
Mueblería con MTO, Subcontratación y Control de Calidad
"""

import xmlrpc.client
import argparse

# === CONFIGURACIÓN ===
URL = "http://localhost:8069"
DB = "odoo_demo"
USER = "admin"
PASSWORD = "admin"

# === CONEXIÓN ===
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, PASSWORD, {})

if not uid:
    print("❌ Error de autenticación")
    exit(1)

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

def execute(model, method, *args, **kwargs):
    """Ejecuta método en modelo Odoo"""
    return models.execute_kw(DB, uid, PASSWORD, model, method, args, kwargs)

def search(model, domain, **kwargs):
    return execute(model, 'search', domain, **kwargs)

def read(model, ids, fields=None):
    return execute(model, 'read', ids, fields or [])

def create(model, vals):
    return execute(model, 'create', vals)

def write(model, ids, vals):
    return execute(model, 'write', ids, vals)

def search_read(model, domain, fields=None, **kwargs):
    return execute(model, 'search_read', domain, fields or [], **kwargs)

# === FUNCIONES AUXILIARES ===

def get_or_create(model, domain, vals):
    """Busca o crea un registro"""
    ids = search(model, domain, limit=1)
    if ids:
        return ids[0]
    return create(model, vals)

def get_route(route_name):
    """Obtiene ID de ruta por nombre"""
    routes = search_read('stock.route',
        [('name', 'ilike', route_name)],
        ['id', 'name'])
    return routes[0]['id'] if routes else None

# ... (resto del script)
```

---

## Descarga

El script completo está disponible en el repositorio:

```
/setup.py
/config.example.py
```

---

## Personalización

### Agregar Más Productos

```python
# En la sección de productos, agregar:
nuevo_producto = {
    'name': 'Nombre del Producto',
    'type': 'product',
    'default_code': 'CODIGO',
    'route_ids': [(6, 0, [route_mto, route_buy])],
}
producto_id = create('product.product', nuevo_producto)
```

### Agregar Más BoMs

```python
# Crear BoM
bom_vals = {
    'product_tmpl_id': producto_tmpl_id,
    'product_qty': 1,
    'type': 'normal',  # o 'subcontract'
    'bom_line_ids': [
        (0, 0, {'product_id': comp1_id, 'product_qty': 1}),
        (0, 0, {'product_id': comp2_id, 'product_qty': 2}),
    ]
}
bom_id = create('mrp.bom', bom_vals)
```

### Agregar Más Control Points

```python
# Crear Control Point
qc_vals = {
    'name': 'Nombre del Control',
    'title': 'Título descriptivo',
    'product_ids': [(6, 0, [producto_id])],
    'picking_type_ids': [(6, 0, [picking_type_id])],
    'test_type_id': test_type_passfail,
    'team_id': team_id,
}
qc_id = create('quality.point', qc_vals)
```

---

## Verificación Post-Ejecución

Después de ejecutar el script:

1. **Verificar proveedores**: Compras → Proveedores
2. **Verificar productos**: Inventario → Productos
3. **Verificar BoMs**: Manufactura → BoMs
4. **Verificar QC Points**: Calidad → Control Points
5. **Verificar orden demo**: Ventas → Pedidos

---

## Solución de Problemas

### Error de conexión

```
❌ Error de autenticación
```

**Solución**: Verificar URL, DB, USER y PASSWORD.

### Error de módulo no instalado

```
xmlrpc.client.Fault: Object 'quality.point' doesn't exist
```

**Solución**: Instalar el módulo Quality en Odoo.

### Error de permisos

```
Access Denied
```

**Solución**: Usar usuario con permisos de administrador.
