# 3. Configuración de Compras

## Acceder a la Configuración

```
Compras → Configuración → Ajustes
```

---

## 3.1 Activar Subcontratación

### Ubicación
```
Compras → Configuración → Ajustes → Logística
```

### Configuración

- [x] **Subcontracting** (Subcontratación)

!!! info "¿Qué habilita esto?"
    - Permite crear BoMs de tipo "Subcontratación"
    - Asocia subcontratistas a BoMs específicas
    - Gestiona el envío de materiales al proveedor
    - Controla la recepción del producto terminado

### Guardar
Click en **Guardar**

---

## 3.2 Verificar que está Activo

Después de activar, al crear una BoM deberías ver:

- Campo **Tipo de BoM** con opción "Subcontratación"
- Campo **Subcontratistas** para asignar proveedores

---

## Resultado Esperado

Con la subcontratación activa, el flujo será:

```
1. Orden de Compra al subcontratista
         │
         ▼
2. Odoo envía automáticamente los materiales
   (según la BoM de subcontratación)
         │
         ▼
3. Subcontratista produce el producto
         │
         ▼
4. Recibimos el producto terminado
   (con control de calidad si está configurado)
```

---

## Resumen

| Configuración | Valor |
|---------------|-------|
| Subcontracting | ✅ Activado |
