# Respuestas a Consultas del Cliente - VERIFICADAS

**Fecha original consultas:** 16/12/25
**Fecha verificación técnica:** 26/12/25

---

## 1. Envío Presupuestos vía WhatsApp/Instagram

### Pregunta del Cliente:
- ¿Se pueden incluir WhatsApp e Instagram como canales para el CRM?
- ¿Tiene algún costo la implementación mensual?
- ¿Se pueden incluir imágenes/videos al presupuesto?

### Respuesta NLINKS (VERIFICADA):

**a. Inclusión de canales:**

Sí, Odoo 19 permite integrar WhatsApp e Instagram como canales de comunicación y venta, y esto puede aplicarse tanto al CRM como al proceso de presupuestos/ventas.

- Presupuestos y órdenes de venta pueden enviarse directamente por WhatsApp, incluyendo enlace al documento, imagen del producto y archivos adjuntos.
- Consultas que ingresan desde WhatsApp e Instagram pueden crear oportunidades en CRM automáticamente, permitiendo seguimiento de prospectos, historial de conversaciones, trazabilidad y reporting comercial.

**b. Costos de integración:**

- **Licencia Odoo** → no tiene costos adicionales por activar estos canales sobre la suscripción estándar.
- **WhatsApp Enterprise (Meta API)** → Meta/Facebook exige un número empresarial y plan mensual.
  - El costo depende del proveedor elegido (Ej.: Odoo Official Connector, ChatterSync, Twilio, Ultramsg, 360dialog).
- **Instagram** → también funciona vía API oficial de Meta, sin costo Odoo, pero sí proveedor externo.

> **CORRECCIÓN TÉCNICA:** Instagram en Odoo 19 Enterprise **solo soporta publicaciones y comentarios**, NO mensajes directos (DM). Para DM de Instagram se requiere módulo de terceros como:
> - Jeebra Instagram DM (~USD 45 única vez)
> - Starter Instagram Integration (~USD 82 única vez)
> - Pragmatic Instagram Integration (~USD 125-355)

**Estimación orientativa (sólo para referencia):**
Entre USD 15 y 60 mensuales para WhatsApp, dependiendo del proveedor y volumen de mensajes.

**c. Adjuntar imágenes y videos al presupuesto:**

Sí, es totalmente posible. Esto permite mostrar combinaciones color/medida/material, especialmente útil en muebles personalizados.

- Adjuntar imágenes dentro del presupuesto PDF o Online Quote.
- Enviar fotos/videos por WhatsApp al cliente.
- Incluir fotos directamente en el producto visible al cliente.

**d. Alcance funcional para el CRM y Ventas con WhatsApp/Instagram:**

Con esta funcionalidad pueden:
- Capturar leads desde mensajes entrantes automáticamente.
- Identificar canal de origen (Instagram/WhatsApp/Web).
- Conversar dentro de Odoo, sin usar el teléfono personal.
- Ver historial del cliente centralizado.
- Compartir catálogos o links de eCommerce.
- Acelerar cierres enviando presupuesto + botón "confirmar pedido".

**Alertas:**
- La integración con WhatsApp e Instagram funciona, pero requiere:
  - WhatsApp Business API (no sirve número personal común).
  - Proveedor autorizado para mensajería, cuyo costo dependerá del volumen de mensajes mensuales.
  - Mantenimiento anual del número de WhatsApp.

---

## 2. Ventas y Compras con diferentes medios de pago (Factura A/B)

### Pregunta del Cliente:
Hay Ventas y Compras que se hacen con transferencia, tarjeta, etc. (Ventas y Compras "A") y otras en efectivo (Ventas y Compras "B"). ¿En qué cambiaría al momento de los pagos a proveedores?

### Respuesta NLINKS (VERIFICADA CON ACLARACIÓN):

Sí, Odoo permite manejar ventas y compras con distintos tipos de operación: transferencias, tarjetas, efectivo, facturación A o B, sin ningún inconveniente.

Lo único que cambia en el flujo de pagos a proveedores es:
- La forma de pago vinculada al documento contable.
- El tipo de factura (A/B) que se registra al proveedor.
- La cuenta contable e impuestos que se aplican según el régimen.

