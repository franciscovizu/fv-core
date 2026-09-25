# FV® Import-to-Finance Architecture

**Autor / originador:** José Francisco Villaseñor Zúñiga (Francisco Villaseñor)  
**Marca raíz:** FV®  
**Estado actual:** Diseño funcional / prototipo avanzado (~60% de avance en la etapa de importaciones, según registro del autor).  
**Fecha de documentación en este repositorio:** 25-sep-2026.

> Nota histórica del autor: el concepto tiene antecedentes de trabajo desde 2010. Francisco Villaseñor identifica en esa etapa a Manuel Parvol, Magda Barba y Yael Ramírez como personas relacionadas con esos antecedentes. Esta nota documenta el antecedente declarado por el autor y no sustituye evidencia histórica independiente.

## Propósito

Diseñar una arquitectura integral de trazabilidad para conectar el ciclo documental, operativo, fiscal, contable y financiero de una importación, desde la fuente documental hasta la toma de decisiones gerencial.

## Cadena principal FV®

```text
FV® Connector
  -> FV® XML
  -> FV® CFDI
  -> FV® Odoo
      -> Provisión
      -> Costo
      -> Gastos de importación
      -> Inventario
  -> FV® Impuestos
  -> FV® Importación
  -> FV® NIF
  -> FV® Dashboard
```

## Capa de decisión y control

```text
FV® Ciclo Operativo
  -> FV® Lead Time
  -> FV® Liquidez
  -> Evaluación de devolución de IVA
  -> FV® Budget / Forecast
```

## Alcance funcional

### 1. FV® Connector
Entrada controlada de información y documentos provenientes de fuentes operativas, fiscales, bancarias y comerciales.

### 2. FV® XML / FV® CFDI
Normalización, identificación, clasificación y trazabilidad de XML/CFDI, incluyendo relaciones PUE/PPD, pagos, impuestos y documentos asociados.

### 3. FV® Odoo
Integración funcional con ERP para compras, ventas, inventario, contabilidad, bancos, impuestos, analítica y documentación.

### 4. Provisión, costo y gastos de importación
Estructuración previa y posterior al reconocimiento contable de:
- provisiones;
- gastos de importación;
- costos directos e indirectos;
- costos asociados al inventario;
- diferencias y ajustes;
- trazabilidad por operación / embarque / documento.

### 5. Inventario
Vinculación de costo, recepción, disponibilidad, movimientos y valorización con la documentación y la operación de importación.

### 6. FV® Impuestos
Control de IVA, retenciones, impuestos relacionados, efectos fiscales y trazabilidad documental.

### 7. FV® Importación
Concentración de la operación de comercio exterior, incluyendo cuando aplique:
- pedimento;
- DODA;
- COVE;
- contribuciones;
- pagos;
- costos;
- gastos;
- inventario;
- documentos soporte.

### 8. FV® NIF
Traducción del ciclo operativo a información financiera y materialidad, incluyendo lectura gerencial de estados financieros y efectos en presentación / revelación según corresponda.

### 9. FV® Dashboard
Panel de control para consolidar indicadores operativos, fiscales, contables y financieros.

## Indicadores previstos

- Ciclo operativo.
- Lead time.
- Liquidez.
- Presupuesto y forecast.
- Costo total de importación.
- Variación entre provisión y costo real.
- Inventario recibido / disponible / valorizado.
- IVA acreditable y análisis de posible devolución.
- Trazabilidad documental completa.
- Conciliación entre plataformas digitales, ERP, SAT, XML y estados financieros.

## Arquitectura complementaria para plataformas digitales

```text
Plataformas digitales
  -> ERP
  -> SAT
  -> XML / CFDI
  -> NIF
  -> Dashboard
```

Objetivo: reconciliar operaciones de eCommerce / plataformas digitales con múltiples estados de cuenta, cobros, comisiones, retenciones, depósitos y registros ERP, preservando consistencia operativa, fiscal, contable y financiera.

## Principios de diseño

- Trazabilidad end-to-end.
- Evidencia auditable.
- Integridad de datos.
- Identificadores consistentes.
- Separación entre origen, transformación y registro.
- Control de materialidad.
- Conciliación entre operación, fiscalidad y contabilidad.
- Capacidad de operar aun cuando no exista integración automática entre plataformas.
- Diseño orientado a decisión gerencial, no solo a captura contable.

## Antecedente operativo relevante

En implementaciones previas, por decisión directiva no se habilitó la conexión automática entre Odoo y Mercado Libre para preservar control sobre inventarios. Se diseñó una trazabilidad manual controlada para relacionar pedido, venta, logística, comisiones, retenciones, Mercado Pago, depósitos, conciliación bancaria y CFDI/SAT. Ese enfoque es antecedente directo de esta arquitectura de integración y control.

## Diferenciador

El valor no está únicamente en leer XML o registrar una importación. La propuesta conecta:

**documento -> operación -> ERP -> inventario -> impuesto -> NIF -> liquidez -> presupuesto -> dashboard**

Esto convierte la importación en un ciclo financiero-operativo completo y trazable.

## Autoría y alcance

La arquitectura, metodología, nomenclatura FV® y diseño funcional aquí descritos se documentan como trabajo originado por José Francisco Villaseñor Zúñiga. Las referencias a empresas, plataformas, ERP, normativa o terceros se usan únicamente para describir contexto funcional y no implican propiedad sobre marcas, sistemas o activos de terceros.
