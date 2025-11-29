# Parte 5: Flujo Operativo

En esta sección ejecutaremos el flujo completo de punta a punta para verificar que toda la configuración funciona correctamente.

## Flujo Completo

```
CLIENTE realiza PEDIDO
         │
         ▼
1. VENTA (Sales Order)
   └── Confirmar pedido
         │
         ▼
2. MANUFACTURA (Manufacturing Order)
   └── Se crea automáticamente por MTO
         │
         ▼
3. COMPRAS (Purchase Orders)
   └── Se crean automáticamente para componentes
         │
         ▼
4. RECEPCIONES + QUALITY CHECKS
   └── Recibir componentes con controles
         │
         ▼
5. PRODUCCIÓN
   └── Ensamblar mesa con Work Orders
         │
         ▼
6. ENTREGA
   └── Enviar al cliente
```

---

## Escenario de Prueba

### Datos del Pedido

| Campo | Valor |
|-------|-------|
| **Cliente** | Cualquier cliente de prueba |
| **Producto** | Mesa Comedor Premium |
| **Variante** | Madera Terminada + Base Negro + 180x90 + Lustre Mate |
| **Cantidad** | 1 |

### Resultado Esperado

| Documento | Cantidad |
|-----------|----------|
| Sale Order | 1 |
| Manufacturing Order | 1 |
| Purchase Orders | 2-3 (Carpintería, Lustrador, Metalúrgica) |
| Quality Checks | 2+ (recepción + manufactura) |

---

## Secciones

1. [Crear la Venta](01-crear-venta.md)
2. [Verificar MO y POs](02-mo-pos.md)
3. [Recepciones con QC](03-recepciones.md)
4. [Producción](04-produccion.md)
