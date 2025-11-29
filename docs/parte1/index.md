# Parte 1: Preparación del Sistema

En esta sección configuraremos el sistema base de Odoo para soportar manufactura con subcontratación.

## Resumen de Configuraciones

| Módulo | Configuración | Por qué |
|--------|---------------|---------|
| **Inventario** | Multi-step Routes | Habilita ubicaciones de QC y tránsito |
| **Compras** | Subcontracting | Permite BoMs de subcontratación |
| **Manufactura** | Work Orders, Subcontracting | Habilita operaciones y routings |
| **Calidad** | Quality Control | Permite crear Control Points |
| **Ventas** | (MTO ya activo) | Ruta "Replenish on Order" |

## Secciones

1. [Aplicaciones a Instalar](01-aplicaciones.md)
2. [Configuración de Inventario](02-config-inventario.md)
3. [Configuración de Compras](03-config-compras.md)
4. [Configuración de Manufactura](04-config-manufactura.md)
5. [Configuración de Calidad](05-config-calidad.md)
6. [Configuración de Ventas (MTO)](06-config-ventas.md)
