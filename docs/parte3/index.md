# Parte 3: Manufactura

En esta sección configuraremos todo lo relacionado con la fabricación:

- Work Centers (Centros de trabajo)
- Listas de Materiales (BoM) normales
- BoMs de Subcontratación
- Operaciones y Routings

## Estructura de BoMs

```
📋 BOMs NORMALES (Mesa)
├── Mesa (Mármol, Negro, 180x90)
│   ├── Tapa Mármol 180x90 .......... qty: 1
│   └── Base Acero Negro 180x90 ..... qty: 1
│
├── Mesa (Madera, Negro, 180x90)
│   ├── Tapa Madera Terminada 180x90 (Lustre Mate) ... qty: 1
│   └── Base Acero Negro 180x90 ..... qty: 1
│
└── ... (12 variantes en total)

📋 BOMs SUBCONTRATACIÓN
├── Base Acero Negro 180x90
│   └── Subcontratista: Metalúrgica
│   └── (sin componentes - proveedor provee todo)
│
├── Tapa Madera Terminada 180x90 (Lustre Mate)
│   └── Subcontratista: Lustrador
│   └── Componente: Tapa Madera Sin Terminar 180x90
│
└── ... (otras variantes)
```

## Secciones

1. [Work Centers](01-work-centers.md)
2. [BoM Normal (Mesa)](02-bom-normal.md)
3. [BoM Subcontratación](03-bom-subcontratacion.md)
4. [Operaciones y Routings](04-operaciones.md)
