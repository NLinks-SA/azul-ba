# Feature Request: Sale Order Traceability on DSC (Dropship Subcontractor) Pickings

## Summary

The `sale_id` field on DSC (Dropship Subcontractor) pickings is not populated, breaking the traceability chain from Sale Order to the dropship movement that delivers components to subcontractors.

## Affected Versions

- Odoo 17.0
- Odoo 18.0
- Odoo 19.0

## Modules Involved

- `mrp_subcontracting_dropshipping`
- `mrp_subcontracting`
- `sale_purchase_stock`
- `sale_stock`
- `sale_mrp`

## Current Behavior

When following this flow:

```
Sale Order (Mesa)
    └── Manufacturing Order (Mesa)
            └── Purchase Order (Lustrador - Subcontractor)
                    └── Subcontract MO (Tapa Terminada)
                            └── Purchase Order (Carpintería - Component supplier)
                                    └── DSC Picking (Carpintería → Lustrador)
```

The DSC Picking has an empty `sale_id` field, even though the entire chain originated from a Sale Order.

### Technical Analysis

The `sale_id` field on `stock.picking` is computed in `sale_stock/models/stock.py`:

```python
@api.depends('reference_ids.sale_ids', 'move_ids.sale_line_id.order_id')
def _compute_sale_id(self):
    for picking in self:
        picking.sale_id = picking.move_ids.sale_line_id.order_id
```

The problem is that `sale_line_id` is not propagated through the subcontracting chain:

1. **SO → MO**: `sale_line_id` is correctly set on the MO via `sale_mrp`
2. **MO → PO Subcontractor**: `sale_line_id` propagates to the receipt move
3. **PO Subcontractor → Subcontract MO**: `sale_line_id` is **NOT** propagated in `_prepare_subcontract_mo_vals()` (gap)
4. **Subcontract MO → PO Component → DSC Picking**: Without `sale_line_id` on the Subcontract MO, the DSC Picking moves don't have it either

Additionally, in `sale_purchase_stock/models/purchase_order.py`, the `sale_line_id` is only propagated to stock moves when the destination location is `customer` or `transit`:

```python
def _prepare_stock_moves(self, picking):
    res = super()._prepare_stock_moves(picking)
    for re in res:
        if self.sale_line_id and re.get('location_final_id'):
            final_loc = self.env['stock.location'].browse(re.get('location_final_id'))
            if final_loc.usage == 'customer' or final_loc.usage == 'transit':
                re['sale_line_id'] = self.sale_line_id.id
    return res
```

Since subcontractor locations have `usage = 'internal'` (required by Odoo's constraint in `mrp_subcontracting/models/stock_location.py`), the `sale_line_id` is never propagated to DSC pickings.

## Expected Behavior

The DSC Picking should have the `sale_id` field populated with the original Sale Order, enabling:

1. Full traceability from SO to all related operations
2. Visibility of the SO in the DSC Picking form ("Información adicional" section)
3. Ability to filter/search DSC Pickings by Sale Order
4. Complete audit trail for quality control purposes

## Business Impact

Without this traceability:

- Users cannot easily identify which customer order a DSC movement belongs to
- Quality Control on DSC Pickings lacks context about the final customer
- Reporting and analytics are incomplete
- Manual tracking is required to link DSC operations to sales

## Proposed Solution

### Option 1: Propagate `sale_line_id` through Subcontract MO (Recommended)

Modify `_prepare_subcontract_mo_vals()` in `mrp_subcontracting/models/stock_picking.py` to include `sale_line_id`:

```python
def _prepare_subcontract_mo_vals(self, subcontract_move, bom):
    res = super()._prepare_subcontract_mo_vals(subcontract_move, bom)
    # Propagate sale_line_id from the subcontract move
    if subcontract_move.sale_line_id:
        res['sale_line_id'] = subcontract_move.sale_line_id.id
    return res
```

Then ensure the raw moves of the Subcontract MO inherit `sale_line_id` in their procurement values.

### Option 2: Extend location check for DSC destinations

Modify `_prepare_stock_moves()` in `sale_purchase_stock` to also propagate `sale_line_id` when destination is a subcontracting location:

```python
if final_loc.usage == 'customer' or final_loc.usage == 'transit' or final_loc.is_subcontract():
    re['sale_line_id'] = self.sale_line_id.id
```

### Option 3: Computed field following the chain

Add a computed `sale_id` that follows the relationship chain:

```
DSC Picking → Subcontract MO → Receipt Move → MO → sale_line_id → Sale Order
```

## Evidence

The module `mrp_subcontracting_dropshipping` already considers `sale_line_id` in some contexts, as seen in `stock_picking.py`:

```python
def _get_warehouse(self, subcontract_move):
    if subcontract_move.sale_line_id:
        return subcontract_move.sale_line_id.order_id.warehouse_id
    return super()._get_warehouse(subcontract_move)
```

This indicates the design intent was for the `sale_line_id` to be available on subcontract moves, but the propagation chain is broken.

## Test Case Reference

In `mrp_subcontracting_dropshipping/tests/test_purchase_subcontracting.py`, the test `test_portal_subcontractor_record_production_with_dropship` confirms the DSC Picking is linked to the Subcontract MO:

```python
self.assertEqual(po_dropship_subcontractor.picking_ids.picking_type_id, self.env.company.dropship_subcontractor_pick_type_id)
self.assertEqual(po_dropship_subcontractor.picking_ids, subcontracted_mo.picking_ids)
```

This relationship exists but doesn't include `sale_id` propagation.

## Steps to Reproduce

1. Install modules: `sale`, `mrp`, `mrp_subcontracting`, `mrp_subcontracting_dropshipping`, `quality_control`
2. Create a subcontracted product (e.g., "Tapa Terminada") with a subcontractor
3. Create a component with route "Dropship" and a vendor
4. Create a manufactured product (e.g., "Mesa") that uses the subcontracted product
5. Create and confirm a Sale Order for the manufactured product
6. Confirm the Purchase Order to the subcontractor
7. Observe that a DSC Picking is created for the component
8. Check the DSC Picking - the `sale_id` field is empty

## Environment

- Odoo Version: 17.0 / 18.0 / 19.0
- Modules: mrp_subcontracting_dropshipping, sale_mrp, sale_purchase_stock
- Database: Any

## Additional Context

This issue affects scenarios where companies need full traceability for:
- Quality Control documentation
- Customer-specific compliance requirements
- Production planning visibility
- Cost tracking per sale order

---

**Submitted by:** [Your Name]
**Date:** 2025-12-13
**Related Forum Discussions:**
- [Manufacturing/Subcontracting/Dropshipping - Route and Rules Config (EE18)](https://www.odoo.com/nl_NL/forum/help-1/manufacturingsubcontractingdropshipping-route-and-rules-config-ee18-281509)
- [How to access sale.order from stock.picking](https://www.odoo.com/forum/help-1/how-to-access-saleorder-from-stockpicking-69542)
