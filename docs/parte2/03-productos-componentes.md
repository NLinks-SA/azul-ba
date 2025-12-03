# 3. Productos Componentes

Antes de crear la Mesa, debemos crear sus componentes: Tapas y Bases.

## Acceder a Productos

```
Inventario → Productos → Productos
```

---

## 3.1 Bases Metálicas

Las bases se compran al proveedor Metalúrgica como subcontratación.

### Crear: Base Acero Negro 180x90

Click en **Nuevo**

#### Pestaña: Información General

| Campo | Valor |
|-------|-------|
| **Nombre** | Base Acero Negro 180x90 |
| **Referencia interna** | BASE-NEGRO-18090 |
| **Tipo de producto** | Almacenable |
| **Categoría** | Mobiliario / Bases |
| **Precio de venta** | 0 (no se vende) |
| **Coste** | 150.00 |

#### Pestaña: Compra

| Campo | Valor |
|-------|-------|
| **Se puede comprar** | ✅ Sí |

En sección **Proveedores** (tabla):

| Proveedor | Precio | Tiempo de entrega |
|-----------|--------|-------------------|
| Metalúrgica Precisión S.A. | 150.00 | 5 días |

#### Pestaña: Inventario

| Campo | Valor |
|-------|-------|
| **Rutas** | ☑ Buy, ☑ Replenish on Order (MTO) |

!!! warning "Importante: Rutas"
    Las rutas **Buy + MTO** son críticas.

    - **Buy**: Indica que se compra
    - **MTO**: Genera PO automáticamente cuando hay demanda

**Guardar**

---

### Crear las otras Bases

Repetir el proceso para:

| Producto | Código | Costo |
|----------|--------|-------|
| Base Acero Negro 220x100 | BASE-NEGRO-22010 | 180.00 |
| Base Acero Dorado 180x90 | BASE-DORADO-18090 | 180.00 |
| Base Acero Dorado 220x100 | BASE-DORADO-22010 | 220.00 |

!!! tip "Duplicar producto"
    Podés usar **Acción → Duplicar** para crear productos similares más rápido.

---

## 3.2 Tapas Mármol

Compra directa a Marmolería (no es subcontratación, proveen el producto completo).

### Crear: Tapa Mármol Carrara 180x90

#### Pestaña: Información General

| Campo | Valor |
|-------|-------|
| **Nombre** | Tapa Mármol Carrara 180x90 |
| **Referencia interna** | TAPA-MARMOL-18090 |
| **Tipo de producto** | Almacenable |
| **Coste** | 450.00 |

#### Pestaña: Compra

| Proveedor | Precio | Tiempo de entrega |
|-----------|--------|-------------------|
| Marmolería Del Sur | 450.00 | 7 días |

#### Pestaña: Inventario

| Campo | Valor |
|-------|-------|
| **Rutas** | ☑ Buy, ☑ Replenish on Order (MTO) |

**Guardar**

---

### Crear otras Tapas simples

| Producto | Código | Proveedor | Precio | Lead Time |
|----------|--------|-----------|--------|-----------|
| Tapa Mármol Carrara 220x100 | TAPA-MARMOL-22010 | Marmolería | 550.00 | 7 días |
| Tapa Neolith Negro 180x90 | TAPA-NEOLITH-18090 | Neolith Argentina | 380.00 | 10 días |
| Tapa Neolith Negro 220x100 | TAPA-NEOLITH-22010 | Neolith Argentina | 480.00 | 10 días |

Todas con rutas: **Buy + MTO**

---

## 3.3 Tapas de Madera - Sin Terminar

Estas tapas se compran a Carpintería y luego van al Lustrador.

### Crear: Tapa Madera Sin Terminar 180x90

#### Pestaña: Información General

| Campo | Valor |
|-------|-------|
| **Nombre** | Tapa Madera Sin Terminar 180x90 |
| **Referencia interna** | TAPA-MADERA-ST-18090 |
| **Tipo de producto** | Almacenable |
| **Coste** | 120.00 |

#### Pestaña: Compra

| Proveedor | Precio | Tiempo de entrega |
|-----------|--------|-------------------|
| Carpintería Artesanal Hnos. García | 120.00 | 5 días |