En ambos casos, se hace el pago desde la misma pantalla, con conciliación automática, remitos y control de deuda sin diferencias operativas importantes.

El usuario puede:
- Pagar proveedores informales en efectivo y registrarlo como "Factura B".
- Pagar proveedores formales con transferencia y registrar "Factura A".
- Filtrar contabilidad por régimen fiscal.
- Separar reportes AFIP.
- Mantener trazabilidad de ambos tipos sin usar Excel.

> **ACLARACIÓN TÉCNICA:** La diferencia entre Factura A y Factura B en Argentina NO es "formal vs informal", sino que depende del **tipo de contribuyente**:
> - **Factura A**: Entre Responsables Inscriptos (discrimina IVA)
> - **Factura B**: De Responsable Inscripto a Consumidor Final o Monotributista (no discrimina IVA)
> - **Factura C**: De Monotributista a cualquier cliente
>
> El módulo `l10n_ar` de localización argentina maneja esto automáticamente según la configuración fiscal del proveedor/cliente.

---

## 3. Gestión de Rotura/Scrap con Autorización

### Pregunta del Cliente:
- ¿Se puede hacer procedimiento de regeneración de OP para fabricar el item roto, autorizado por un supervisor?
- ¿El material roto se puede hacer una nota con la rotura, a qué pedido pertenecía y si se envía a "Inventario de revisión" o "Descarte"?
- ¿Que impacte ese gasto adicional como pérdida?

### Respuesta NLINKS (VERIFICADA E IMPLEMENTADA):

Sí, se puede manejar la rotura de un ítem, su regeneración de orden de producción, la autorización por supervisor, y el impacto económico como pérdida o reproceso, todo con trazabilidad.

**El flujo implementado es:**

1. **Se detecta la rotura** del producto asociada al pedido y a la OP original.
2. **Se crea solicitud de aprobación** (módulo Approvals Enterprise):
   - Categoría: "Autorización de Rotura/Scrap"
   - Incluye: Producto, cantidad, referencia MO/PO, monto pérdida
3. **El supervisor revisa y aprueba/rechaza** desde Aprobaciones.
4. **Si aprobado, se registra el Scrap**:
   - Destino: "Revisión" (evaluar recuperación) o "Descarte" (pérdida definitiva)
   - Campo `should_replenish`: controla si se regenera automáticamente la OP
5. **Impacto contable automático**:
   - Movimiento de stock registra la pérdida
   - Asiento contable debita cuenta de pérdidas, acredita inventario

> **IMPLEMENTADO EN SETUP:** El script `setup_real.py` configura automáticamente:
> - Módulo Approvals instalado
> - Categoría "Autorización de Rotura/Scrap" con campos requeridos
> - Ubicaciones "Revisión" y "Descarte" creadas
> - Aprobadores configurados
>
> Ver documentación completa: `docs/parte4/03-gestion-rotura-scrap.md`

---

## ANEXO A: Carga Automática de Componentes

### Preguntas del Cliente:
- ¿La carga de ítems se hace automáticamente?
- ¿Se pueden incluir detalles de terminación elegidos por el cliente?
- ¿El workflow está predeterminado para cada producto?
- ¿Se puede modificar ese workflow para un pedido en particular?

### Respuesta NLINKS (VERIFICADA):

**a. Carga de componentes:**

Sí, Odoo permite que los componentes que forman un producto (tapa cruda, tapa lustrada, patas metálicas, etc.) se carguen automáticamente cuando se vende el producto final.

Esto se hace configurando:
- Listas de materiales (BOM)
- Rutas de fabricación
- Reglas de subcontratación

Además, cada componente generado automáticamente puede validarse manualmente paso a paso antes de avanzar el proceso.

**b. Sobre incluir detalles de terminación del cliente:**

Sí. En la venta se pueden agregar terminaciones personalizadas mediante:
- Variantes de producto
- Atributos configurables
- Campos personalizados en el pedido

**c. Sobre workflow predeterminado:**

Sí, el flujo operativo por producto viene definido automáticamente con la BOM y rutas.

**d. ¿Puede modificarse manualmente el workflow para un pedido puntual?**

