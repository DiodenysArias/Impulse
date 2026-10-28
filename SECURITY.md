# Seguridad

El límite de esta edición es la simulación en memoria. No existen destinos configurables, transporte de red, descubrimiento, credenciales, captura de paquetes ni extensiones dinámicas. Un aviso de uso responsable por sí solo no es una barrera técnica: por eso se retira el código anterior completo.

Los límites se validan tanto en la interfaz como en la API del modelo. Las pruebas verifican contabilidad, capacidad, rechazo de opciones heredadas, importaciones permitidas y ejecución con sockets y resolución DNS bloqueados. Estas comprobaciones ayudan a detectar regresiones; no son un aislamiento del sistema operativo ni garantizan la seguridad de código modificado.

Una contribución que introduzca conexiones, procesos externos o dependencias requiere una revisión nueva del diseño antes de integrarse. No se aceptan emisores de tráfico abusivo, listas de servicios reales, generación de mensajes masivos ni interruptores de compatibilidad con el proyecto anterior.

Para comunicar un problema, use un canal privado verificado del mantenedor o el mecanismo privado de GitHub si está habilitado. No publique credenciales, datos personales ni una demostración contra servicios reales. No se presupone que exista un canal privado configurado. Los fallos ordinarios del modelo pueden documentarse con un escenario sintético reproducible.

La retirada del árbol actual no elimina versiones históricas, copias, ramas o forks. La revisión de esta conversión no constituye una auditoría completa del historial ni de equipos donde se hubiera ejecutado el software anterior. Si se utilizó el antiguo guardado de correo, revise por separado las credenciales y los archivos locales de ese entorno; no los copie al laboratorio nuevo.
