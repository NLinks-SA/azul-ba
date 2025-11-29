# Troubleshooting

Soluciones a problemas comunes durante la configuración y operación.

---

## Problemas de Configuración

### La ruta MTO no aparece en productos

**Síntoma**: No puedo seleccionar "Reponer bajo pedido (MTO)" en un producto.

**Solución**:
1. Ir a **Inventario → Configuración → Ajustes**
2. Activar **Rutas Multi-Paso**
3. Guardar
4. Ir a **Inventario → Configuración → Rutas**
5. Buscar "Reponer bajo pedido (MTO)"
6. Activar la casilla **Seleccionable en producto**

---

### No se crea MO automáticamente al confirmar venta

**Síntoma**: Confirmo la venta pero no aparece orden de fabricación.

**Causas posibles**:

1. **El producto no tiene ruta MTO**
   - Verificar en producto → Inventario → Rutas
   - Debe tener: "Reponer bajo pedido (MTO)" + "Fabricar"

2. **El producto no tiene BoM**
   - Verificar en Manufactura → BoMs
   - Debe existir una BoM para el producto/variante

3. **La BoM está archivada o inactiva**
   - Buscar BoMs archivadas y activar

---

### No se crean POs automáticamente

**Síntoma**: La MO se crea pero no las órdenes de compra para componentes.

**Causas posibles**:

1. **Los componentes no tienen ruta MTO + Comprar**
   - Verificar cada componente en la BoM
   - Deben tener: "Reponer bajo pedido (MTO)" + "Comprar"

2. **Los componentes no tienen proveedor configurado**
   - Ir al componente → Compra → Agregar proveedor

3. **Hay stock disponible del componente**
   - Si hay stock, el MTO no genera compra
   - Verificar cantidades en inventario

---

## Problemas de Subcontratación

### La PO de subcontratación no mueve componentes

**Síntoma**: Al confirmar PO a subcontratista, no se crea envío de componentes.

**Solución**:
1. Verificar que la BoM es tipo **Subcontratación**
2. Verificar que la BoM tiene componentes definidos
3. Verificar que el proveedor está en la lista de **Subcontratistas** de la BoM
4. Verificar stock del componente (debe haber disponibilidad)

---

### Error al recibir producto subcontratado

**Síntoma**: No puedo validar la recepción del subcontratista.

**Causas posibles**:

1. **Componentes no enviados**
   - Primero validar el envío de componentes
   - Luego validar la recepción

2. **Ubicación de subcontratista no configurada**
   - Verificar que el proveedor tiene ubicación asignada
   - Proveedor → Inventario → Ubicación de Subcontratista

---

## Problemas de Quality

### Los Quality Checks no aparecen

**Síntoma**: Hago una recepción pero no aparece control de calidad.

**Causas posibles**:

1. **Control Point no configurado para el producto**
   - Verificar en Calidad → Control Points
   - El producto debe estar incluido

2. **Control Point no configurado para la operación**
   - Verificar que "Tipos de operación" incluye "Recepciones" (o Manufacturing)

3. **Control Point archivado**
   - Buscar Control Points archivados

---

### Quality Check bloquea la recepción

**Síntoma**: No puedo validar recepción porque hay QC pendiente.

**Solución**:
1. Click en el indicador de Quality Check
2. Completar el check (Pass o Fail)
3. Luego validar la recepción

Si el check falló:
- Se crea Quality Alert
- Decidir acción: rechazar, aceptar, etc.

---

## Problemas de Manufactura

### Work Orders no se generan

**Síntoma**: La MO no tiene Work Orders.

**Causas posibles**:

1. **BoM no tiene operaciones**
   - Agregar operaciones en la BoM → Pestaña Operaciones

2. **Work Centers no configurados**
   - Crear Work Centers antes de definir operaciones

3. **Work Orders desactivados**
   - Manufactura → Configuración → Activar Work Orders

---

### No puedo completar Work Order

**Síntoma**: El botón "Hecho" no aparece o está deshabilitado.

**Causas posibles**:

1. **Quality Check pendiente**
   - Completar el QC asociado al WO

2. **WO anterior no completado**
   - Completar Work Orders en secuencia

---

## Problemas de Inventario

### Producto muestra stock incorrecto

**Síntoma**: El stock no coincide con lo esperado.

**Solución**:
1. Ir a **Inventario → Informes → Historial de movimientos**
2. Filtrar por producto
3. Analizar movimientos para identificar discrepancias
4. Si es necesario, hacer ajuste de inventario

---

### Movimiento atascado en "Esperando"

**Síntoma**: Un movimiento queda en estado "Esperando otro movimiento".

**Causas posibles**:

1. **Depende de recepción pendiente**
   - Completar la recepción primero

2. **Multi-step route incompleto**
   - Verificar y completar pasos anteriores

---

## Errores Comunes de Datos

### "No se puede eliminar registro vinculado"

**Síntoma**: Error al intentar borrar un registro.

**Solución**:
- Algunos registros tienen dependencias
- Archivar en lugar de eliminar
- O eliminar primero los registros dependientes

---

### Producto duplicado

**Síntoma**: Aparecen productos duplicados.

**Solución**:
1. Verificar si son variantes vs productos separados
2. Si son duplicados reales:
   - Mover stock al producto correcto
   - Archivar el duplicado

---

## Verificaciones Rápidas

### Checklist Pre-Operación

```
□ Apps instaladas: Sales, Inventory, Purchase, Manufacturing, Quality
□ MTO activado y visible en productos
□ Subcontratación activada
□ Work Centers creados
□ Proveedores con ubicaciones de subcontratista
□ Productos con rutas correctas
□ BoMs creadas y activas
□ Control Points configurados
```

### Comandos Útiles (Consola Odoo)

```python
# Ver rutas de un producto
product = env['product.product'].browse(ID)
print(product.route_ids.mapped('name'))

# Ver BoM de un producto
bom = env['mrp.bom'].search([('product_tmpl_id', '=', product.product_tmpl_id.id)])
print(bom.bom_line_ids.mapped('product_id.name'))

# Ver Control Points activos
qc = env['quality.point'].search([('active', '=', True)])
for q in qc:
    print(f"{q.name}: {q.product_ids.mapped('name')}")
```

---

## Contacto de Soporte

Si el problema persiste:
1. Documentar pasos para reproducir
2. Capturar screenshots del error
3. Contactar al equipo de implementación