Sí. El usuario puede, para un pedido en particular:
- Agregar/remover componentes
- Cambiar cantidades
- Cambiar proveedor
- Modificar fechas
- Cambiar ruta productiva
- Alterar operaciones

Sin romper el estándar del producto.

---

## ANEXO B: Envío de OP a Proveedores

### Preguntas del Cliente:
- ¿Se pueden usar WhatsApp, mail, imprimir papel para enviar las OP?
- ¿Tiene algún costo adicional el envío por WhatsApp?
- ¿Se necesita algún Template de activación de conversación?

### Respuesta NLINKS (VERIFICADA):

**a. Envío de Orden de Compra al proveedor:**

Sí, Odoo permite enviar órdenes de compra directamente a proveedores por email o imprimirlas para uso físico sin costos adicionales.

El flujo estándar es:
1. Se confirma la orden de compra
2. El sistema envía un correo electrónico al proveedor con el PDF adjunto
3. O bien se imprime la orden para entregar físicamente

**b. Sobre WhatsApp:**

Es posible enviar la orden por WhatsApp también, pero requiere una integración opcional.

- **WhatsApp manual** → posible sin costo (descargar PDF y enviar por WhatsApp Web)
- **WhatsApp automatizado desde Odoo** → requiere integración y puede tener costo externo

**c. Plantillas de inicio de conversación:**

No es necesario usar como en CRM. Para proveedores, la comunicación es directa: el PDF se envía al número del proveedor igual que un mail.

**Resumen:**
| Canal | Costo |
|-------|-------|
| Email | Incluido, sin costo adicional |
| Impresión | Incluida, sin costo adicional |
| WhatsApp manual | Posible sin costo |
| WhatsApp automatizado | Requiere integración (costo externo) |

---

## ANEXO C: Seguimiento de OP

### Preguntas del Cliente:
- ¿Se puede visualizar todas las OP con filtros por venta, proveedor, ítem, fecha?
- ¿Se puede ver resumen del tiempo faltante de entrega?
- ¿Se puede marcar un ítem como "Disponible" y registrar fechas?
- ¿Se puede hacer flujo de reverso por rechazo de calidad?

### Respuesta NLINKS (VERIFICADA CON CORRECCIONES):

**a. Visualizar todas las OP activadas + filtros:**

Sí, es totalmente posible. En el sistema se puede generar una vista/tabla de seguimiento donde aparezcan todas las OP activas, y agregar filtros dinámicos por:
- Nº de Orden de Venta
- Nº de OP
- Proveedor asignado
- Ítem del producto
- Fecha de pedido
- Fecha estimada de recepción
- Estado actual de la etapa

> **CORRECCIÓN:** Los filtros son **nativos** en Odoo. El campo `origin` en `purchase.order` y `mrp.production` contiene la referencia al documento origen (SO). Los filtros por proveedor, fecha, estado están disponibles por defecto.

**b. Resumen del tiempo faltante de entrega:**

Sí, también es posible. Se puede calcular mediante: Fecha de Venta → Fecha actual y mostrar:
- Días transcurridos desde la venta
- Tiempo estimado restante por etapa
- Alerta automática si se excede el plazo

> **CORRECCIÓN:** Odoo tiene campos `date_deadline` y `date_start`/`date_finished` en MO. Para alertas automáticas de plazo excedido, se requiere configurar **Acciones Automatizadas** (base_automation) - no es automático out-of-the-box.

**c. Marcar un ítem como "Disponible":**

Sí, el sistema puede manejar este flujo mediante los estados de picking:
- `assigned` = Reservado/Disponible
- `done` = Transferido

Las fechas se registran automáticamente en cada cambio de estado:
- `scheduled_date` = fecha planificada
- `date_done` = fecha real de transferencia

> **CORRECCIÓN:** Esto es **nativo** en el flujo de pickings. Cuando el proveedor confirma que está listo, se valida el picking de recepción y automáticamente queda registrada la fecha.

**d. Flujo de reverso manual por rechazo:**

Sí, puede hacerse con estructura de workflow manual controlado.

**Caso 1: falla en lustre:**
Flujo: Etapa 3 → vuelve a Etapa 2 → vuelve a Etapa 3

