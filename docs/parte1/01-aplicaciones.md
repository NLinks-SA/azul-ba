# 1. Aplicaciones a Instalar

## Acceder al Menú de Aplicaciones

1. Ir a **Aplicaciones** (ícono de cuadrícula en la barra superior)
2. O navegar a: `Ajustes → Aplicaciones`

---

## Aplicaciones Requeridas

Instalar las siguientes aplicaciones en este orden:

### 1.1 Ventas (Sales)

```
Nombre técnico: sale_management
```

- Permite crear cotizaciones y órdenes de venta
- Gestiona clientes y precios

!!! info "Cómo instalar"
    1. Buscar "Ventas" o "Sales"
    2. Click en **Instalar**

---

### 1.2 Inventario (Inventory)

```
Nombre técnico: stock
```

- Gestión de almacenes y ubicaciones
- Control de stock
- Movimientos de inventario

---

### 1.3 Compras (Purchase)

```
Nombre técnico: purchase
```

- Gestión de proveedores
- Órdenes de compra
- Recepciones de mercadería

---

### 1.4 Manufactura (Manufacturing)

```
Nombre técnico: mrp
```

- Listas de materiales (BoM)
- Órdenes de fabricación
- Work Centers y operaciones

---

### 1.5 Calidad (Quality)

```
Nombre técnico: quality_control
```

!!! warning "Módulo Enterprise"
    El módulo de Calidad completo requiere licencia Enterprise.
    En Community existe una versión limitada.

- Control Points
- Alertas de calidad
- Checks en recepciones y producción

---

### 1.6 Contabilidad (Accounting) - Opcional

```
Nombre técnico: account_accountant
```

- Para costeo de productos
- Valuación de inventario
- Facturación

---

## Verificar Instalación

Después de instalar, deberías ver estos menús en la barra de aplicaciones:

- 📊 Ventas
- 📦 Inventario
- 🛒 Compras
- 🏭 Manufactura
- ✅ Calidad

---

## Módulos Adicionales (se instalan automáticamente)

Al instalar las aplicaciones principales, Odoo instala automáticamente:

| Módulo | Se instala con |
|--------|----------------|
| `mrp_subcontracting` | Manufactura |
| `purchase_mrp` | Compras + Manufactura |
| `quality_mrp` | Calidad + Manufactura |
| `sale_mrp` | Ventas + Manufactura |

!!! tip "Verificar módulos de subcontratación"
    Ir a `Aplicaciones → Buscar "subcontract"` y verificar que esté instalado:

    - **MRP Subcontracting** (`mrp_subcontracting`)
