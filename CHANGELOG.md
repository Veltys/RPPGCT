# Changelog
Todos los cambios importantes en este proyecto serán documentados en este documento.

Su formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Por hacer (*TODO*)]
- [ ] Implementar comandos por archivo en **domotica_cliente.py**.
- [ ] Hacer un cliente en Django, que permita una gestión más visual del sistema.
- [ ] Rehacer **dht11.py** de manera que pueda ser configurado para leer individualmente cada sensor.
- [ ] Pasar los scripts de inicio a *systemctl*.
- [ ] Cambiar al sistema de procesado de argumentos *argparse.ArgumentParser()* en **dht11.py**.
- [ ] ¡Mucho más!


## [Hecho (*DONE*)]
- [x] Crear una rama (*branch*) de *testing*.
- [x] Pasar **boton.py** a dicha rama.
- [x] Testear en dicha rama el instalador.
- [x] Acabar de hacer el resto de scripts de init.d.
- [x] Añadir el control de relés.
- [x] Implementar la domótica remota.
- [x] Cambiar el comando *conectar* para que sea un *conectar* y *listar* en **domotica_cliente.py** ~~y **domotica_servidor.py**~~.
- [x] Implementar comando *estado* para ver en qué estado se encuentra un puerto GPIO en **domotica_cliente.py** y **domotica_servidor.py**.
- [x] Implementar comandos por parámetros en **domotica_cliente.py**.
- [x] Integrar el control de relés en un archivo separado.


## [Cancelado]
- [ ] ~~Añadir el configurador general.~~
- [ ] ~~Añadir el control de GPIOs general: leds y relés.~~
- [ ] ~~Añadir control de versiones en la instalación.~~
- [ ] ~~Hacer que **actualizador.sh** sea "inteligente" y actualice en función de la versión.~~


## [0.11.0] - 2021-04-30
### Añadido
- Agradecimientos que faltaban en **README.md**
- Comentarios varios para suprimir errores del editor (Eclipse + Pydev) en **aviso_electricidad.py** e **indice_gpio.py**.
- Instalación de paquetes ampliable en **config.sh** e **instalador.sh**.
- Lectura de sondas DHT11 a través de un paquete en **dht11.py**.
- Posibilidad de añadir hosts por parámetros a **internet.py**.

