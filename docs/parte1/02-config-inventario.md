# 2. Configuración de Inventario

## Acceder a la Configuración

1. Ir a **Inventario**
2. Click en **Configuración → Ajustes**

---

## 2.1 Activar Multi-Step Routes

### Ubicación
```
Inventario → Configuración → Ajustes → Almacén
```

### Configuración

- [x] **Storage Locations** (Ubicaciones de almacenamiento)
- [x] **Multi-Step Routes** (Rutas de múltiples pasos)

!!! info "¿Por qué Multi-Step Routes?"
    Permite configurar flujos como:

    - Recepción → Control de Calidad → Stock
    - Stock → Picking → Packing → Envío

    Sin esto, los productos van directo de recepción a stock.

### Guardar
Click en **Guardar** para aplicar los cambios.

---

## 2.2 Configurar el Almacén

### Ubicación
```
Inventario → Configuración → Almacenes
```

### Pasos

1. Click en el almacén principal (ej: "WH" o nombre de tu empresa)
2. Configurar:

| Campo | Valor | Descripción |
|-------|-------|-------------|
| **Incoming Shipments** | Receive goods in input, then quality and then stock (3 steps) | Input → QC → Stock |
| **Outgoing Shipments** | Pack goods, send goods in output and then deliver (3 steps) | Pick → Pack → Ship |

### Resultado

Al guardar, Odoo crea automáticamente estas ubicaciones:

```
WH/
├── Input          (Recepción)
├── Quality Control (Control de Calidad)
├── Stock          (Almacén principal)
├── Output         (Salida)
└── Packing Zone   (Zona de empaque)
```

---

## 2.3 Crear Ubicaciones de Subcontratista

### Ubicación
```
Inventario → Configuración → Ubicaciones
```

### ¿Por qué crear estas ubicaciones?

Cada subcontratista necesita una ubicación virtual para:

- Rastrear materiales enviados al proveedor
- Controlar el inventario en tránsito

### Pasos

1. Click en **Nuevo**
2. Crear una ubicación por cada subcontratista:

| Nombre | Tipo | Ubicación Padre |
|--------|------|-----------------|
| Subcontract - Carpintería | Interna | Vendors (o Proveedores) |
| Subcontract - Lustrador | Interna | Vendors |
| Subcontract - Metalúrgica | Interna | Vendors |
| Subcontract - Marmolería | Interna | Vendors |

!!! example "Ejemplo de configuración"
    ```
    Nombre de ubicación: Subcontract - Carpintería Hnos. García
    Tipo de ubicación: Interna
    Ubicación padre: Partners/Vendors
    ```

---

## 2.4 Crear Ubicaciones de Tránsito (Opcional)

Si necesitás rastrear envíos entre proveedores:

### Pasos

1. Crear ubicación padre:
   ```
   Nombre: Transit Locations
   Tipo: Tránsito
   ```

2. Crear ubicaciones hijas:

| Nombre | Tipo | Padre |
|--------|------|-------|
| Transit: Carpintería → Lustrador | Tránsito | Transit Locations |
| Transit: Lustrador → Fábrica | Tránsito | Transit Locations |

---

## Verificación

Al finalizar deberías tener:

```
📍 Ubicaciones
├── WH/
│   ├── Input
│   ├── Quality Control ← Para QC en recepciones
│   ├── Stock
│   ├── Output
│   └── Packing Zone
├── Partners/Vendors/
│   ├── Subcontract - Carpintería ← Por subcontratista
│   ├── Subcontract - Lustrador
│   └── Subcontract - Metalúrgica
└── Transit Locations/ (opcional)
    ├── Transit: Carpintería → Lustrador
    └── Transit: Lustrador → Fábrica
```

---

## Resumen de Cambios

| Configuración | Valor |
|---------------|-------|
| Multi-Step Routes | ✅ Activado |
| Almacén - Recepción | 3 pasos (Input → QC → Stock) |
| Almacén - Envío | 3 pasos (Pick → Pack → Ship) |
| Ubicaciones subcontratista | Creadas por proveedor |