**Caso 2: falla estructural:**
Flujo: Etapa 3 → vuelve a Etapa 1 → Etapa 2 → Etapa 3

> **CORRECCIÓN IMPORTANTE:** El "reverso" en Odoo se maneja mediante:
> 1. **Scrap del producto defectuoso** (registra la pérdida)
> 2. **Nueva MO/PO de reposición** (genera nuevo flujo desde la etapa que corresponda)
>
> NO existe un "botón de reverso" que mueva el producto hacia atrás en el flujo. La trazabilidad se mantiene vinculando el scrap a la MO original y la nueva MO de reposición.

---

## ANEXO D: Tareas de Ensamble

### Preguntas del Cliente:
- ¿Se pueden adicionar planos, videos y notas a la tarea de ensamble?
- ¿Se puede emitir alerta visual cuando ingresa nuevo producto para entrega?
- ¿Se puede establecer criterio automático de prioridades?

### Respuesta NLINKS (VERIFICADA CON CORRECCIONES):

**a. Adjuntar planos, videos y notas:**

Sí, técnicamente es totalmente viable.

**Opciones técnicas nativas:**
- Archivos adjuntos en Work Order (PDF, imágenes)
- Notas estructuradas en campos de operación
- Videos: link YouTube/servidor privado (recomendado) o archivo mp4

> **CORRECCIÓN:** Los documentos se adjuntan a nivel de **producto** en la BoM (`product.document` con `attached_on_mrp='bom'`), NO directamente a la Work Order. La Work Order **no tiene chatter** en el módulo base.
>
> Para worksheets personalizadas con instrucciones paso a paso, se requiere el módulo `quality_mrp_workorder_worksheet`, que **depende de Odoo Studio** (`web_studio`).

**b. Alerta visual a logística cuando producto terminado:**

Sí, cuando el operario marca ensamble completado, el workflow pasa a estado "Listo para entregar".

> **IMPLEMENTADO EN SETUP:** Configuramos una **Acción Automatizada** que:
> - Se dispara cuando MO cambia a estado `done`
> - Envía notificación al grupo "Logística" en el chatter de la MO
> - Opcionalmente puede enviar email
>
> Ver documentación: `docs/parte4/04-alertas-automatizadas.md`
>
> Para activar:
> 1. Agregar usuarios al grupo "Logística"
> 2. (Opcional) Descomentar líneas de email en la acción de servidor

**c. Priorización automática de tareas:**

> **CORRECCIÓN IMPORTANTE:** El campo `priority` en `mrp.production` solo tiene **2 valores nativos**:
> - `0` = Normal
> - `1` = Urgent
>
> **NO existe** priorización automática compleja basada en fechas, antigüedad, etc. de forma nativa.
>
> **Para implementar priorización como describe el cliente** (columna numérica 1,2,3... con fallback a fecha de venta), se requiere:
> - Desarrollo custom para agregar campo de prioridad numérica
> - Acción automatizada para ordenar/calcular prioridades
> - Vista personalizada que ordene por este campo
>
> **Alternativa sin desarrollo:** Usar el campo `priority` existente (Normal/Urgent) + ordenar por `date_start` para mantener orden por antigüedad.

---

## ANEXO E: Integración Google Maps

### Preguntas del Cliente:
- ¿Se puede vincular Odoo con Google Maps para visualizar destinos de entrega?
- ¿Se puede visualizar en mapa automáticamente cuando un producto está terminado o en ensamble?

### Respuesta NLINKS (VERIFICADA):

**Integración con Google Maps:**

Sí. Odoo permite integraciones de direcciones de entrega con mapa.

**Módulos disponibles:**

| Módulo | Tipo | Funcionalidad |
|--------|------|---------------|
| `base_geolocalize` | Community | Geolocalización de partners (lat/long) |
| `website_google_map` | Community | Muestra mapa en website |
| `industry_fsm` | Enterprise | Vista mapa para Field Service |

**Proveedores de geolocalización:**

| Proveedor | Costo | Uso |
|-----------|-------|-----|
| OpenStreetMap | Gratis | Por defecto (Nominatim) |
| Google Maps | Pago | Requiere API Key |

