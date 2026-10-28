# Prácticas guiadas

Ejecute cada escenario con 20 ticks. Antes de mirar la salida, prediga qué ocurrirá si llegan más elementos de los que pueden atenderse. No necesita conectarse a ningún equipo.

```sh
python -m impulse_lab --scenario baseline --ticks 20
python -m impulse_lab --scenario congestion --ticks 20
python -m impulse_lab --scenario rate-limit --ticks 20
```

| Métrica | baseline | congestion | rate-limit |
| --- | ---: | ---: | ---: |
| offered | 40 | 120 | 120 |
| completed | 40 | 60 | 60 |
| rate_limited | 0 | 0 | 60 |
| queue_dropped | 0 | 51 | 0 |
| remaining | 0 | 9 | 0 |
| peak_queue_depth | 2 | 12 | 3 |
| mean_wait_ticks | 0 | 2.55 | 0 |

1. Compruebe la identidad de contabilidad del README para cada ejecución.
2. Active `--events` y localice el primer descarte por cola llena. Explique por qué el máximo antes del servicio puede ser 12 mientras quedan 9 después.
3. Compare el rechazo temprano con los descartes de cola. Explique por qué el trabajo completado no aumenta.
4. Repita con 1 y 100 ticks y observe el efecto del trabajo pendiente sobre la interpretación de los resultados.
5. Explique por qué un tiempo lógico de espera no permite estimar latencia de Internet ni resistencia de un servidor.

La entrega sugerida es una tabla de resultados y una explicación propia. No incluya información personal, objetivos reales ni capturas de servicios externos.
