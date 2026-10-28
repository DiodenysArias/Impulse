# Impulse Defensive Lab

Laboratorio educativo de redes y resiliencia que funciona completamente en memoria. Permite observar cómo una cola limitada y el control de admisión afectan al trabajo completado, los descartes y el tiempo de espera, sin generar tráfico de red.

Esta edición reemplaza las funcionalidades de denegación de servicio del proyecto histórico. No contiene un motor de ataques ni conserva compatibilidad con su interfaz anterior.

## Objetivos de aprendizaje

- Comprender la relación entre demanda, capacidad de servicio y congestión.
- Comparar una cola sin control de admisión con una política de limitación.
- Interpretar eventos estructurados, contadores y tiempos de espera.
- Diseñar experimentos reproducibles y explicar sus límites.

Los resultados son sintéticos. No representan una medición de ancho de banda, rendimiento TCP/IP, latencia real ni resistencia de un servicio ante ataques. El simulador no implementa protocolos de red.

## Inicio rápido

Requiere Python 3.11 o posterior. Desde la raíz de esta edición del proyecto:

```sh
python -m impulse_lab
python -m impulse_lab --scenario congestion --ticks 20 --events
python -m impulse_lab --scenario rate-limit --ticks 20
python -m unittest discover -s tests -v
```

En sistemas donde el ejecutable se llama `python3`, úselo en lugar de `python`. No se necesitan paquetes de terceros, instalación con pip, permisos de administrador, controladores de captura ni conexión a Internet.

## Escenarios

| Escenario | Llegadas por tick | Control de admisión | Qué observar |
| --- | ---: | --- | --- |
| `baseline` | 2 | Sin límite adicional | Capacidad suficiente, sin espera |
| `congestion` | 6 | Sin límite adicional | Acumulación y descartes al llenarse la cola |
| `rate-limit` | 6 | Admite como máximo 3 por tick | Rechazo temprano y menor espera |

Todos utilizan una cola de 12 elementos y atienden como máximo 3 elementos por tick. Se admiten llegadas antes de atender la cola. Un tick es un paso lógico, no un segundo. La ejecución termina después de 1 a 100 ticks, sin vaciar automáticamente el trabajo pendiente. El valor predeterminado es 20. No hay hilos ni bucles indefinidos.

## Observabilidad

La salida es JSON; `--events` añade un registro JSON por tick, seguido del resumen. Todos los registros llevan `synthetic: true`. Puede guardar la salida mediante la redirección normal de su terminal; no hay envío de telemetría.

| Campo | Significado |
| --- | --- |
| `offered` | Trabajo sintético presentado |
| `admitted` | Trabajo incorporado a la cola en ese tick |
| `rate_limited` | Trabajo rechazado por control de admisión |
| `queue_dropped` | Trabajo descartado por falta de espacio |
| `completed` | Trabajo atendido |
| `queue_depth` / `remaining` | Trabajo pendiente tras la atención / al finalizar |
| `peak_queue_depth` | Máximo antes de atender, durante toda la ejecución |
| `mean_wait_ticks` | Espera media del trabajo completado; excluye pendientes y rechazados |

El resumen cumple `offered = completed + rate_limited + queue_dropped + remaining`. El control de admisión no crea capacidad nueva: cambia dónde se rechaza el exceso de trabajo. Véanse los [ejercicios](docs/labs.md).

## Límites de seguridad y uso responsable

- Solo simulación local en memoria: no abre sockets, resuelve DNS ni contacta servicios.
- No acepta IP, URL, puerto, teléfono, correo, proxy, credenciales ni destinos externos.
- No envía mensajes, paquetes ni solicitudes HTTP; no incluye amplificación, suplantación ni inundaciones.
- No ofrece opciones para restaurar los modos antiguos ni cargar módulos de terceros.
- Use únicamente datos sintéticos. No introduzca credenciales ni datos de personas en ejemplos o registros.
- Las prácticas que involucren infraestructura real quedan fuera del alcance de esta edición, incluso cuando exista autorización.

La autorización no convierte una red compartida en un laboratorio aislado. Los criterios para una posible ampliación local están en [arquitectura y límites](docs/architecture.md); esa ampliación no está implementada. Consulte también [SECURITY.md](SECURITY.md).

## Estructura

```text
impulse_lab/
  __init__.py        Identidad del paquete
  __main__.py        Interfaz limitada y salida JSONL
  model.py           Modelo de colas determinista
tests/
  test_lab.py        Límites, contabilidad, interfaz y ausencia de red
docs/
  architecture.md   Diseño y criterios para futuras prácticas
  labs.md           Ejercicios y resultados esperados
  migration.md      Revisión y eliminación de componentes heredados
README.md
SECURITY.md
CONTRIBUTING.md
LICENSE
```

## Procedencia y licencia

Este repositorio deriva históricamente de Impulse, creado por LimerBoy. La conversión conserva el archivo LICENSE original (GNU GPL versión 3) y reconoce esa procedencia; sustituye el código ejecutable anterior por un modelo educativo nuevo. La relación de fork y los commits históricos no desaparecen al cambiar los archivos. Esta documentación se refiere exclusivamente al árbol convertido; no recomienda utilizar versiones históricas.
