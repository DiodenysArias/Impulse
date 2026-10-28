# Revisión y conversión defensiva

Base revisada: `DiodenysArias/Impulse`, rama `master`, commit `592a91b16a40e912655199be51f10ae4f76287aa`. Se inspeccionaron el árbol completo, README, requisitos y archivos Python. No se ejecutó el código heredado ni se instalaron sus dependencias. No había pull requests abiertos al consultar el repositorio. Las listas de datos se identificaron por su presencia y por el código que las consume; no se validaron sus entradas ni se contactó a los servicios.

## Inventario de retirada

| Componente | Hallazgo y decisión |
| --- | --- |
| `impulse.py` | CLI de objetivo, método, duración e hilos que invoca `AttackMethod`. Eliminar; la nueva entrada es `python -m impulse_lab`. |
| `tools/method.py` | Importación dinámica, temporizador y repetición mediante hilos. Eliminar por completo. |
| `tools/L4/` | Emisores, suplantación y mecanismos de reflexión; incluye `syn.py`, `udp.py`, `ntp.py`, `memcached.py`, `pod.py`, `icmp.py`. Eliminar todo el directorio. |
| `tools/L4/*_servers.txt` | Listas de servidores consumidas por los emisores. Eliminar, sin copiarlas a fixtures ni anexos. |
| `tools/L7/` | Solicitudes HTTP y mantenimiento de conexiones; referers y user agents asociados. Eliminar código y datos. |
| `tools/SMS/` | Solicitudes a servicios externos, catálogo de servicios, proxy y generación de datos. Eliminar código y todos los JSON. |
| `tools/EMAIL/` | Envío SMTP, solicitud de credenciales y guardado local. Eliminar; no migrar archivos de credenciales locales. |
| `tools/addons/twilight/` | Transformaciones reversibles utilizadas para credenciales. Retirar con el flujo de correo; no reutilizar como seguridad. |
| `tools/ipTools.py` | Resolución de destinos, comprobaciones externas de Internet y protección, configuración de correo. Eliminar. |
| `tools/addons/winpcap.py` | Descarga y lanzamiento de instalador en Windows tras interacción. Eliminar. |
| Resto de `tools/` | Generadores, presentación, limpieza de terminal e informes del flujo antiguo. Eliminar, incluidos `randomData.py`, `crash.py`, `addons/clean.py`, `addons/logo.py`. |
| `requirements.txt` | Eliminar `requests`, `scapy`, `wget`, `argparse`, `colorama`, `humanfriendly`. La nueva implementación usa solo biblioteca estándar; `argparse` ya viene con Python. |
| README anterior | Sustituir branding, catálogo de ataques, ejemplo SMS, capturas remotas, instalación del toolkit y donaciones históricas por documentación educativa. |
| `LICENSE` | Conservar exactamente y reconocer la procedencia. |

No se aísla código ofensivo detrás de un indicador o una carpeta `legacy`: se elimina del árbol convertido. Solo se conserva este inventario descriptivo, sin cargas útiles, listas de objetivos ni instrucciones operativas.

## Diferencias entre nombres y comportamiento

`tools/L4/icmp.py` construía TCP con bandera SYN, aunque sus mensajes lo llamaban ICMP. `pod.py` creaba un payload grande, pero esta revisión no demuestra que produjera un «Ping of Death» efectivo. La clasificación se basa en el código observado, no en asumir que todas las promesas del README funcionaban.

## Alcance de la migración

La conversión añade el simulador, observabilidad JSONL, ejercicios, límites, política de contribución y pruebas. El nuevo árbol conserva únicamente la licencia del árbol anterior y sustituye su documentación. El historial de Git sigue conteniendo versiones anteriores; no se ha reescrito ni eliminado el repositorio original.

Para completar la presentación pública después de integrar la conversión, la descripción sugerida es: «Laboratorio defensivo de redes: simulación offline de colas, observabilidad y control de admisión». Los temas sugeridos son `networking`, `education`, `simulation`, `defensive-security` y `python`. Cambiar archivos no modifica automáticamente la descripción ni la relación de fork.

No se ha auditado todo el historial, ramas, releases o artefactos externos. Si el objetivo adicional fuera dejar de distribuir cualquier versión antigua, hará falta una decisión separada sobre publicación e historial; esta propuesta no promete borrar copias existentes. No se restaura el toolkit como mecanismo de reversión: ante un defecto se corrige el modelo o se retira la edición defectuosa.