### Arreglado
- Actualizado general del código en **internet.py**.
- Mejora en la inteligibilidad del código en **temperatura.py**.
- Cadenas heteogéneas migradas a [*cadenas-f*](https://realpython.com/python-f-strings/#f-strings-a-new-and-improved-way-to-format-strings-in-python) para mejorar la presentación del código en **aviso_electricidad.py**, **comun.py** y **dht11.py**.
- Optimizado del método *estado_conexion_lenguaje_natural* en **comun.py**.
- Optimizaciones varias en **cpu.py**, **domotica_cliente.py** y **temperatura.py**.
- Ordenado de *imports* en **aviso_electricidad.py**, **comun.py**, **correo_electronico.py**, **cpu.py**, **dht11.py**, **domotica_cliente.py**, **domotica_servidor.py**, **internet.py**, **internet.py**, **reiniciar_router.py** y **temperatura.py**.
- Renombrado **dht11.py** a **sonda_dht11.py**

### Eliminado
- Compatibilidad con Python 3.5 debido a las cadenas-f (requieren Python 3.6).
- Configuración no necesaria relativa a la sonda dht11 en **config.py** y **domotica_servidor.py**.
- Sistema antiguo de lectura de sondas DHT11 en **dht11.py**.

## [0.10.4] - 2021-04-14
### Arreglado
- Ruta al comando de medición de temperatura en **temperatura.sh**.


## [0.10.3] - 2019-12-19
### Añadido
- Soporte de requisitos de otros servicios en **cpu.sh**, **domotica_servidor.sh**, **reinicar_router.sh** y **temperatura.sh**.

### Arreglado
- Comando status sin necesidad de sudo en **cpu.sh**, **domotica_servidor.sh**, **reinicar_router.sh** y **temperatura.sh**.
- Comando de restart


## [0.10.2] - 2019-12-19
### Arreglado
- *temperaturas.py* ➡ *temperatura.py* en **README.md**.
- Lista de puertos GPIO libres en **indice_gpio.py**.


## [0.10.1] - 2019-11-25
### Arreglado
- Acceso al puerto GPIO en **dht11.py**.
- Devolución de resultado errónero en **dht11.py**.


## [0.10.0] - 2019-11-25
### Añadido
- Archivo separado para el historial de versiones en **CHANGELOG.md**.
- Agradecimiento por la plantilla para este archivo.
- Posibilidad de realizar más de una llamada por cada sensor de domótica en **config.py** y **domotica_servidor.py**.
- Últimos cambios del original en **dht11.py**.

### Arreglado
- Cambiado el comportamiento para que ahora sea posible que un botón o sonda dispare más de un relé o led en **config.py** y **domotica_servidor.py**.
- Fechas en el estándar ISO 8601 en **actualizador.sh**, **aviso_electricidad.py**, **CHANGELOG.md**, **comun.py**, **config.py**, **config.sh**, **correo_electronico.py**, **desinstalador.sh**, **cpu.py**, **cpu.sh**, **dht11.py**, **domotica_cliente.py**, **domotica_servidor.py**, **domotica_servidor.sh**, **indice_gpio.py**, **instalador.sh**, **internet.py**, **pid.py**, **reiniciar_router.py**, **reiniciar_router.sh**, **temperatura.py** y **temperatura.sh**.
- Mejoras en la calidad del código.
- Optimizaciones varias y de seguridad.

### Eliminado
- Secciones *Historial de versiones* y *Por hacer (*TODO*)* en **README.md**.


## [0.9.0] - 2019-06-25
### Añadido
- Acceso externo sencillo por pid en **pid.py**.
- Más controles de excepciones.
- Soporte para leds PWM.
- Soporte para relés en **temperatura.py**.

### Arreglado
- Cambiada la nomenclatura de los puertos GPIO para el reinicio en caso de desconexión con el fin de evitar confusiones en su parte correspondiente de **config.py** y **reiniciar_router.py**.
- Fallo de acceso a un índice incorrecto de una tupla en **domotica_servidor.py**.
- Fallo por el cual no se imprimía el comando *describir* en **domotica_cliente.py**.
- Fallo por el cual se normalizaba siempre la respuesta de un comando y no bajo petición en **comun.py** y **domotica_cliente.py**. 
- Homogeneizado (todavía más) de **README.md**.
- Mejoras en la calidad del código.
- Mejoras en la documentación.
- Optimizaciones varias.
- Proceso de actualización en **actualizador.sh**.


## [0.8.2] - 2018-07-01
### Arreglado
- Homogeneizado (aún más) de **README.md**.
- Independizado de código encargado de mandar correos electrónicos.


## [0.8.1] - 2018-07-01
### Añadido
- **aviso_electricidad.py** a la lista de scripts en **config.sh**.

### Arreglado
- Homogeneizado de **README.md**.


## [0.8.0] - 2018-07-01
### Añadido
- Posibilidad de invocar código al dispararse eventos en puertos GPIO en **domotica_servidor.py**.

### Eliminado
- Código innecesario en **reiniciar_router.py**.
- Posibilidad de conectar a un servidor que no sea el local en **comun.py** y adecuado el código a la nueva conexión en **config.py**, **domotica_cliente.py** y **reiniciar_router.py**.


## [0.7.2] - 2018-06-17
### Arreglado
- Mejoras en la calidad del código.


## [0.7.1] - 2018-05-03
### Añadido
- Otra licencia en la sección de *Otras licencias* en **README.md**.
- Varios parámetros para variar la salida en **dht11.py**.


## [0.7.0] - 2018-03-11
### Añadido
- Otra licencia en la sección de *Otras licencias* en **README.md**.
- Sistema de lectura de sondas de temperatura DHT11 en **dht11.py**.


## [0.6.2] - 2018-03-11
### Añadido
- Sección de *Otras licencias* en **README.md**.

### Arreglado
- Fallo en la sangría en **README.md**.

### Eliminado
- *Import* innecesario en **cpu.py**.


## [0.6.1] - 2017-12-31
### Arreglado
- Fallo en **cpu.py**, que podría provocar que no se ejecutase correctamente.
- Renombrado **config_sample.py** a **config.py** y actualizadas referencias.


## [0.6.0] - 2017-12-02
### Añadido
- Bloque para interceptar un posible fallo al intentar borrar un archivo de bloqueo inexistente en **pid.py**. Esto podía ocurrir al reinstalar el sistema, especialmente si la parada de un servicio implica tiempo de procesamiento adicional, como en **domotica_servidor.py**. En este caso, es posible que el archivo de bloqueo sea borrado antes de la completa detención del servicio y, por consiguiente, éste arrojaría un fallo.
- Campo *"descripción"* en las "constantes" *GPIO* en **config_sample.py**.
- Mecanismos para depuración remota en **domotica_cliente.py** y **reiniciar_router.py**.

### Arreglado
- **domotica_cliente.py** para que la clase principal herede de la clase principal de **comun.py**.
- Eliminaciones de archivos de bloqueo en **actualizador.sh** y **desinstalador.sh** silenciosas (> /dev/null), para evitar exceso de flood de fallos.
- Fallo en la función *estado* en **comun.py**.
- Protocolo de comunicación entre **domotica_servidor.py** y **domotica_cliente.py** para el primero pueda indicar al segundo la descripción de los puertos GPIO y un "saludo" para acordar la versión del protocolo a emplear.
- **reiniciar_router.py** para que no actúe de manera independiente, sino a través de **domotica_servidor.py**.
- **actualizador.sh**, **desinstalador.sh** e **instalador.sh** y añadido **config.sh** para ajustar más finamente los permisos a la hora de instalar / actualizar y agrupada toda la configuración común.
- Reajustadas configuraciones en arreglo a los cambios anteriores en **config_sample.py**.
- Renombrado de la sección *Contenido* a *Sistemas* en **README.md**.
- Taspasados métodos que ahora son comunes a varios scripts de **domotica_cliente.py** a **comun.py**.


## [0.5.4] - 2017-11-18
### Añadido
- Comando de ayuda en **domotica_cliente.py**.

### Arreglado
- Sangría de *imports* en **domotica_cliente.py**, **indice_gpio.py**, **internet.py**, **reiniciar_router.py** y **temperatura.py**.
- Estética de **config_sample.py**.

### Eliminado
- *Imports* no necesarios en **domotica_cliente.py**.


## [0.5.3] - 2017-10-03
### Arreglado
- Fallo en **desinstalador.sh**.


## [0.5.2] - 2017-08-23
### Arreglado
- Modificado el tiempo de pausa de la clase *domotica_servidor_config* en **config_sample.py** para reducir la tasa de fallo. Sigue sin ser perfecto, pero a la espera de que arreglen [este fallo](https://sourceforge.net/p/raspberry-gpio-python/tickets/103/), es lo mejor que puedo hacer.


## [0.5.1] - 2017-08-13
### Arreglado
- Convertido (de nuevo y espero que no vuelva a fallar) el retorno de línea de modo Windows a Linux en **cpu.py**.
- Fallo en las variables de depuración en **temperatura.py**.


## [0.5.0] - 2017-08-13
### Añadido
- Configuración necesaria en **domotica_servidor.py** para que lea la configuración de depuración remota.
- Nuevos agradecimientos y reordenación de dicha sección en **README.md**.
- Sistema de comprobación al importar para alertar de la no instalación del paquete *psutil* en **cpu.py**.

### Arreglado
- Clarificado parte del texto de **actualizador.sh** e **instalador.sh**.
- Clarificado parte del texto del *Historial de versiones* en **README.md**.
- Configuración correspondiente en **config.py.sample**.
- Fallo en la inicialización de los puertos GPIO de salida (sólo en el caso de ser puertos activos a bajo nivel, como podría ser el caso de un relé) en **comun.py**.
- Fallo en un *import* de **indice_gpio.py**.
- Fallos menores en la documentación de **domotica_servidor.py**. ¡Maldito copia-pega!
- Modo de encender los leds de **temperaturas.py**. Ahora puede soportar cualquier color.
- Modo de procesamiento de los hijos en **domotica_servidor.py**. Ahora debería ser más eficiente.
- Mejorada la documentación de **config_sample.py**.
- Movida la configuración de *PAUSA* de la clase *domotica_cliente_config* a la clase *domotica_servidor_config*, ya que sólo hace falta en el servidor y no en ambos en **config.py.sample**.
- Reajustada la "constante" *PAUSA* de la clase *domotica_servidor_config* en **config_sample.py**.
- Reajustado el nombre de algunas variables en **domotica_cliente.py**.
- Renombrado **config.py.sample** a **config_sample.py**.


## [0.4.6] - 2017-08-10
### Añadido
- Algunos servidores más en la clase *internet_config* de **config.py.sample**.
- Comando *estado* en **domotica_cliente.py** y **domotica_servidor.py**.
- Configuración necesaria para la depuración remota en **config.sample.py**.

### Arreglado
- Documentación de **comun.py**.
- Fallo en **actualizador.sh**, **desinstalador.sh** e **instalador.sh**.
- Modificado el procedimiento de arranque en **comun.py**, **cpu.py**, **domotica_cliente.py**, **domotica_servidor.py**, **reiniciar_router.py** y **temperaturas.py**.
- Reajustado el código de **indice_gpio.py** para hacerlo más legible.

### Eliminado
- *Import* innecesario en **domotica_servidor.py**.


## [0.4.5] - 2017-07-24
### Arreglado
- Fallo de versiones en los commits y en **README.md**.


## [0.4.4] - 2017-07-24
### Arreglado
- Fallo en la sangría de algunas línas de código en **domotica_servidor.py**


## [0.4.3] - 2017-07-24
### Arreglado
- Fallo en la comprobación de desconexión de **domotica_servidor.py**
- Fallo en la descripción de **pid.py**


## [0.4.2] - 2017-07-24
### Arreglado
- Fallo al lanzar hijos en **domotica_servidor.py**.


## [0.4.1] - 2017-07-23
### Arreglado
- Fallos varios en **actualizador.sh**, **desinstalador.sh** e **instalador.sh**.
- Homogeneizado de **README.md**.
- Renombrado **domotica.sh** a **domotica_servidor.sh**.
- Renombrado **temperaturas.sh** a **temperatura.sh**.


## [0.4.0] - 2017-07-23
### Añadido
- Comprobaciones a **comun.py** para no hacer nada si ciertas variables no existen.
- Sección de *F. A. Q.* en **README.md**.
- Implementación inicial de **domotica_cliente.py**.

### Arreglado
- **actualizador.sh**, **desinstalador.sh** e **instalador.sh** para adecuarse al cambio de nombre.
- **config.py.sample** con los parámetros correspondientes a las novedades.
- **comun.py**, **cpu.py**, **domotica_servidor.py**, **reiniciar_router.py** y **temperaturas.py** para adecuarse al nuevo **pid.py**.
- Documentación de **comun.py**.
- **config.py.sample** para adecuarse al cambio de nombre.
- Homogeneizado de **README.md**.
- **pid.py** ahora es compatible con Windows.
- **pid.py** ahora es de estilo orientado a objetos.
- Renombrado de **domotica.py** a **domotica_servidor.py**.
- Renombrado **temperaturas.py** a **temperatura.py** por convención de nombres.


## [0.3.3] - 2017-07-10
### Añadido
- **domotica.py** en **actualizador.sh**.

### Arreglado
- Fallo en **reiniciar_router.py**.
- Limpieza de código en **instalador.sh**, **actualizador.sh** y **desinstador.sh**.

## [0.3.2] - 2017-07-07
### Arreglado
- Fallos varios
- Limpieza de código en **actualizador.sh**.


## [0.3.1] - 2017-07-07
### Arreglado
- Fallos en **instalador.sh**, **actualizador.sh** y **desinstador.sh**.


## [0.3.0] - 2017-07-07
### Añadido
- **boton.py**, **comun.py**, **cpu.py**, **reiniciar_router.py** y **temperaturas.py** para adecuarse al nuevo **pid.py** para adecuarse a la nueva configuración.
- Configuración de **config.py** para permitir puertos GPIO tanto de entrada, como de salida.
- Implementación inicial de **domotica.py** a partir de **boton.py**.

### Arreglado
- Homogeneizado de **README.md**.


## [0.2.4] - 2017-07-05
### Añadido
- Comprobación de superusuario en los scripts de **init**.
- **indice_gpio.py**.

### Arreglado
- Fallos varios.
- Movido todo el código común a **comun.py**.
- Rediseñado el bucle de **temperaturas.py**.


## [0.2.3] - 2017-07-02
### Arreglado
- Arreglos menores.
- Cambio de editor, lo que puede provocar algún desajuste con las tabulaciones o similar.
- Comenzado proceso para hacer el código independiente del sistema operativo.


## [0.2.2] - 2017-07-02
### Arreglado
- Fallo en **temperaturas.py**.


## [0.2.1] - 2017-07-01
### Arreglado
- Fallo en los scripts de init.


## [0.2.0] - 2017-07-01
### Añadido
- Exportada configuración a un único archivo.
- Sistema de comprobación al importar para alertar de una mala (o inexistente) configuración en **boton.py**, **cpu.py**, **internet.py**, **pid.py**, **reiniciar_router.py** y **temperaturas.py**.

### Actualizado
- **actualizador.sh**, **desinstalador.sh** e **instalador.sh**.

### Arreglado
- **.gitignore** para que no suba el archivo **config.py**.

### Eliminado
- *import* innecesario en **internet.py**.


## [0.1.8] - 2017-07-01
### Añadido
- Script actualizador.


## [0.1.7] - 2017-06-29
### Añadido
- Cabeceras en **boton.py**, **cpu.py**, **internet.py**, **pid.py**, **reiniciar_router.py** y **temperaturas.py**.

### Arreglado
- Fallos menores.

### Eliminado
- Funcionalidad no necesaria en **reiniciar_router.py**.


## [0.1.6] - 2017-06-29
### Añadido
- Instalador.
- Scripts para init.d.
- Sección de "Agradecimientos y otros créditos" en **README.md** y en los archivos correspondientes.


## [0.1.5] - 2017-06-28
### Añadido
- Instalador de pruebas.
- *Rama* (*branch*) de *testing*.


## [0.1.4] - 2017-06-28
### Añadido
- **README.md**.


## [0.1.3] - 2017-06-28
### Arreglado
- Arreglo del mismo fallo anterior en **cpu.py**.


## [0.1.2] - 2017-06-28
### Arreglado
- Fallo menor en **temperaturas.py**.


## [0.1.1] - 2017-06-28
### Añadido
- Scrpit de init.d **temperaturas.sh**, para darle a **temperaturas.py** la capacidad de autoarranque.


## [0.1.0] - 2017-06-28
### Añadido
- Scripts **boton.py**, **cpu.py**, **internet.py**, **pid.py**, **reiniciar_router.py** y **temperaturas.py**.
