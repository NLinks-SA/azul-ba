# 4. Configuración de Manufactura

## Acceder a la Configuración

```
Manufactura → Configuración → Ajustes
```

---

## 4.1 Activar Work Orders

### Ubicación
```
Manufactura → Configuración → Ajustes → Operaciones
```

### Configuración

- [x] **Work Orders** (Órdenes de trabajo)

!!! info "¿Qué habilita esto?"
    - Permite definir **Work Centers** (centros de trabajo)
    - Habilita las **Operaciones/Routings** en las BoMs
    - Permite planificar la producción por estación
    - Vista Gantt de planificación

---

## 4.2 Verificar Subcontratación

En la misma pantalla, verificar que esté activo:

- [x] **Subcontracting** (Subcontratación)

!!! note "Se activa automáticamente"
    Si activaste Subcontracting en Compras, ya debería estar activo aquí.

---

## 4.3 Otras Configuraciones Útiles (Opcionales)

### By-Products (Subproductos)

- [ ] **By-Products**

Habilita si tu proceso genera subproductos o residuos que querés rastrear.

### Lot/Serial Numbers (Lotes/Números de Serie)

Si querés trazabilidad por lote:

```
Inventario → Configuración → Ajustes → Trazabilidad
```

- [x] **Lots & Serial Numbers**

---

## 4.4 Guardar Cambios

Click en **Guardar**

---

## Verificación

Después de guardar, deberías ver en el menú de Manufactura:

- **Work Centers** (Centros de trabajo)
- En las BoMs: pestaña **Operaciones**

### Menú esperado:

```
Manufactura
├── Operaciones
│   ├── Órdenes de Fabricación
│   ├── Órdenes de Trabajo    ← Nuevo
│   └── ...
├── Productos
├── Datos
│   ├── Listas de materiales
│   └── Work Centers          ← Nuevo
└── Configuración
```

---

## Resumen

| Configuración | Valor |
|---------------|-------|
| Work Orders | ✅ Activado |
| Subcontracting | ✅ Activado |
| By-Products | ⚪ Opcional |
| Lots & Serial | ⚪ Opcional |
