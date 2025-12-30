# Shop Floor - Configuración y Uso

## Resumen

Este documento describe la configuración de Shop Floor en Odoo 19 para la gestión de operaciones de manufactura con:
- **Un solo Work Center** para simplificar la interfaz
- **Operaciones secuenciales** (cada operación depende de la anterior)
- **Instrucciones con PDF embebido** usando el visor nativo de Odoo
- **Quality Points** para cada paso del proceso

---

## Configuración Automática

El script `setup_real.py` configura automáticamente:

| Componente | Descripción |
|------------|-------------|
| **Work Center único** | "Producción" - todas las operaciones en un solo lugar |
| **Operaciones secuenciales** | 4 pasos con dependencias (blocked_by_operation_ids) |
| **Quality Points** | Instrucciones detalladas para cada operación |
| **PDF embebido** | Plano de ensamble visible en el visor nativo |

---

## Work Center Único

Para simplificar Shop Floor, se usa un solo work center:

```
Producción (ID: PROD)
├── 1. Preparación componentes
├── 2. Ensamble tapa + base
├── 3. Control de calidad
└── 4. Embalaje
```

**Ventajas:**
- Interfaz más simple (una sola pestaña)
- No requiere cambiar entre work centers
- Todas las operaciones visibles en secuencia

---

## Operaciones Secuenciales

Las operaciones se configuran con dependencias para ejecutarse en orden:

| Operación | Sequence | Bloqueada por | Estado inicial |
|-----------|----------|---------------|----------------|
| 1. Preparación | 10 | - | ready |
| 2. Ensamble | 20 | Preparación | blocked |
| 3. Control | 30 | Ensamble | blocked |
| 4. Embalaje | 40 | Control | blocked |

**Comportamiento:**
1. Solo "1. Preparación" está disponible al inicio
2. Al completar Preparación, se desbloquea Ensamble
3. Al completar Ensamble, se desbloquea Control
4. Y así sucesivamente

---

## PDF Embebido en Instrucciones

### Configuración del PDF

El PDF se almacena en el campo `worksheet_document` del Quality Point:

```python
qp_vals = {
    'name': 'Instrucciones: 1. Preparación componentes',
    'title': 'Verificar componentes antes de iniciar',
    'measure_on': 'operation',
    'operation_id': op_id,
    'test_type_id': test_type_instr_id,
    'note': '<h3>📋 PREPARACIÓN...</h3>...',
    'worksheet_document': pdf_base64,  # PDF en base64
}
```

### Visualización

Odoo usa PDF.js para mostrar el documento embebido:
- El operador ve el PDF directamente en Shop Floor
- No requiere descarga externa
- Zoom y navegación incluidos

### Generar PDF con Python

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import base64

# Crear PDF
c = canvas.Canvas('/tmp/plano.pdf', pagesize=A4)
c.drawString(100, 750, 'PLANO DE ENSAMBLE')
c.save()

# Convertir a base64
with open('/tmp/plano.pdf', 'rb') as f:
    pdf_base64 = base64.b64encode(f.read()).decode()
```

---

## Configuración Manual

### 1. Crear Work Center

1. Ir a **Fabricación → Configuración → Work Centers**
2. Crear nuevo: "Producción"
3. Configurar tiempos y capacidad

### 2. Configurar Operaciones en BoM

1. Abrir un BoM existente
2. Ir a pestaña **Operaciones**
3. Agregar operaciones con:
   - **Sequence**: 10, 20, 30, 40
   - **Work Center**: Producción (el mismo para todas)
   - **Blocked by**: Seleccionar la operación anterior

### 3. Crear Quality Points

1. Ir a **Calidad → Puntos de Control**
2. Crear nuevo:
   - **Tipo de test**: Instructions
   - **Medir en**: Operation
   - **Operación**: Seleccionar la operación del BoM
3. En el campo **Hoja de trabajo (PDF)**, subir el archivo PDF

### 4. Agregar Operador

1. Ir a **Empleados**
2. Verificar que el empleado tenga:
   - Usuario vinculado
   - Sin PIN (para login automático) o con PIN conocido

---

## Uso en Shop Floor

### Acceso

URL: `https://[instancia].odoo.com/odoo/shop-floor`

### Flujo de Trabajo

1. **Login de operador**: Click en nombre → ingresar PIN (si tiene)
2. **Ver órdenes**: Aparecen las MO con work orders
3. **Iniciar trabajo**: Click en la work order → "INICIAR"
4. **Ver instrucciones**: Click en el check de instrucciones
5. **Ver PDF**: El plano se muestra embebido
6. **Completar**: Marcar como hecho y pasar a la siguiente

### Filtros Útiles

- **Información general**: Todas las MO
- **Producción**: Work orders del work center
- **Mis órdenes**: Solo las asignadas al operador

---

## Troubleshooting

### El operador aparece como "Inactivo"

1. Verificar que el empleado tenga usuario vinculado
2. Si tiene PIN, ingresarlo al hacer click en el nombre
3. Si no tiene PIN, el login es automático
4. Cerrar sesión y volver a entrar para limpiar la sesión

### Las work orders no son clickeables

1. Verificar que el work center esté en los tabs activos
2. Click en "+" para agregar el work center "Producción"
3. Limpiar localStorage del navegador (F12 → Application → Clear)

### El PDF no se muestra

1. Verificar que el Quality Point tenga `worksheet_document` configurado
2. El campo debe contener el PDF en base64
3. Crear una nueva MO para que se generen los quality checks

### Las operaciones no son secuenciales

1. Verificar que las operaciones tengan `blocked_by_operation_ids` configurado
2. Revisar que la sequence sea correcta (10, 20, 30, 40)
3. Crear una nueva MO para aplicar la configuración

---

## URLs de Acceso

| Función | URL |
|---------|-----|
| **Shop Floor** | `/odoo/shop-floor` |
| **Work Centers** | `/odoo/mrp.workcenter` |
| **Operaciones BoM** | `/odoo/mrp.routing.workcenter` |
| **Quality Points** | `/odoo/quality.point` |
| **Manufactura** | `/odoo/mrp.production` |
