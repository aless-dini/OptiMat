# Guion de la simulación de OptiMat (2 personas)

Duración total: unos 4 minutos. Diapositivas: 11 (Producto final), 12 (Simulación) y 13 (Semáforo de stock) de la versión v2 del PPT.

- **Persona 1** muestra el reporte: explica **qué calcula** OptiMat.
- **Persona 2** usa el menú: muestra **cómo reacciona** OptiMat cuando cambian los datos.

---

## Antes de grabar (los dos)

1. Abrir una **terminal** en la carpeta `OptiMat` (en VS Code: Terminal → Nueva terminal). No usar el panel *Output*.
2. Agrandar la letra de la terminal (Ctrl + rueda del mouse) para que se lea en el video.
3. Ejecutar `python main.py` y elegir **9** (restaurar datos de ejemplo), así todos los números coinciden con este guion. Luego **0** para salir.
4. Ensayar una vez completo con el cronómetro.
5. Los dos deben aparecer en cámara mientras hablan.

---

## Persona 1: el reporte (≈ 2 min)

**Diapositiva 11 → pasar a la terminal.**

> "A continuación, realizaremos una simulación de OptiMat con datos de ejemplo de una pyme que abastece a tres clientes desde una bodega."

| Acción | Qué decir |
|---|---|
| Escribir `python main.py` | "Al ejecutar el programa aparece un menú con las operaciones disponibles." |
| Elegir **1** (Ver reporte completo) | "Primero revisaremos el reporte completo." |
| Sección **1) Unidades por despachar** | "Esta tabla es una **resta de matrices**: la matriz de pedidos menos la matriz de entregas. Por ejemplo, el Cliente A pidió 40 teclados y recibió 20, por lo tanto faltan 20." |
| Sección **2) Costo de despacho** | "Aquí se aplica el **producto de matriz por vector**: las unidades pendientes por la tarifa de flete de cada cliente. Para los teclados: 20 por 1.500, más 0 por 2.500, más 20 por 4.000, da 110.000 pesos. El costo total es de **428.000 pesos**." |
| Sección **3) Bodega vs. pendientes** | "Con una **sumatoria por fila** se obtiene el total pendiente de cada producto. En notebooks se deben 12 y hay 9 en bodega: **faltan 3**." |
| Sección **4) Demanda proyectada** | "La demanda es el **promedio** de seis meses de ventas. El mouse vende en promedio 129,7 unidades al mes y hay 125 en bodega, por eso aparece el riesgo de quiebre." |
| Sección **6) Semáforo** | "El semáforo divide el stock por lo pendiente y lo expresa en porcentaje. Los notebooks están en **75 %, en rojo**, porque no alcanza para cumplir." |
| Sección **7) Pedido sugerido** | "Finalmente, el programa sugiere cuánto comprar: lo pendiente más la demanda, menos el stock. Para notebooks sugiere **22 unidades**." |
| Presionar **Enter** | (vuelve al menú) |

**Traspaso:**
> "Hasta aquí vimos lo que calcula OptiMat. Ahora [nombre de la Persona 2] mostrará cómo el programa reacciona cuando la empresa registra movimientos."

---

## Persona 2: el programa en acción (≈ 2 min)

**Sigue en la terminal, en el menú.**

| Acción | Qué decir | Qué debe aparecer |
|---|---|---|
| Elegir **3** (Registrar una entrega), producto **4** (Notebooks), cliente **1** (Cliente A), unidades **6** | "Supongamos que despachamos 6 notebooks al Cliente A. El programa valida que no entreguemos más de lo pendiente ni más de lo que hay en bodega." | `Costo de este flete: $9.000` |
| Mostrar el resumen | "El costo total baja de 428.000 a **419.000 pesos**, porque 6 por 1.500 son 9.000. Pero la bodega quedó con solo 3 notebooks y el semáforo sigue en **rojo**." | `$419.000` y `Notebooks ... 50 % -> ROJO` |
| **Enter**, elegir **4** (Recibir mercadería) | "Para resolverlo, registramos una compra al proveedor. OptiMat sugiere comprar 22 notebooks." | `Notebooks 22` en el pedido sugerido |
| Producto **4**, unidades **20** | "Recibimos 20 unidades." | `Stock de Notebooks actualizado a 23 unidades` |
| Mostrar el resumen | "Con esta compra, los notebooks pasan a **verde**: ahora el stock cubre más de tres veces lo pendiente." | `Notebooks ... 383 % -> VERDE` |
| **Enter**, elegir **8** (Generar gráfico) | "Por último, el programa genera el gráfico del semáforo." | Se abre `alertas.png` |
| Mostrar el gráfico (o pasar a la **diapositiva 13**) | "Cada barra muestra el porcentaje de cumplimiento de un producto y las líneas marcan los umbrales de 100 % y 150 %." | |
| Cerrar la imagen, **Enter**, elegir **9** y responder **s** | "Restauramos los datos de ejemplo para dejar el programa listo." | |
| Elegir **0** (Salir) | | |

**Cierre:**
> "Así, OptiMat reemplaza el control manual: cada movimiento se recalcula al instante con matrices, vectores y sumatorias."

---

## Si algo sale mal durante la grabación

- **Se equivocan al escribir un número:** el programa avisa y vuelve a preguntar. No hay que reiniciar.
- **Los números no coinciden:** elegir **9** para restaurar los datos de ejemplo y repetir la parte.
- **El gráfico tarda en abrirse:** mostrar la diapositiva 13, que tiene el mismo gráfico.
