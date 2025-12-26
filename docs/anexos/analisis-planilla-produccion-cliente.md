# Análisis Exhaustivo: Planilla de Producción del Cliente

## Resumen Ejecutivo

La planilla "Odoo - Produccion.xlsx" contiene la operatoria real de producción del cliente. Es un sistema manual basado en Excel con **10 hojas** que gestionan todo el ciclo productivo: desde el pedido hasta la logística de entrega.

**Datos clave:**
- **2,835 registros** de producción (2021-2025)
- **171 productos/artículos** diferentes
- **64 proveedores** activos
- **125 proveedores** en catálogo completo
- **4,363 registros** de logística

---

## 1. Estructura de Hojas

| Hoja | Propósito | Registros |
|------|-----------|-----------|
| **Produccion** | Registro principal de pedidos y seguimiento | 2,835 |
| **SEGUIMIENTO** | Pedidos prioritarios/urgentes | 9 |
| **AGENDA** | Pedidos por vencer/vencidos | (dinámico) |
| **LOGISTICA** | Registro de envíos y retiros | 4,363 |
| **Logistica Planilla** | Planificación de rutas | - |
| **VACACIONES** | Control de vacaciones proveedores | - |
| **Proveedores** | Catálogo de proveedores | 125 |
| **Tiempos** | Lead times por proveedor | 125 |
| **Mejoras** | Lista de mejoras pendientes | 5 |

---

## 2. Productos Principales

### 2.1 Mesas (Producto Principal)

| Modelo | Registros | Descripción |
|--------|-----------|-------------|
| **Wull Extensible Stone** | 277 | Mesa extensible con tapa de piedra (Neolith/Dekton) |
| **Rocca Stone** | 104 | Mesa fija con tapa de piedra |
| **Rinni Extensible Wood** | 68 | Mesa extensible con tapa de madera |
| **Venus Extensible Stone** | 70 | Mesa extensible con tapa de piedra |
| **Rinni Extensible Stone** | 36 | Mesa extensible con tapa de piedra |
| **Venus Extensible Wood** | 33 | Mesa extensible con tapa de madera |
| **Frame Stone** | 28 | Mesa con base Frame y tapa de piedra |
| **Exon Stone** | 25 | Mesa con base Exon y tapa de piedra |

### 2.2 Bases de Mesa

| Modelo | Registros | Material |
|--------|-----------|----------|
| **Fix** | 95 | Caño aluminio/hierro |
| **Cantabria** | 75 | Caño aluminio |
| **Rinni** | 44 | MDF + acero |
| **Valentinox** | 33 | Acero inoxidable |
| **Krull** | 19 | Madera Paraíso |
| **Conica** | 20 | Varios |
| **Frame** | 16 | Madera Paraíso |
| **Tecno** | 27 | Aluminio |

### 2.3 Sillas

| Modelo | Registros | Características |
|--------|-----------|-----------------|
| **Silla Gin** | 42 | Tapizado, patas madera |
| **Silla Evelyn** | 37 | Tapizado |
| **Butaca Gin** | 37 | Tapizado, patas madera |
| **Silla Eve** | 25 | Tapizado |
| **Butaca Evelyn** | 25 | Tapizado |
| **Butaca Ulises** | 21 | Tapizado |
| **Silla Forms** | 11 | Tapizado |
| **Silla Luana** | 10 | Tapizado |

---

## 3. Proveedores y Rubros

### 3.1 Proveedores Principales (por volumen)

| Proveedor | Registros | Rubro | Lead Time |
|-----------|-----------|-------|-----------|
| **TALLER** | 166 | Producción interna | 7 días |
| **GUSTAVO LUS** | 134 | Lustrador | 14 días |
| **HUGO** | 114 | Tornería | 10 días |
| **JONATHAN LUS** | 87 | Lustrador | 14 días |
| **ORMETAL** | 78 | Aluminio | 7 días |
| **ALEJANDRO HERRERO** | 72 | Cliente/Herrería | 14 días |
| **GN ESTUDIO** | 71 | Corte CNC | 7 días |
| **EUROSTONE** | 66 | Corte mármol/piedra | 10 días |
| **PINTURA NEGABY** | 56 | Pintura | 7 días |
| **MAXI CAR** | 49 | Carpintero | 14 días |

### 3.2 Rubros de Proveedores

