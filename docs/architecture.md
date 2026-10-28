# Arquitectura del laboratorio

## Implementación actual

La interfaz valida un escenario enumerado y entre 1 y 100 ticks. El modelo recibe esos valores, valida de nuevo los límites y procesa una cola acotada en memoria. Devuelve eventos y un resumen, que la interfaz serializa a JSON por la salida estándar. No existen conexiones entre equipos, contenedores ni servicios.

Los parámetros de demanda, capacidad y servicio están definidos en el código. La CLI no acepta tasas arbitrarias, duración de reloj, hilos, destinos ni archivos de configuración. El máximo actual es 600 llegadas sintéticas por ejecución y 100 eventos de tick. La cola nunca supera 12 elementos. No hay persistencia automática ni recopilación de información del equipo.

## Pruebas autorizadas en entornos locales

Las prácticas implementadas se realizan en el equipo del estudiante mediante el modelo sintético. La validación comprueba 300 combinaciones de escenario y duración lógica, reproducibilidad, invariantes de cola, opciones no permitidas y salida JSONL. No requiere privilegios ni acceso a una LAN.

## Ampliación posible, no implementada

Si un curso necesitara observar un intercambio real, debe diseñarse como un ejercicio independiente de cliente y servidor propios, con una única transacción pequeña y predeterminada. No se reutilizará ningún emisor antiguo. Antes de implementarlo se exigirán:

1. Alcance escrito: propietario, proceso de prueba, finalidad y criterio de parada.
2. Entorno desechable sin salida a Internet ni acceso a la LAN, con bloqueo de egreso aplicado por el sistema operativo. Un nombre de host local o una subred privada no bastan.
3. Servicio de prueba propio, sin destinos arbitrarios, proxies, redirecciones, DNS externo ni credenciales reales.
4. Presupuestos fijos de bytes, mensajes y tiempo; concurrencia mínima, cierre garantizado y parada ante errores.
5. Pruebas negativas de escape IPv4/IPv6, redirecciones, configuración de proxies, agotamiento de límites y limpieza de procesos.
6. Registros sintéticos o minimizados y pruebas de que no hay conexiones fuera del aislamiento.

No se incluye una implementación de esa ampliación ni se habilita un modo de pruebas de carga. La simulación actual sigue siendo suficiente para estudiar colas, admisión y observabilidad.