#### Pestaña: Inventario

| Campo | Valor |
|-------|-------|
| **Rutas** | ☑ Buy, ☑ Replenish on Order (MTO), ☑ Resupply Lustrador |

!!! info "Ruta Resupply Lustrador"
    Esta ruta se crea en [Parte 1 - Configuración de Inventario](../parte1/02-config-inventario.md#25-crear-ruta-resupply-lustrador).
    Es necesaria para propagar el MTO y generar automáticamente la PO a Carpintería.

**Guardar**

---

### Crear otra Tapa Sin Terminar

| Producto | Código | Precio |
|----------|--------|--------|
| Tapa Madera Sin Terminar 220x100 | TAPA-MADERA-ST-22010 | 150.00 |

Con las mismas rutas: **Buy + MTO + Resupply Lustrador**

---

## 3.4 Tapas de Madera - Terminadas (Con Variantes)

Estas tapas tienen 3 tipos de terminación. Usamos variantes.

### Crear: Tapa Madera Terminada 180x90

#### Pestaña: Información General

| Campo | Valor |
|-------|-------|
| **Nombre** | Tapa Madera Terminada 180x90 |
| **Referencia interna** | TAPA-MADERA-TERM-18090 |
| **Tipo de producto** | Almacenable |
| **Coste** | 280.00 |

#### Pestaña: Atributos y Variantes

Agregar línea:

| Atributo | Valores |
|----------|---------|
| Terminación | Lustre Mate, Lustre Brillante, Natural |

Al guardar, se crean **3 variantes** automáticamente.

#### Pestaña: Compra

!!! warning "Proveedor en Tapas Terminadas"
    Aunque el Lustrador es subcontratista, necesitamos configurar el supplierinfo para que las POs se generen automáticamente.

| Proveedor | Precio | Tiempo de entrega |
|-----------|--------|-------------------|
| Lustres & Acabados Premium | 280.00 | 3 días |

#### Pestaña: Inventario

| Campo | Valor |
|-------|-------|
| **Rutas** | ☑ Buy, ☑ Replenish on Order (MTO) |

**Guardar**

---

### Crear otra Tapa Terminada

| Producto | Código | Precio |
|----------|--------|--------|
| Tapa Madera Terminada 220x100 | TAPA-MADERA-TERM-22010 | 350.00 |

Con el mismo atributo **Terminación** (3 valores).

---

## Verificación

### Lista de Componentes

```
Inventario → Productos → Productos
```

Filtrar por categoría "Bases" y "Tapas":

| Producto | Rutas | Proveedor |
|----------|-------|-----------|
| Base Acero Negro 180x90 | Buy + MTO | Metalúrgica |
| Base Acero Negro 220x100 | Buy + MTO | Metalúrgica |
| Base Acero Dorado 180x90 | Buy + MTO | Metalúrgica |
| Base Acero Dorado 220x100 | Buy + MTO | Metalúrgica |
| Tapa Mármol Carrara 180x90 | Buy + MTO | Marmolería |
| Tapa Mármol Carrara 220x100 | Buy + MTO | Marmolería |
| Tapa Neolith Negro 180x90 | Buy + MTO | Neolith |
| Tapa Neolith Negro 220x100 | Buy + MTO | Neolith |
| Tapa Madera Sin Terminar 180x90 | Buy + MTO + Resupply Lustrador | Carpintería |
| Tapa Madera Sin Terminar 220x100 | Buy + MTO + Resupply Lustrador | Carpintería |
| Tapa Madera Terminada 180x90 (3 var) | Buy + MTO | Lustrador |
| Tapa Madera Terminada 220x100 (3 var) | Buy + MTO | Lustrador |

---

## Resumen

| Tipo | Cantidad | Variantes |
|------|----------|-----------|
| Bases | 4 | - |
| Tapas Mármol | 2 | - |
| Tapas Neolith | 2 | - |
| Tapas Madera Sin Terminar | 2 | - |
| Tapas Madera Terminada | 2 | 6 (3 cada una) |
| **Total productos** | **12** | **6** |