| Rubro | Proveedores | Lead Time Típico |
|-------|-------------|------------------|
| **LUSTRADOR** | 5 (Gustavo, Jonathan, Hernan, Elian, Lus Eze) | 14 días |
| **CARPINTERO** | 4 (Maxi Car, Francisco, Celestino, Pablo) | 14-21 días |
| **TORNERÍA** | 2 (Hugo, Coco) | 7-10 días |
| **MARMOLERÍA/PIEDRA** | 3 (Eurostone, Destefano, Decostone) | 7-30 días |
| **ALUMINIO** | 4 (Ormetal, AX, Marra, DYM) | 7-14 días |
| **PINTURA** | 2 (Negaby, Florida) | 7 días |
| **SILLAS** | 6 (BYB, ECSA, JYJ, Milciades, Elias, Omicrom) | 20-50 días |
| **TAPICERO** | 3 (Juan Andres, Cacho, Pedro) | 7-14 días |
| **CORTE CNC** | 2 (GN Estudio, AGG Metalurgica) | 7-14 días |
| **CROMADOR** | 2 (Claudio, Sergio) | 14 días |
| **HERRERÍA** | 3 (Chamo, German, Roberto) | 10-20 días |

---

## 4. Flujo de Producción Identificado

### 4.1 Mesa con Tapa de Piedra (ej: Wull Extensible Stone)

```
1. PEDIDO CLIENTE
      │
      ▼
2. GN ESTUDIO (Corte CNC de MDF) ──────────────────────┐
      │                                                 │
      ▼                                                 ▼
3. EUROSTONE/DESTEFANO (Corte piedra)     GUSTAVO/JONATHAN LUS (Lustrado)
      │                                                 │
      ▼                                                 ▼
4. PINTURA NEGABY (Pintura de base MDF)    ◄───────────┘
      │
      ▼
5. ALEJANDRO HERRERO (Herrería/Ensamble)
      │
      ▼
6. TALLER (Ensamble final + Control)
      │
      ▼
7. HECTOR EMBALAJES (Embalaje)
      │
      ▼
8. METROFLET (Logística de entrega)
```

### 4.2 Mesa con Base de Madera (ej: Fix, Cantabria)

```
1. PEDIDO CLIENTE
      │
      ▼
2. AX ALUMINIO (Corte caños aluminio)
      │
      ├────────────────────────────────────────┐
      ▼                                        ▼
3. SARAVIA (Anodizado)              CARPINTERO FRANCISCO (Madera)
      │                                        │
      ▼                                        ▼
4. ORMETAL (Mecanizado)             GUSTAVO LUS (Lustrado madera)
      │                                        │
      └────────────────────────────────────────┘
                      │
                      ▼
5. TALLER (Ensamble final)
```

### 4.3 Sillas (ej: Silla Gin)

```
1. PEDIDO CLIENTE
      │
      ▼
2. BYB/ECSA/JYJ (Estructura base) ─── Lead time: 20-50 días
      │
      ▼
3. JONATHAN/GUSTAVO LUS (Lustrado patas)
      │
      ▼
4. TAPICERO JUAN ANDRES (Tapizado)
      │
      ▼
5. MILCIADES/SIROTA (Ajustes/Revisión)
      │
      ▼
6. TALLER (Control final)
```

---

## 5. Estados y Seguimiento

### 5.1 Estados de Pedido

| Estado | Significado |
|--------|-------------|
| **LISTO** | Completado (1,496 registros) |
| **\*** | En proceso/Activo |
| **Números negativos** | Días de atraso |
| **Números positivos** | Días restantes |

### 5.2 Columnas de Control

| Columna | Propósito |
|---------|-----------|
| **F. Ped.** | Fecha de pedido al proveedor |
| **F. Entre.** | Fecha de entrega prometida |
| **Falta** | Estado/días restantes |
| **Rehace 1/2/3** | Reprocesos por problemas de calidad |
| **Observaciones** | Notas adicionales |
| **TIEMPO** | Lead time esperado (días) |

---

## 6. Problemas de Calidad (Rehaces)

Se identifican múltiples registros con "Rehace 1/2/3" indicando problemas de calidad:
- Rayones en piedra
- Problemas de lustre
- Defectos en soldadura
- Errores de medidas
- Problemas de tapizado

---

## 7. Logística

### 7.1 Empresa de Transporte
- **METROFLET**: Principal empresa de logística (4,363 registros)

### 7.2 Tipos de Operación
- **CARGAR**: Cargar material en taller
- **DAR**: Entregar material a proveedor
- **RETIRAR**: Retirar material de proveedor

### 7.3 Direcciones Frecuentes
Cada proveedor tiene su dirección registrada en la hoja "Proveedores" con:
- Dirección completa
- Contacto
- Canal de pedidos (Papel, WhatsApp, Email)
- Horario de atención

