# RPPGCT
Raspberry Pi Python GPIO Control Tools

## Descripción
Colección de utilidades varias para el control GPIO en Python

## Contenido
- **boton.py**: Sistema de respuesta a un evento en un determinado pin GPIO, como una pulsación de un botón. *Aún en pruebas*.
- **cpu.py**: Sistema indicador led de la carga de CPU en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma".
- **indice_gpio.py**: Sistema indicador de los puertos GPIO que quedan libres.
- **internet.py**: Módulo auxiliar para la comprobación de si hay o no Internet.
- **pid.py**: Módulo auxiliar para ciertas funciones de bloqueo y de PIDs.
- **reiniciar_router.py**: Sistema que comprueba si hay acceso a Internet. Si no, manda una señal en un puerto GPIO determinado. La idea es conectar un relé a este GPIO y al mismo la alimentación del sistema de acceso a Internet.
- **temperaturas.py**: Sistema indicador led de la temperatura del procesador en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma".

## Historial de versiones
- 0.1.0: Creación de los scripts **boton.py**, **cpu.py**, **internet.py**, **pid.py**, **reiniciar_router.py** y **temperaturas.py**.
- 0.1.1: Creación del scrpit de init.d **temperaturas.sh**, para darle a **temperaturas.py** la capacidad de autoarranque.
- 0.1.2: Arreglo de un bug menor en **temperaturas.py**.
- 0.1.3: Arreglo del mismo bug anterior en **cpu.py**.
- 0.1.4: Redacción de este documento.
- 0.1.5: Creación de la rama (*branch*) de *testing* y adición del instalador de pruebas.
- 0.1.6: Añadida la sección de "Agradecimientos y otros créditos" en este documento y en los archivos correspondientes. Añadido el instalador. Acabados los scripts para init.d.
- 0.1.7: Añadidas cabeceras en todos los archivos, eliminada funcionalidad no necesaria en **reiniciar_router.py** y arreglo de bugs menores.
- 0.1.8: Añadido el script actualizador.
- 0.2.0: Configuración exportada a un único archivo, añadido un sistema de comprobación para alertar de una mala configuración, actualizados instalador, actualizador y desinstalador, eliminado import innecesario en **internet.py** y editado **.gitignore** para que no suba el archivo **./Python/config.py**.
- 0.2.1: Arreglo de bug en los scripts de **./init/**.
- 0.2.2: Arreglo de bug en el script de **./Python/temperaturas.py**.
- 0.2.3: Arreglos menores, cambio de editor (lo que puede provocar algún desajuste) y comienzo del proceso de hacerlo independiente del sistema operativo (así algunas cosas podré probarlas con mayor rapidez)
- 0.2.4: Movido todo el código común a **comun.py**, arreglados fallos varios, rediseñado el bucle de **temperaturas.py**, añadida comprobación de superusuario en los scripts de **init** y añadido **indice_gpio.py**.

## Agradecimientos y otros créditos
* A *linuxitux*, por [su script *netisup.py*](https://www.linuxito.com/programacion/635-netisup-py-script-python-para-verificar-el-estado-de-la-red), el cual he utilizado (adaptado) en mi **internet.py**

## Por hacer (*TODO*)
* Añadir el control de GPIOs general: leds y relés.
