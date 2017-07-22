# RPPGCT
Raspberry Pi Python GPIO Control Tools

## Descripción
Colección de utilidades varias para el control GPIO en Python

## Contenido
- **cpu.py**: Sistema indicador led de la carga de CPU en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma".
- **domotica_cliente.py**: Cliente del sistema gestor de domótica.
- **domotica_servidor.py**: Servidor del sistema gestor de domótica.
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
- 0.1.6: Añadida la sección de "Agradecimientos y otros créditos" en este documento y en los archivos correspondientes.
		 Añadido el instalador.
		 Acabados los scripts para init.d.
- 0.1.7: Añadidas cabeceras en **boton.py**, **cpu.py**, **internet.py**, **pid.py**, **reiniciar_router.py** y **temperaturas.py**.
		 Eliminada funcionalidad no necesaria en **reiniciar_router.py**.
		 Arreglo de bugs menores.
- 0.1.8: Añadido el script actualizador.
- 0.2.0: Configuración exportada a un único archivo.
		 Añadido un sistema de comprobación para alertar de una mala configuración.
		 Actualizados **actualizador.sh**, **instalador.sh** y **desinstalador.sh**.
		 Eliminado import innecesario en **internet.py**.
		 Editado **.gitignore** para que no suba el archivo **config.py**.
- 0.2.1: Arreglo de bug en los scripts de init.
- 0.2.2: Arreglo de bug en **temperaturas.py**.
- 0.2.3: Arreglos menores.
		 Cambio de editor, lo que puede provocar algún desajuste con las tabulaciones o similar.
		 Comienzo del proceso de hacer el código independiente del sistema operativ, ya que así algunas cosas podré probarlas con mayor rapidez.
- 0.2.4: Movido todo el código común a **comun.py**.
		 Arreglados fallos varios.
		 Rediseñado el bucle de **temperaturas.py**.
		 Añadida comprobación de superusuario en los scripts de **init**.
		 Añadido **indice_gpio.py**.
- 0.3.0: Actualización de la configuración de **config.py** para permitir puertos GPIO tanto de entrada, como de salida.
		 Actualizados **boton.py**, **comun.py**, **cpu.py**, **reiniciar_router.py** y **temperaturas.py** para adecuarse al nuevo **pid.py** para adecuarse a la nueva configuración.
		 Homogeneizado de este documento.
		 Implementación inicial de **domotica.py** a partir de **boton.py**.
- 0.3.1: Arreglo de fallos en **instalador.sh**, **actualizador.sh** y **desinstador.sh**.
- 0.3.2: Arreglo de fallos varios y limpieza de código en **actualizador.sh**.
- 0.3.3: Arreglo de bug en **reiniciar_router.py**.
		 Añadido **domotica.py** en **actualizador.sh**.
		 Limpieza de código en **instalador.sh**, **actualizador.sh** y **desinstador.sh**.
- 0.4.0: Renombrado de **domotica.py** a **domotica_servidor.py**.
		 Editado **config.py.sample** para adecuarse al cambio de nombre.
		 Añadidas comprobaciones a **comun.py** para no hacer nada si ciertas variables no existen.
		 Documentación de **comun.py**.
		 Modificado **pid.py** para ser compatible con Windows.
		 Pasado **pid.py** a estilo orientado a objetos.
		 Actualizados **comun.py**, **cpu.py**, **domotica_servidor.py**, **reiniciar_router.py** y **temperaturas.py** para adecuarse al nuevo **pid.py**.
		 Actualizado **config.py.sample** con los parámetros correspondientes a las novedades.
		 Homogeneizado de este documento.
		 Implementación inicial de **domotica_cliente.py**.
		 Renombrado **temperaturas.py** a **temperatura.py** por convención de nombres.
		 Actualizados **actualizador.sh**, **instalador.sh** y **desinstalador.sh** para adecuarse al cambio de nombre.
		 

## Agradecimientos y otros créditos
* A la [documentación oficial de Python](https://docs.python.org/3/), por motivos evidentes.
* A *linuxitux*, por [su script *netisup.py*](https://www.linuxito.com/programacion/635-netisup-py-script-python-para-verificar-el-estado-de-la-red), el cual he utilizado (adaptado) en mi **internet.py**
* A *alex*, por [la documentación en la web *raspi.tv*](http://raspi.tv/2013/rpi-gpio-basics-6-using-inputs-and-outputs-together-with-rpi-gpio-pull-ups-and-pull-downs), la cual me ha sido muy útil para mi **domotica_servidor.py**
* A *Alberto Vela*, por [el minitutorial de sockets en la web *developeando.net*](http://developeando.net/sockets-python/)

## Por hacer (*TODO*)
* ¡Mucho más!
