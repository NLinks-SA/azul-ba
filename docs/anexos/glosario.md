# Glosario de Términos

Definiciones de términos clave usados en esta guía.

---

## A

### Atributo (Attribute)
Característica variable de un producto que genera variantes. Ejemplo: Color, Tamaño.

---

## B

### BoM (Bill of Materials)
Lista de materiales. Define los componentes necesarios para fabricar un producto.

### BoM de Subcontratación
BoM especial donde el producto es fabricado por un proveedor externo (subcontratista).

---

## C

### Componente
Producto que forma parte de otro producto en una BoM.

### Control Point
Punto de control de calidad que define cuándo y qué verificar automáticamente.

---

## D

### Dropship
Ruta de abastecimiento donde el proveedor envía directamente al destino, sin pasar por nuestro almacén.

### Dropship Subcontractor
Flujo especial donde un proveedor envía materiales **directamente** a un subcontratista, sin pasar por el almacén de la empresa. Ejemplo: Carpintería envía Tapa Sin Terminar directo al Lustrador.

### DSC (Dropship Subcontractor)
Código del Picking Type que gestiona los movimientos de Dropship Subcontractor.

### DSC Picking
Movimiento de inventario del tipo Dropship Subcontractor. Representa el envío directo de un proveedor a un subcontratista.

```
Proveedor A ──(DSC Picking)──► Subcontratista B
                    │
                    └── NO pasa por WH/Stock
```

---

## L

### Lead Time
Tiempo de entrega. Días desde que se ordena hasta que se recibe un producto.

---

## M

### MO (Manufacturing Order)
Orden de fabricación. Documento que indica qué producir, cuánto y cuándo.

### MTO (Make to Order)
Fabricar bajo pedido. Estrategia donde se produce solo cuando hay una demanda real.

### MTS (Make to Stock)
Fabricar para stock. Estrategia donde se produce para mantener inventario.

---

## O

### Operación
Paso de trabajo en un proceso de fabricación, asociado a un Work Center.

---

## P

### Picking Type
Tipo de operación de inventario. Define el comportamiento de los movimientos (recepciones, entregas, internos, etc.).

### PO (Purchase Order)
Orden de compra. Documento para solicitar productos a un proveedor.

### Producto Terminado
Producto final que se vende al cliente.

---

## Q

### Quality Alert
Alerta de calidad generada cuando un Quality Check falla.

### Quality Check
Control de calidad individual que debe completarse.

### Quality Point
Regla que define cuándo se crea automáticamente un Quality Check. Se asocia a productos, tipos de operación, etc.

---

## R

### Ruta (Route)
Reglas que definen cómo se abastece un producto (comprar, fabricar, MTO, Dropship, etc.).

### RFQ (Request for Quotation)
Solicitud de presupuesto. Borrador de orden de compra.

---

## S

### SO (Sales Order)
Orden de venta. Pedido confirmado de un cliente.

### Subcontract MO
Orden de manufactura que se crea automáticamente al confirmar una PO de subcontratación. Representa el trabajo que realiza el subcontratista.

### Subcontratación
Proceso donde un proveedor externo fabrica productos usando (opcionalmente) nuestros materiales.

### Subcontratista
Proveedor que realiza trabajo de fabricación por nosotros.

---

## U

### Ubicación (Location)
Lugar físico o lógico donde se almacenan productos.

### Ubicación de Subcontratista
Ubicación virtual que representa el stock en poder del subcontratista. Deben ser hijas de la ubicación **Subcontratación** (no de Vendors).

```
Subcontratación/
├── Subcontract - Carpintería Hnos. García
├── Subcontract - Lustres & Acabados
├── Subcontract - Metalúrgica Precisión
├── Subcontract - Marmolería Del Sur
└── Subcontract - Neolith Argentina
```

### Ubicación de Tránsito
Ubicación intermedia para productos en movimiento entre ubicaciones.

---

## V

### Variante
Versión específica de un producto basada en combinaciones de atributos.

---

## W

### WO (Work Order)
Orden de trabajo. Tarea específica dentro de una orden de fabricación.

### Work Center
Centro de trabajo. Lugar donde se realizan operaciones de fabricación.

---

## Acrónimos Comunes

| Acrónimo | Significado |
|----------|-------------|
| BoM | Bill of Materials (Lista de Materiales) |
| DSC | Dropship Subcontractor |
| MO | Manufacturing Order (Orden de Fabricación) |
| MTO | Make to Order (Fabricar Bajo Pedido) |
| MTS | Make to Stock (Fabricar Para Stock) |
| PO | Purchase Order (Orden de Compra) |
| QC | Quality Control (Control de Calidad) |
| RFQ | Request for Quotation (Solicitud de Presupuesto) |
| SO | Sales Order (Orden de Venta) |
| WC | Work Center (Centro de Trabajo) |
| WO | Work Order (Orden de Trabajo) |

---

## Módulos Clave

| Módulo Técnico | Nombre | Función |
|----------------|--------|---------|
| `mrp_subcontracting` | MRP Subcontracting | Habilita subcontratación básica |
| `mrp_subcontracting_dropshipping` | MRP Subcontracting Dropshipping | Habilita Dropship Subcontractor (DSC) |
| `stock_dropshipping` | Dropshipping | Habilita ruta Dropship en productos |
| `quality_control` | Quality Control | Control de calidad con Quality Points |
