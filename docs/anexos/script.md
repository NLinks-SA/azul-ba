# Script de Automatización

Script Python para automatizar toda la configuración del demo.

## Descripción

El script `setup.py` automatiza:

- Instalación de módulos necesarios
- Configuración del sistema (variantes, MTO, rutas, etc.)
- Creación de proveedores con ubicaciones de subcontratación
- Creación de productos y variantes
- Creación de BoMs (normales y subcontratación)
- Creación de Work Centers
- Configuración de Dropship Subcontractor
- Control de calidad en DSC Picking
- Orden de demo para verificar el flujo

---

## Requisitos

- Python 3.8+
- Acceso XML-RPC a la instancia de Odoo
- Usuario con permisos de administrador

---

## Uso

### Ejecución Normal

```bash
python setup.py
```

Instala módulos, aplica configuraciones y crea toda la demo.

### Limpiar y Recrear

```bash
python setup.py --limpiar
```

Elimina los datos de demo anteriores y los recrea.

### Saltar Instalación de Módulos

```bash
python setup.py --skip-install
```

Si los módulos ya están instalados, salta esa sección.

---

## Configuración

Crear archivo `config.py` con las credenciales:

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
├── Instalación de Módulos
│   ├── sale_management, purchase, mrp
│   ├── mrp_subcontracting
│   ├── stock_dropshipping
│   ├── mrp_subcontracting_dropshipping
│   └── quality_control
│
├── Configuración de Ajustes
│   ├── group_product_variant (Variantes)
│   ├── module_stock_dropshipping (Triangulación)
│   ├── replenish_on_order (MTO)
│   ├── group_stock_multi_locations (Ubicaciones)
│   ├── group_stock_adv_location (Rutas multi-paso)
│   ├── group_mrp_routings (Órdenes de trabajo)
│   └── module_mrp_subcontracting (Subcontratación)
│
├── Sección 0: Configuración Avanzada
│   ├── Almacén 1 paso (one_step / ship_only)
│   ├── Ubicaciones de subcontratista (5 proveedores)
│   ├── Jerarquía de ubicaciones para DSC
│   └── Picking Type DSC configurado
│
├── Sección 1: Datos Base
│   ├── Rutas (MTO, Buy, Manufacture, Dropship)
│   └── Categorías de productos
│
├── Sección 2: Proveedores
│   └── 5 proveedores con ubicaciones de subcontratación
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
│   └── 2 centros de trabajo (ENSAM, QC)
│
├── Sección 6: Bases Metálicas
│   └── 4 productos (Buy + MTO)
│
├── Sección 7: Tapas Mármol/Neolith
│   └── 4 productos (Buy + MTO)
│
├── Sección 8: Tapas de Madera
│   ├── 8.1 Tapas Sin Terminar (Dropship)
│   └── 8.2 Tapas Terminadas (subcontratación a Lustrador)
│
├── Sección 9: Producto Final
│   └── Mesa Comedor Premium
│       ├── 48 variantes totales
│       └── 20 con BoM (combinaciones válidas)
│
├── Sección 10: BoMs Mesa
│   └── 20 BoMs con operaciones
│
├── Sección 11: Operaciones BoMs
│   └── Consumo estricto + ready_to_produce=asap
│
├── Sección 12: Control de Calidad
│   └── QC en DSC Picking para Tapas Sin Terminar
│
└── Sección 13: Orden de Demo
    └── SO para verificar flujo
```

---

## Módulos Instalados

| Módulo | Descripción |
|--------|-------------|
| `sale_management` | Ventas |
| `purchase` | Compras |
| `mrp` | Fabricación |
| `mrp_subcontracting` | Subcontratación |
| `stock_dropshipping` | Triangulación (Dropship) |
| `mrp_subcontracting_dropshipping` | Dropship Subcontractor |
| `quality_control` | Control de Calidad |

---

## Configuraciones Habilitadas

| Configuración | Campo |
|---------------|-------|
| Variantes de producto | `group_product_variant` |
| Triangulación | `module_stock_dropshipping` |
| MTO | `replenish_on_order` |
| Ubicaciones | `group_stock_multi_locations` |
| Rutas multi-paso | `group_stock_adv_location` |
| Reporte de recepción | `group_stock_reception_report` |
| Órdenes de trabajo | `group_mrp_routings` |
| Subcontratación | `module_mrp_subcontracting` |

---

## Flujo Dropship Subcontractor

El script configura el flujo completo de Dropship Subcontractor:

```
SO → MO Mesa → PO Lustrador (subcontratación)
                            ↓ (confirmar PO)
                 Subcontract MO (necesita Tapa Sin Terminar)
                            ↓ (ruta Dropship)
                 PO Carpintería → DSC Picking (con QC) → Lustrador
```

### Configuración Clave

1. **Tapa Sin Terminar**: Ruta = solo **Dropship** (sin MTO)
2. **Picking Type DSC**: `default_location_dest_id` apunta a ubicación padre de subcontratación
3. **QC Point**: Asociado al Picking Type DSC

---

## Verificación Post-Ejecución

Después de ejecutar el script, verificar:

1. **Módulos**: Apps → Verificar que todos estén instalados
2. **Proveedores**: Compras → Proveedores (5 proveedores)
3. **Ubicaciones**: Inventario → Configuración → Ubicaciones → Subcontratación (5 hijos)
4. **Productos**: Inventario → Productos (Mesa + componentes)
5. **BoMs**: Manufactura → BoMs (26 total)
6. **QC Points**: Calidad → Control Points (1: DSC)
7. **Demo**: Ventas → Pedidos → S00001

---

## URLs de Verificación

El script muestra al final las URLs relevantes:

```
Productos:     {URL}/odoo/product-template
BoMs:          {URL}/odoo/mrp-bom
Work Centers:  {URL}/odoo/mrp-workcenter
Gantt:         {URL}/odoo/mrp-production?view_type=gantt
Work Orders:   {URL}/odoo/mrp-workorder
Compras:       {URL}/odoo/purchase-order
Ventas:        {URL}/odoo/sale-order
Quality:       {URL}/odoo/quality-point
Ubicaciones:   {URL}/odoo/stock-location
```

---

## Solución de Problemas

### Error de conexión

```
Error de autenticación
```

**Solución**: Verificar URL, DB, USERNAME y PASSWORD en `config.py`.

### Error de módulo no instalado

```
xmlrpc.client.Fault: Object 'quality.point' doesn't exist
```

**Solución**: Ejecutar `python setup.py` sin `--skip-install` para instalar módulos.

### Error de permisos

```
Access Denied
```

**Solución**: Usar usuario con permisos de administrador.

### Error en configuraciones

```
Error aplicando configuraciones
```

**Solución**: Algunos campos pueden no existir si los módulos no están completamente inicializados. Ejecutar el script nuevamente o aplicar configuraciones manualmente en Ajustes.
