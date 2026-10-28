# Contribuir

Mantenga los cambios pequeños, reproducibles y sin red. Se aceptan mejoras al modelo de colas, observabilidad sintética, explicaciones y pruebas. Documente las unidades, el orden de los eventos y los límites de cada nueva métrica.

Antes de proponer un cambio, ejecute `python -m unittest discover -s tests -v`. Añada pruebas que demuestren la propiedad nueva y sus casos límite. No eleve los topes para representar carga: modifique el modelo matemático, sin emitir tráfico.

No incorpore código antiguo, listas de destinos, secretos, instaladores descargados, integraciones de mensajería, módulos de transporte ni ejemplos operativos de ataques. Mantenga la licencia y la atribución de procedencia.
