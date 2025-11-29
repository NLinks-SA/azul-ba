# Parte 2: Datos Maestros

En esta sección crearemos los proveedores y productos necesarios para la demo.

## Estructura de Datos

```
📦 PRODUCTOS
├── Mesa Comedor Premium (12 variantes)
│   └── Atributos: Material Tapa × Material Base × Medidas
│
├── Componentes - TAPAS
│   ├── Tapa Mármol Carrara (180x90, 220x100)
│   ├── Tapa Neolith Negro (180x90, 220x100)
│   ├── Tapa Madera Sin Terminar (180x90, 220x100)
│   └── Tapa Madera Terminada (2 tamaños × 3 terminaciones)
│
└── Componentes - BASES
    ├── Base Acero Negro (180x90, 220x100)
    └── Base Acero Dorado (180x90, 220x100)

👥 PROVEEDORES
├── Marmolería Del Sur
├── Neolith Argentina
├── Carpintería Artesanal Hnos. García
├── Lustres & Acabados Premium
└── Metalúrgica Precisión S.A.
```

## Orden de Creación

!!! warning "Importante: Respetar el orden"
    Los productos deben crearse en este orden porque las BoMs necesitan que los componentes existan primero.

1. **Proveedores** - Primero los proveedores
2. **Atributos** - Para variantes de producto
3. **Componentes** - Tapas y Bases
4. **Producto Final** - Mesa con variantes

## Secciones

1. [Proveedores](01-proveedores.md)
2. [Atributos de Producto](02-atributos.md)
3. [Productos Componentes](03-productos-componentes.md)
4. [Producto Final (Mesa)](04-producto-final.md)
