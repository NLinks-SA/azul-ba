# Parte 6: Facturación y Control

Esta sección cubre los procesos de facturación al cliente y validación de facturas de proveedores.

---

## Procesos Cubiertos

```
┌─────────────────────────────────────────────────────────────┐
│                    FACTURACIÓN                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   CLIENTE                        PROVEEDORES                │
│      │                                │                     │
│      ▼                                ▼                     │
│  ┌─────────┐                    ┌───────────┐              │
│  │ Entrega │                    │  Reciben  │              │
│  │Completa │                    │  Factura  │              │
│  └────┬────┘                    └─────┬─────┘              │
│       │                               │                     │
│       ▼                               ▼                     │
│  ┌─────────┐                    ┌───────────┐              │
│  │ Factura │                    │ Validación│              │
│  │ Cliente │                    │  3-Way    │              │
│  └────┬────┘                    │  + QC     │              │
│       │                         └─────┬─────┘              │
│       ▼                               │                     │
│  ┌─────────┐                          ▼                     │
│  │ Cobro   │                    ┌───────────┐              │
│  └─────────┘                    │   Pago    │              │
│                                 └───────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## Secciones

1. [Facturación al Cliente](01-factura-cliente.md)
2. [Validación Facturas Proveedores](02-factura-proveedores.md)

---

## Responsabilidades (RACI)

| Proceso | Responsable | Accountable |
|---------|-------------|-------------|
| Factura al cliente | Ventas | Ventas |
| Carga factura proveedor | Contabilidad | Contabilidad |
| Validación 3-way match | Contabilidad | Contabilidad |
| Consulta sobre PO | Compras | Contabilidad |
| Consulta sobre QC | Calidad | Contabilidad |