---

## 8. Comparación con Demo Actual (setup.py)

| Aspecto | Demo Actual | Realidad Cliente |
|---------|-------------|------------------|
| **Productos** | Mesa Comedor Premium (48 variantes) | 171 artículos diferentes |
| **Proveedores** | 5 (simplificado) | 64+ activos |
| **Flujo** | Lineal simple | Multi-etapa paralelo |
| **Materiales tapa** | Madera, Mármol, Neolith | Neolith, Dekton, MDF, Mármol, Melamina |
| **Bases** | 4 tipos simples | 15+ modelos |
| **Sillas** | No incluido | 20+ modelos |
| **Lead times** | 3-10 días | 7-50 días |
| **Subcontratación** | 1 nivel (Lustrador) | Multi-nivel (3-5 proveedores por producto) |

---

## 9. Recomendaciones para Odoo

### 9.1 Estructura de Productos

```
Productos
├── Mesas
│   ├── Wull (Extensible Stone, Extensible Wood, Stone, Wood, PE)
│   ├── Rocca (Stone, Wood)
│   ├── Rinni (Extensible Stone, Extensible Wood, Stone, Acero)
│   ├── Venus (Extensible Stone, Extensible Wood, Stone, Wood)
│   ├── Frame (Stone, Wood, PE)
│   ├── Exon (Stone, Wood)
│   └── ... (otros modelos)
├── Bases
│   ├── Fix
│   ├── Cantabria
│   ├── Krull
│   ├── Valentinox
│   ├── Conica
│   └── ... (otros modelos)
├── Tapas
│   ├── Stone (Neolith, Dekton, Mármol)
│   ├── Wood (MDF lustrado)
│   └── Melamina
└── Sillas
    ├── Gin (Silla, Butaca, Banqueta)
    ├── Evelyn (Silla, Butaca)
    ├── Eve (Silla, Butaca)
    └── ... (otros modelos)
```

### 9.2 Categorías de Proveedores

Crear categorías en Odoo para:
- Lustradores
- Carpinteros
- Marmolerías/Piedra
- Herrería/Aluminio
- Pintura
- Tapicería
- Sillas (fabricantes)
- Logística

### 9.3 Rutas de Producción

Necesitan rutas multi-nivel:
1. **Compra directa** (Buy)
2. **Subcontratación simple** (1 proveedor)
3. **Subcontratación en cadena** (múltiples proveedores secuenciales)
4. **Dropship a subcontratista** (proveedor → subcontratista)

### 9.4 Control de Calidad

Implementar QC en:
- Recepción de piedra (rayones, vetas)
- Lustrado (acabado, color)
- Pintura (uniformidad, adherencia)
- Ensamble final (ajuste, nivelación)

### 9.5 Atributos de Producto

**Para Mesas:**
- Modelo base (Wull, Rocca, Rinni, Venus, etc.)
- Tipo (Extensible, Fija, Personalizada)
- Material tapa (Stone, Wood)
- Piedra específica (Neolith Calacatta, Dekton Rem, etc.)
- Medidas (personalizable)
- Acabado base (Lustre, Pintura, Anodizado)

**Para Sillas:**
- Modelo (Gin, Evelyn, Eve, etc.)
- Tipo (Silla, Butaca, Banqueta)
- Tela (código y proveedor)
- Acabado patas (Lustre, Pintura)

---

## 10. Complejidad Real vs Demo

La demo actual (setup.py) cubre aproximadamente el **5-10%** de la complejidad real del cliente:

| Característica | Demo | Real |
|----------------|------|------|
| Variantes de producto | Básico (4 atributos) | Complejo (6+ atributos) |
| Cadena de subcontratación | 1 nivel | 3-5 niveles |
| Proveedores por producto | 2-3 | 5-10 |
| Control de calidad | 1 punto | 4-5 puntos |
| Personalización | Limitada | Extensiva (medidas a medida) |
| Rehaces/Devoluciones | No implementado | Crítico |
| Logística | No implementado | Compleja (rutas diarias) |

---

## 11. Próximos Pasos Sugeridos

1. **Fase 1**: Expandir catálogo de productos y proveedores
2. **Fase 2**: Implementar rutas multi-nivel de subcontratación
3. **Fase 3**: Agregar módulo de sillas
4. **Fase 4**: Implementar gestión de rehaces/devoluciones
5. **Fase 5**: Integrar módulo de logística (rutas de entrega)

---

*Análisis generado el 2025-12-17*
