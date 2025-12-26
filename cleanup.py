#!/usr/bin/env python3
"""
Script de limpieza para Odoo - Azul BA Demo
Elimina todos los datos creados por setup.py
"""

import xmlrpc.client
from config import ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD


def connect():
    """Conectar a Odoo"""
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    if not uid:
        raise Exception("Error de autenticación")
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    return uid, models


def delete_records(models, uid, model, domain, name="registros"):
    """Eliminar registros de un modelo"""
    ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, model, 'search', [domain])
    if ids:
        try:
            models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, model, 'unlink', [ids])
            print(f"  ✓ {len(ids)} {name} eliminados")
        except Exception as e:
            print(f"  ✗ Error eliminando {name}: {e}")
    else:
        print(f"  - No hay {name} para eliminar")
    return len(ids) if ids else 0


def main():
    print("=" * 70)
    print("LIMPIEZA DE DATOS - AZUL BA")
    print("=" * 70)
    print(f"  URL: {ODOO_URL}")
    print(f"  DB: {ODOO_DB}")
    print()

    uid, models = connect()
    print(f"  Conectado como usuario ID: {uid}")
    print()

    # 1. Eliminar Quality Checks y Alerts primero
    print("=" * 70)
    print("1. ELIMINANDO QUALITY CONTROL")
    print("=" * 70)
    delete_records(models, uid, 'quality.check', [], "quality checks")
    delete_records(models, uid, 'quality.alert', [], "quality alerts")
    delete_records(models, uid, 'quality.point', [
        ('title', 'ilike', 'Tapa Madera')
    ], "quality points")

    # 2. Eliminar órdenes de venta
    print()
    print("=" * 70)
    print("2. ELIMINANDO ÓRDENES DE VENTA")
    print("=" * 70)

    # Cancelar primero las órdenes confirmadas
    sale_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'sale.order', 'search', [
        [('state', 'in', ['sale', 'done'])]
    ])
    if sale_ids:
        try:
            models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'sale.order', 'action_cancel', [sale_ids])
            print(f"  ✓ {len(sale_ids)} órdenes canceladas")
        except Exception as e:
            print(f"  ! Error cancelando órdenes: {e}")

    delete_records(models, uid, 'sale.order', [], "órdenes de venta")

    # 3. Eliminar órdenes de compra
    print()
    print("=" * 70)
    print("3. ELIMINANDO ÓRDENES DE COMPRA")
    print("=" * 70)

    # Cancelar primero
    po_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'purchase.order', 'search', [
        [('state', 'in', ['purchase', 'done'])]
    ])
    if po_ids:
        try:
            models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'purchase.order', 'button_cancel', [po_ids])
            print(f"  ✓ {len(po_ids)} POs canceladas")
        except Exception as e:
            print(f"  ! Error cancelando POs: {e}")

    delete_records(models, uid, 'purchase.order', [], "órdenes de compra")

    # 4. Eliminar MOs y Work Orders
    print()
    print("=" * 70)
    print("4. ELIMINANDO MANUFACTURA")
    print("=" * 70)

    # Cancelar MOs primero
    mo_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'mrp.production', 'search', [
        [('state', 'not in', ['cancel', 'draft'])]
    ])
    if mo_ids:
        try:
            models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'mrp.production', 'action_cancel', [mo_ids])
            print(f"  ✓ {len(mo_ids)} MOs canceladas")
        except Exception as e:
            print(f"  ! Error cancelando MOs: {e}")

    delete_records(models, uid, 'mrp.workorder', [], "work orders")
    delete_records(models, uid, 'mrp.production', [], "órdenes de manufactura")

    # 5. Eliminar pickings
    print()
    print("=" * 70)
    print("5. ELIMINANDO PICKINGS")
    print("=" * 70)

    # Cancelar pickings primero
    picking_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'stock.picking', 'search', [
        [('state', 'not in', ['cancel', 'draft'])]
    ])
    if picking_ids:
        try:
            models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'stock.picking', 'action_cancel', [picking_ids])
            print(f"  ✓ {len(picking_ids)} pickings cancelados")
        except Exception as e:
            print(f"  ! Error cancelando pickings: {e}")

    delete_records(models, uid, 'stock.picking', [], "pickings")

    # 6. Eliminar stock moves
    print()
    print("=" * 70)
    print("6. ELIMINANDO STOCK MOVES")
    print("=" * 70)
    delete_records(models, uid, 'stock.move', [], "stock moves")

    # 7. Eliminar BoMs
    print()
    print("=" * 70)
    print("7. ELIMINANDO BOMs")
    print("=" * 70)
    delete_records(models, uid, 'mrp.bom.line', [], "líneas de BoM")
    delete_records(models, uid, 'mrp.bom', [], "BoMs")

    # 8. Eliminar productos
    print()
    print("=" * 70)
    print("8. ELIMINANDO PRODUCTOS")
    print("=" * 70)

    # Productos específicos del demo
    productos_demo = [
        'Mesa Comedor Premium',
        'Base Acero Negro',
        'Base Acero Dorado',
        'Tapa Mármol Carrara',
        'Tapa Neolith Negro',
        'Tapa Madera Sin Terminar',
        'Tapa Madera Terminada',
    ]

    for producto in productos_demo:
        # Eliminar variantes primero
        variant_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.product', 'search', [
            [('name', 'ilike', producto)]
        ])
        if variant_ids:
            try:
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.product', 'unlink', [variant_ids])
                print(f"  ✓ {len(variant_ids)} variantes de '{producto}' eliminadas")
            except Exception as e:
                print(f"  ! Error eliminando variantes de '{producto}': {e}")

        # Eliminar templates
        template_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.template', 'search', [
            [('name', 'ilike', producto)]
        ])
        if template_ids:
            try:
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.template', 'unlink', [template_ids])
                print(f"  ✓ {len(template_ids)} templates de '{producto}' eliminados")
            except Exception as e:
                print(f"  ! Error eliminando templates de '{producto}': {e}")

    # 9. Eliminar supplierinfo
    print()
    print("=" * 70)
    print("9. ELIMINANDO SUPPLIERINFO")
    print("=" * 70)
    delete_records(models, uid, 'product.supplierinfo', [], "supplierinfo")

    # 10. Eliminar atributos
    print()
    print("=" * 70)
    print("10. ELIMINANDO ATRIBUTOS")
    print("=" * 70)

    atributos_demo = ['Material Tapa', 'Material Base', 'Medidas', 'Terminación']
    for attr_name in atributos_demo:
        # Eliminar valores primero
        value_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.attribute.value', 'search', [
            [('attribute_id.name', '=', attr_name)]
        ])
        if value_ids:
            try:
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.attribute.value', 'unlink', [value_ids])
                print(f"  ✓ Valores de '{attr_name}' eliminados")
            except Exception as e:
                print(f"  ! Error eliminando valores de '{attr_name}': {e}")

        # Eliminar atributo
        attr_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.attribute', 'search', [
            [('name', '=', attr_name)]
        ])
        if attr_ids:
            try:
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.attribute', 'unlink', [attr_ids])
                print(f"  ✓ Atributo '{attr_name}' eliminado")
            except Exception as e:
                print(f"  ! Error eliminando atributo '{attr_name}': {e}")

    # 11. Eliminar Work Centers
    print()
    print("=" * 70)
    print("11. ELIMINANDO WORK CENTERS")
    print("=" * 70)

    wc_names = ['Ensamble Final', 'Control de Calidad']
    for wc_name in wc_names:
        # Eliminar capacidades primero
        cap_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'mrp.workcenter.capacity', 'search', [
            [('workcenter_id.name', '=', wc_name)]
        ])
        if cap_ids:
            try:
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'mrp.workcenter.capacity', 'unlink', [cap_ids])
            except:
                pass

        wc_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'mrp.workcenter', 'search', [
            [('name', '=', wc_name)]
        ])
        if wc_ids:
            try:
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'mrp.workcenter', 'unlink', [wc_ids])
                print(f"  ✓ Work Center '{wc_name}' eliminado")
            except Exception as e:
                print(f"  ! Error eliminando '{wc_name}': {e}")

    # 12. Eliminar proveedores y clientes
    print()
    print("=" * 70)
    print("12. ELIMINANDO PROVEEDORES Y CLIENTES")
    print("=" * 70)

    partners_demo = [
        'Marmolería Del Sur',
        'Carpintería Artesanal Hnos. García',
        'Neolith Argentina',
        'Metalúrgica Precisión S.A.',
        'Lustres & Acabados Premium',
        'Estudio de Arquitectura Modernista',
        'Hotel Boutique La Estancia',
    ]

    for partner_name in partners_demo:
        partner_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'res.partner', 'search', [
            [('name', '=', partner_name)]
        ])
        if partner_ids:
            try:
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'res.partner', 'unlink', [partner_ids])
                print(f"  ✓ '{partner_name}' eliminado")
            except Exception as e:
                print(f"  ! Error eliminando '{partner_name}': {e}")

    # 13. Eliminar ubicaciones de subcontratista
    print()
    print("=" * 70)
    print("13. ELIMINANDO UBICACIONES DE SUBCONTRATISTA")
    print("=" * 70)

    loc_names = [
        'Subcontract - Carpintería Hnos. García',
        'Subcontract - Lustres & Acabados',
        'Subcontract - Metalúrgica Precisión',
        'Subcontract - Marmolería Del Sur',
        'Subcontract - Neolith Argentina',
    ]

    for loc_name in loc_names:
        loc_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'stock.location', 'search', [
            [('name', '=', loc_name)]
        ])
        if loc_ids:
            try:
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'stock.location', 'unlink', [loc_ids])
                print(f"  ✓ Ubicación '{loc_name}' eliminada")
            except Exception as e:
                print(f"  ! Error eliminando '{loc_name}': {e}")

    # 14. Eliminar categorías de producto
    print()
    print("=" * 70)
    print("14. ELIMINANDO CATEGORÍAS")
    print("=" * 70)

    cat_names = ['Bases', 'Tapas Intermedias', 'Tapas', 'Mesas', 'Mobiliario']
    for cat_name in cat_names:
        cat_ids = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.category', 'search', [
            [('name', '=', cat_name)]
        ])
        if cat_ids:
            try:
                models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.category', 'unlink', [cat_ids])
                print(f"  ✓ Categoría '{cat_name}' eliminada")
            except Exception as e:
                print(f"  ! Error eliminando '{cat_name}': {e}")

    print()
    print("=" * 70)
    print("LIMPIEZA COMPLETADA")
    print("=" * 70)
    print()
    print(f"  URL: {ODOO_URL}")
    print()


if __name__ == '__main__':
    main()
