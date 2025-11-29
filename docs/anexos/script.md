# Script de Automatización

Script Python para automatizar toda la configuración del demo.

## Descripción

El script `setup_demo_completo.py` automatiza:

- Configuración del sistema
- Creación de proveedores
- Creación de productos y variantes
- Creación de BoMs
- Creación de Work Centers
- Creación de Control Points de calidad
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
python setup_demo_completo.py
```

Crea toda la configuración sin eliminar datos existentes.

### Limpiar y Recrear

```bash
python setup_demo_completo.py --limpiar
```

Elimina los datos de demo anteriores y los recrea.

---

## Configuración

Al inicio del script, configurar las credenciales:

```python
# === CONFIGURACIÓN ===
URL = "http://localhost:8069"    # URL de Odoo
DB = "odoo_demo"                 # Nombre de la base de datos
USER = "admin"                   # Usuario
PASSWORD = "admin"               # Contraseña
```

---

## Estructura del Script

```
setup_demo_completo.py
│
├── Sección 0: Configuración Avanzada
│   ├── Multi-step routes
│   ├── Ubicaciones de subcontratista
│   └── Ubicaciones de tránsito
│
├── Sección 1: Proveedores
│   └── 5 proveedores con ubicaciones
│
├── Sección 2: Atributos
│   └── 4 atributos con valores
│
├── Sección 3: Categorías
│   └── Categoría "Muebles"
│
├── Sección 4-7: Productos
│   ├── Tapas sin terminar
│   ├── Tapas terminadas (variantes)
│   ├── Tapas mármol/neolith
│   └── Bases metálicas
│
├── Sección 8: Producto Final
│   └── Mesa Comedor Premium (12 variantes)
│
├── Sección 9: Work Centers
│   └── 6 centros de trabajo
│
├── Sección 10: BoMs Normales
│   └── 12 BoMs de Mesa
│
├── Sección 11: BoMs Subcontratación
│   └── 10 BoMs
│
├── Sección 12: Control de Calidad
│   └── 6 Control Points
│
└── Sección 13: Orden de Demo
    └── SO + confirmación
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
/setup_demo_completo.py
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
