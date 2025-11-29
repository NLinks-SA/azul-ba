# Parte 4: Control de Calidad

En esta sección configuraremos los **Quality Control Points** para automatizar controles de calidad.

## ¿Qué son los Control Points?

Los Control Points definen **cuándo** y **qué** controlar automáticamente:

```
RECEPCIÓN de Tapa Mármol
         │
         ▼
   ¿Hay Control Point para este producto en recepciones?
         │
         ▼ Sí
   Se crea Quality Check automáticamente
         │
         ▼
   Operador debe completar el check antes de continuar
```

---

## Control Points a Crear

| Control Point | Tipo | Productos | Momento |
|---------------|------|-----------|---------|
| QC Recepción Tapas Sin Terminar | Recepción | Tapas Madera Sin Terminar | Al recibir |
| QC Recepción Tapas Lustradas | Recepción | Tapas Madera Terminadas | Al recibir |
| QC Recepción Bases | Recepción | Bases Acero | Al recibir |
| QC Recepción Mármol | Recepción | Tapas Mármol | Al recibir |
| QC Recepción Neolith | Recepción | Tapas Neolith | Al recibir |
| QC Pre-Ensamblado | Work Order | Mesa | Antes de ensamblar |

---

## Secciones

1. [Control Points en Recepción](01-qc-recepcion.md)
2. [Control Points en Manufactura](02-qc-manufactura.md)
