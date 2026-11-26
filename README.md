# OptiMat

Prototipo en Python para una pyme de retail tecnológico que vende desde una bodega
a varios clientes. Calcula cuántas unidades faltan por despachar a cada cliente,
cuánto cuesta ese despacho, si el stock de la bodega alcanza y qué productos
tienen riesgo de quiebre de stock, con un semáforo de alertas y su gráfico.
Funciona con un menú interactivo en la consola: se pueden registrar pedidos, entregas,
llegada de mercadería, ventas mensuales, tarifas y umbrales, y todo se recalcula al instante.
Los cambios se guardan en `optimat_datos.json` (se puede volver a los datos de ejemplo desde el menú).

## Archivos

- `datos.py`: datos de ejemplo (productos, clientes, pedidos, entregas, tarifas, stock en bodega, ventas de 6 meses en un arreglo de 3 dimensiones y umbrales del semáforo).
- `calculos.py`: funciones matemáticas.
- `graficos.py`: gráfico del semáforo de stock con Matplotlib.
- `main.py`: menú interactivo; imprime el reporte, registra movimientos y guarda el gráfico en `alertas.png`.
- `test_calculos.py`: pruebas con un caso pequeño calculado a mano.
- `docs/`: tablas de la Etapa 2 en PDF y Word, y la presentación de la Etapa 3.

## Instalación y ejecución

```bash
pip install -r requirements.txt
python main.py            # menú interactivo
python main.py --reporte  # solo el reporte, sin menú
```

Importante: ejecutar en una **terminal** (en VS Code: botón ▶ "Run Python File" o `python main.py` en la terminal integrada).
Si usa la extensión *Code Runner*, el panel **Output** no permite escribir; active `code-runner.runInTerminal`.

Para correr las pruebas (requiere `pytest`):

```bash
pip install pytest
python -m pytest
```

## Conceptos matemáticos

| Función | Concepto | Qué hace |
|---|---|---|
| `calcular_reposicion` | Resta de matrices | R = Pedidos − Entregado (filas = productos, columnas = clientes) |
| `calcular_costos` | Producto matriz × vector | Costos = R · t (t = tarifa de flete por cliente); el total es la suma de las componentes |
| `verificar_despacho` | Sumatoria por fila | Σ de lo pendiente de cada producto en todos los clientes, comparado con el stock en bodega |
| `proyectar_demanda` | Sumatoria | Demanda = (1/n) · Σ ventas, calculada con un ciclo `for` acumulativo |
| `detectar_riesgo_quiebre` | Comparación | Si el stock en bodega < demanda proyectada, hay riesgo de quiebre |
| `resumir_ventas` | Arreglo multidimensional y sumatoria por eje | V tiene 3 índices (producto, cliente, mes); Σ sobre los clientes da la matriz productos × meses y Σ sobre los meses da la matriz productos × clientes |
| `calcular_cumplimiento` | División y porcentaje | Cumplimiento = Bodega / Pendiente × 100 |
| `clasificar_alertas` | Desigualdades | Verde si cumplimiento ≥ 150 %, amarillo si 100 % ≤ cumplimiento < 150 %, rojo si < 100 % (no alcanza) |
| `calcular_pedido_sugerido` | Operaciones con vectores y máximo | Comprar = máx(0, Pendiente + Demanda − Bodega), redondeado hacia arriba |
