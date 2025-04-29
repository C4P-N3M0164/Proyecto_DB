# Actividad Proyecto - Contenedor

## Estructura base de datos e inserción de datos de prueba

### 🛠️ Paso a paso

1. Clona el repositorio usando el siguiente enlace:
**Nota**: Si usted es el profesor no vuelva a clonar el repositorio porque todos los archivo del repositorio estan en el .zip enviado. 🫡 

   ```
   https://github.com/C4P-N3M0164/Proyecto_DB.git
   ```

2. Abre Docker Desktop si aún no lo tienes abierto.
3. Abre una terminal con la ruta base del proyecto.
4. Crea la imagen en base a los archivos descargados con el siguiente comando:

   ```
   docker-compose up --build
   ```

5. Espera a que la imagen termine de construirse.
6. Ejecuta el siguiente comando para acceder a la base de datos:

   ```
   docker exec -it mysql-energia mysql -u root -p
   ```

7. Ejecuta el siguiente comando para listar las bases de datos disponibles:

   ```sql
   show databases;
   ```

8. Para usar una base de datos específica, usa el siguiente comando:

   ```sql
   use energia;
   ```

9. Si deseas listar las tablas dentro de la base de datos, usa:

   ```sql
   show tables;
   ```

10. Realiza las consultas que requieras.

---

## Justificación del Modelo

### 🔍 1. Precio_Energía (MetricName: `valor_cop_kwh`)

- **Descripción:** Representa el precio unitario de la energía en pesos colombianos por kilovatio-hora (COP/kWh) para un sistema energético y una fecha determinada.
- **Relación clave:** Relacionada con la tabla `sistema_energetico`.
- **Valor analítico:** Permite conocer los periodos de precios altos o bajos.
- **Enfoque de rentabilidad:** Comprar cuando el precio esté bajo y vender cuando esté alto para maximizar márgenes.

---

### 🔍 2. Demanda_Energética (MetricName: `valor_kwh`)

- **Descripción:** Valor de energía demandada (kWh) por un agente del mercado en una fecha y hora específicas.
- **Relación clave:** Vinculada con la tabla `agente_mercado`.
- **Valor analítico:** Analiza picos, caídas y patrones horarios.
- **Enfoque de rentabilidad:** Ajustar producción a los picos y evitar desperdicio.

---

### 🔍 3. Transacción_Energética (MetricName: `volumen_kwh`)

- **Descripción:** Volumen de energía efectivamente transado por un agente en kWh.
- **Relación clave:** También vinculada a `agente_mercado`.
- **Valor analítico:** Mide el flujo energético comercializado.
- **Enfoque de rentabilidad:** Maximizar volumen transado en momentos clave del mercado.

---

## 📈 Correlación entre Métricas

| Métrica               | Relación                    | Patrón a identificar                          |
|-----------------------|-----------------------------|-----------------------------------------------|
| Precio + Demanda      | Alta demanda + precio alto  | Oportunidad para maximizar ingresos.          |
| Demanda + Transacción | Alta demanda, bajo volumen  | Pérdida por falta de cobertura.               |
| Precio + Transacción  | Alto volumen, precio bajo   | Menor margen de ganancia.                     |

---

## 📊 Consulta Analítica SQL

Esta consulta agrupa la información por fecha y sistema energético para estimar ingresos:

```sql
SELECT 
    pe.fecha,
    se.nombre_sistema,
    pe.valor_cop_kwh,
    
    SUM(de.valor_kwh) AS demanda_total_kwh,
    SUM(te.volumen_kwh) AS volumen_transado_kwh,
    
    (SUM(te.volumen_kwh) * pe.valor_cop_kwh) AS ingreso_estimado_cop

FROM precio_energia pe

JOIN sistema_energetico se ON pe.id_sistema = se.id_sistema
LEFT JOIN agente_mercado am_de ON am_de.id_agente IN (
    SELECT id_agente FROM demanda_energetica
)
LEFT JOIN demanda_energetica de ON de.id_agente = am_de.id_agente AND de.fecha = pe.fecha

LEFT JOIN agente_mercado am_te ON am_te.id_agente IN (
    SELECT id_agente FROM transaccion_energetica
)
LEFT JOIN transaccion_energetica te ON te.id_agente = am_te.id_agente AND te.fecha = pe.fecha

GROUP BY pe.fecha, se.nombre_sistema, pe.valor_cop_kwh
ORDER BY pe.fecha ASC;
```