**Funcionalidades posibles:**
- Ver en mapa las entregas pendientes
- Filtrar por estado (en fabricación, listo para despacho, etc.)
- Estados con colores diferentes
- Calcular rutas y distancias (requiere API Google Maps pago)

**Configuración:**
Ajustes → Configuración General → Integraciones → Proveedor de Geocodificación

> **NOTA:** Para rutas optimizadas, tracking en móvil o geolocalización automática, se requiere **licencia API Google Maps** (servicio pago de Google).
>
> Sin Google Maps pago, se puede usar:
> - Vista mapa nativa de Odoo (básica)
> - Coordenadas GPS cargadas por dirección

---

## Consolidación de POs por Proveedor

### Preguntas del Cliente:

**Caso a)** 2 ventas diferentes, mismo producto: ¿Se puede enviar al proveedor una sola OP con los items de ambas ventas?

**Caso b)** 1 venta con 2 productos (mesa + sillas): ¿Se puede enviar una sola OP al Carpintero con los ítems de ambos productos?

### Respuesta NLINKS (VERIFICADA):

**Caso a) Agrupar ítems de múltiples pedidos de venta:**

Sí, es posible. Cuando 2 ventas diferentes requieren componentes que provienen del mismo proveedor/subcontratista, Odoo puede generar una sola Orden de Compra consolidada.

Esto permite:
- Menos órdenes
- Menos emails
- Mejor comunicación
- Control más claro de costos por proveedor

Es 100% trazable y no tiene costo extra. Es funcionalidad nativa de compras/manufactura.

**Caso b) Consolidar múltiples componentes de una venta:**

Sí, Odoo permite consolidar múltiples componentes destinados al mismo proveedor/subcontratista en una única Orden de Compra.

En el ejemplo, el Carpintero recibiría una sola PO con:
- Tapa 2x1 mts (Mesa)
- Tapa 1x1 mts (Mesa)
- 8 esqueletos de silla

**Trazabilidad mantenida:**
Cada línea puede mostrar:
- Referencia a la venta
- Nombre del cliente
- Tipo de producto
- Medidas/terminación
- Notas técnicas
- Cantidades separadas

> **VERIFICACIÓN TÉCNICA:** La consolidación de POs es **nativa** en Odoo mediante las reglas de reabastecimiento y el scheduler de compras. Se configura en:
> - Producto → Inventario → Rutas → Comprar
> - Reglas de reabastecimiento con agrupación por proveedor
>
> El campo `origin` en cada línea de PO mantiene la referencia al documento origen (SO/MO).

---

## Resumen de Implementaciones Realizadas

| Funcionalidad | Estado | Ubicación |
|---------------|--------|-----------|
| Gestión Rotura/Scrap | ✅ Implementado | `setup_real.py` sección 12 |
| Alertas a Logística | ✅ Implementado | `setup_real.py` sección 13 |
| Ubicaciones Revisión/Descarte | ✅ Implementado | `setup_real.py` sección 12 |
| Categoría Aprobación Scrap | ✅ Implementado | `setup_real.py` sección 12 |
| Grupo Logística | ✅ Implementado | `setup_real.py` sección 13 |
| Documentación Scrap | ✅ Documentado | `docs/parte4/03-gestion-rotura-scrap.md` |
| Documentación Alertas | ✅ Documentado | `docs/parte4/04-alertas-automatizadas.md` |

---

## Correcciones Importantes a Comunicar al Cliente

1. **Instagram DM**: NO es nativo. Solo posts/comentarios. DM requiere módulo de terceros.

2. **Factura A/B**: No es "formal vs informal", sino tipo de contribuyente (RI, CF, Monotributista).

3. **Priorización automática de tareas**: Solo Normal/Urgent nativo. Priorización numérica requiere desarrollo.

4. **Adjuntos en Work Order**: Van en el producto/BoM, no directamente en WO. Worksheets requieren Studio.

5. **Reverso de producción**: No existe "botón reverso". Se maneja con Scrap + nueva MO de reposición.

6. **Alertas a logística**: Requiere configuración de Acción Automatizada (ya implementada en setup).
