# RPPGCT
Raspberry Pi Python GPIO Control Tools

## Descripción
Colección de utilidades varias para el control GPIO en Python

## Contenido
- **boton.py**: Sistema de respuesta a un evento en un determinado pin GPIO, como una pulsación de un botón. *Aún en pruebas*.
- **cpu.py**: Sistema indicador led de la carga de CPU en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma".
- **internet.py**: Módilo auxiliar para la comprobación de si hay o no Internet.
- **pid.py**: Módulo auxiliar para ciertas funciones de bloqueo y de PIDs.
- **reiniciar_router.py**: Sistema que comprueba si hay acceso a Internet. Si no, manda una señal en un puerto GPIO determinado. La idea es conectár un relé a este GPIO y al mismo la alimentación del sistema de acceso a Internet.
- **temperaturas.py**: Sistema indicador led de la temperatura del procesador en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma".

## Historial de versiones
- 0.1.0: Creación de los scripts **boton.py**, **cpu.py**, **internet.py**, **pid.py**, **reiniciar_router.py** y **temperaturas.py**.
- 0.1.1: Creación del scrpit de init.d **temperaturas.sh**, para darle a **temperaturas.py** la capacidad de autoarranque.
- 0.1.2: Arreglo de un bug menor en **temperaturas.py**.
- 0.1.3: Arreglo del mismo bug anterior en **cpu.py**.
- 0.1.4: Redacción de este documento.
- 0.1.5: Creación de la rama (*branch*) de *testing* y adición de el instalador de pruebas.

## Por hacer (*TODO*)
* Testear el instalador.
* Acabar de hacer el resto de scripts de init.d.
