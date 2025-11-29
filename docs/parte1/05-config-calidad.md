# 5. Configuración de Calidad

## Acceder al Módulo

```
Calidad → Configuración → Ajustes
```

!!! warning "Módulo Enterprise"
    El módulo completo de Calidad requiere Odoo Enterprise.

    Si tenés Community, las funcionalidades serán limitadas.

---

## 5.1 Verificar Instalación

El módulo de Calidad debería incluir:

- **Quality Control Points** (Puntos de control)
- **Quality Checks** (Controles de calidad)
- **Quality Alerts** (Alertas de calidad)

---

## 5.2 Equipos de Calidad

### Ubicación
```
Calidad → Configuración → Quality Teams
```

### Verificar o Crear Equipo

Odoo crea un equipo por defecto: **Main Quality Team**

Si necesitás equipos específicos:

1. Click en **Nuevo**
2. Configurar:

| Campo | Valor |
|-------|-------|
| Nombre | Equipo QC Recepción |
| Miembros | (seleccionar usuarios) |

---

## 5.3 Tipos de Test

### Ubicación
```
Calidad → Configuración → Test Types
```

### Tipos Disponibles

Odoo incluye estos tipos de test:

| Tipo | Uso |
|------|-----|
| **Pass - Fail** | Aprobado/Rechazado simple |
| **Measure** | Medición numérica con tolerancias |
| **Take a Picture** | Requiere foto del producto |
| **Instructions** | Instrucciones a seguir |
| **Spreadsheet** | Hoja de cálculo |

!!! tip "Recomendación"
    Para control de calidad básico en recepciones, usar **Pass - Fail**.

    Para inspecciones más detalladas, usar **Measure** con tolerancias.

---

## 5.4 No Configurar Control Points Todavía

!!! note "Importante"
    Los **Control Points** se configuran en la [Parte 4](../parte4/index.md) después de crear los productos.

    Necesitamos los productos creados para asociarlos a los Control Points.

---

## Verificación

En el menú de Calidad deberías ver:

```
Calidad
├── Control Points     ← Para crear los puntos de control
├── Quality Checks     ← Donde aparecerán los controles a realizar
├── Quality Alerts     ← Alertas de problemas
└── Configuración
    ├── Quality Teams
    └── Test Types
```

---

## Resumen

| Configuración | Estado |
|---------------|--------|
| Módulo Quality | ✅ Instalado |
| Quality Team | ✅ Existe (Main Quality Team) |
| Test Types | ✅ Disponibles (Pass-Fail, Measure, etc.) |
| Control Points | ⏳ Pendiente (Parte 4) |
