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
- 0.1.0:
    - Creación de los scripts **boton.py**, **cpu.py**, **internet.py**, **pid.py**, **reiniciar_router.py** y **temperaturas.py**.
- 0.1.1:
    - Creación del scrpit de init.d **temperaturas.sh**, para darle a **temperaturas.py** la capacidad de autoarranque.
- 0.1.2:
    - Arreglo de un bug menor en **temperaturas.py**.
- 0.1.3:
    - Arreglo del mismo bug anterior en **cpu.py**.
- 0.1.4:
    - Redacción de **README.md**.
- 0.1.5:
    - Creación de la rama (*branch*) de *testing* y adición del instalador de pruebas.
- 0.1.6:
    - Añadida la sección de "Agradecimientos y otros créditos" en **README.md** y en los archivos correspondientes.
    - Añadido el instalador.
    - Acabados los scripts para init.d.
- 0.1.7:
    - Añadidas cabeceras en **boton.py**, **cpu.py**, **internet.py**, **pid.py**, **reiniciar_router.py** y **temperaturas.py**.
    - Eliminada funcionalidad no necesaria en **reiniciar_router.py**.
    - Arreglo de bugs menores.
- 0.1.8:
    - Añadido el script actualizador.
- 0.2.0:
    - Configuración exportada a un único archivo.
    - Añadido un sistema de comprobación al importar para alertar de una mala (o inexistente) configuración en **boton.py**, **cpu.py**, **internet.py**, **pid.py**, **reiniciar_router.py** y **temperaturas.py**.
    - Actualizados **actualizador.sh**, **desinstalador.sh** e **instalador.sh**.
    - Eliminado *import* innecesario en **internet.py**.
    - Editado **.gitignore** para que no suba el archivo **config.py**.
- 0.2.1:
    - Arreglo de bug en los scripts de init.
- 0.2.2:
    - Arreglo de bug en **temperaturas.py**.
- 0.2.3:
    - Arreglos menores.
    - Cambio de editor, lo que puede provocar algún desajuste con las tabulaciones o similar.
    - Comienzo del proceso de hacer el código independiente del sistema operativ, ya que así algunas cosas podré probarlas con mayor rapidez.
- 0.2.4:
    - Movido todo el código común a **comun.py**.
    - Arreglados fallos varios.
    - Rediseñado el bucle de **temperaturas.py**.
    - Añadida comprobación de superusuario en los scripts de **init**.
    - Añadido **indice_gpio.py**.
- 0.3.0:
    - Actualización de la configuración de **config.py** para permitir puertos GPIO tanto de entrada, como de salida.
    - Actualizados **boton.py**, **comun.py**, **cpu.py**, **reiniciar_router.py** y **temperaturas.py** para adecuarse al nuevo **pid.py** para adecuarse a la nueva configuración.
    - Homogeneizado de **README.md**.
    - Implementación inicial de **domotica.py** a partir de **boton.py**.
- 0.3.1:
    - Arreglo de fallos en **instalador.sh**, **actualizador.sh** y **desinstador.sh**.
- 0.3.2:
    - Arreglo de fallos varios y limpieza de código en **actualizador.sh**.
- 0.3.3:
    - Arreglo de bug en **reiniciar_router.py**.
    - Añadido **domotica.py** en **actualizador.sh**.
    - Limpieza de código en **instalador.sh**, **actualizador.sh** y **desinstador.sh**.
- 0.4.0:
    - Renombrado de **domotica.py** a **domotica_servidor.py**.
    - Editado **config.py.sample** para adecuarse al cambio de nombre.
    - Añadidas comprobaciones a **comun.py** para no hacer nada si ciertas variables no existen.
    - Documentación de **comun.py**.
    - Modificado **pid.py** para ser compatible con Windows.
    - Pasado **pid.py** a estilo orientado a objetos.
    - Actualizados **comun.py**, **cpu.py**, **domotica_servidor.py**, **reiniciar_router.py** y **temperaturas.py** para adecuarse al nuevo **pid.py**.
    - Actualizado **config.py.sample** con los parámetros correspondientes a las novedades.
    - Homogeneizado de **README.md**.
    - Implementación inicial de **domotica_cliente.py**.
    - Renombrado **temperaturas.py** a **temperatura.py** por convención de nombres.
    - Actualizados **actualizador.sh**, **desinstalador.sh** e **instalador.sh** para adecuarse al cambio de nombre.
    - Añadida sección de *F. A. Q.* en **README.md**.
- 0.4.1:
    - Arreglados fallos varios en **actualizador.sh**, **desinstalador.sh** e **instalador.sh**.
    - Renombrado **domotica.sh** a **domotica_servidor.sh**.
    - Renombrado **temperaturas.sh** a **temperatura.sh**.
    - Homogeneizado de **README.md**.
- 0.4.2:
    - Arreglado fallo al lanzar hijos en **domotica_servidor.py**.
- 0.4.3:
    - Arreglado fallo en la descripción de **pid.py**
    - Arreglado fallo en la comprobación de desconexión de **domotica_servidor.py**
- 0.4.4:
    - Arreglado fallo en la sangría de algunas línas de código en **domotica_servidor.py**
- 0.4.5:
    - Arreglado fallo de versiones en los commits y en **README.md**.
- 0.4.6:
    - Modificado el procedimiento de arranque en **comun.py**, **cpu.py**, **domotica_cliente.py**, **domotica_servidor.py**, **reiniciar_router.py** y **temperaturas.py**.
    - Reajustado el código de **indice_gpio.py** para hacerlo más legible.
    - Implementado comando *estado* en **domotica_cliente.py** y **domotica_servidor.py**.
    - Actualizado un fallo en **actualizador.sh**, **desinstalador.sh** e **instalador.sh**.
    - Eliminado *import* innecesario en **domotica_servidor.py**.
    - Arreglo en la documentación de **comun.py**.
    - Añadidos algunos servidores más en la clase *internet_config* de **config.py.sample**.
- 0.5.0:
    - Arreglado fallo en la inicialización de los puertos GPIO de salida (sólo en el caso de ser puertos activos a bajo nivel, como podría ser el caso de un relé) en **comun.py**.
    - Añadido nuevos agradecimientos y reordenación de dicha sección en **README.md**.
    - Arreglo de fallos menores en la documentación de **domotica_servidor.py**. ¡Maldito copia-pega!
    - Cambio en el modo de procesamiento de los hijos en **domotica_servidor.py**. Ahora debería ser más eficiente.
    - Movida la configuración de *PAUSA* de la clase *domotica_cliente_config* a la clase *domotica_servidor_config*, ya que sólo hace falta en el servidor y no en ambos en **config.py.sample**.
    - Arreglado fallo en un *import* de **indice_gpio.py**.
    - Añadido un sistema de comprobación al importar para alertar de la no instalación del paquete *psutil* en **cpu.py**.
    - Clarificado parte del texto del *Historial de versiones* en **README.md**.
    - Clarificado parte del texto de **actualizador.sh** e **instalador.sh**.
    - Reajustado el nombre de algunas variables en **domotica_cliente.py**.
    - Renombrado **config.py.sample** a **config_sample.py**.
    - Reajustada la "constante" *PAUSA* de la clase *domotica_servidor_config* en **config_sample.py**.
    - Añadida la configuración necesaria para la depuración remota en **config.sample.py**.
    - Configurado **domotica_servidor.py** para que lea la configuración de depuración remota.
    - Actualizado el modo de encender los leds de **temperaturas.py**. Ahora puede soportar cualquier color.
    - Actualizada la configuración correspondiente en **config.py.sample**.
    - Mejorada la documentación de **config_sample.py**.
- 0.5.1:
    - Arreglado fallo en las variables de depuración en **temperatura.py**.
    - Convertido (de nuevo y espero que no vuelva a fallar) el retorno de línea de modo Windows a Linux en **cpu.py**.
- 0.5.2:
    - Modificado el tiempo de pausa de la clase *domotica_servidor_config* en **config_sample.py** para reducir la tasa de fallo. Sigue sin ser perfecto, pero a la espera de que arreglen [este error](https://sourceforge.net/p/raspberry-gpio-python/tickets/103/), es lo mejor que puedo hacer.
- 0.5.3:
    - Arreglado fallo en **desinstalador.sh**.
- 0.5.4:
    - Arreglo estético en **config_sample.py**.
    - Eliminados *imports* no necesarios en **domotica_cliente.py**
    - Arreglada sangría de *imports* en **domotica_cliente.py**, **indice_gpio.py**, **internet.py**, **reiniciar_router.py** y **temperatura.py**.
    - Implementado el comando de ayuda en **domotica_cliente.py**.
- 0.6.0:
	- Modificado **reiniciar_router.py** para que no actúe de manera independiente, sino a través de **domotica_servidor.py**.
	- Taspasadas clases que ahora son comunes a varios scripts de **domotica_cliente.py** a **comun.py**.
	- Modificado **domotica_cliente.py** para que la clase principal herede de la clase principal de **comun.py**.
	- Arreglado fallo en la función *estado* en **comun.py**.
	- Reajustadas configuraciones en arreglo a los cambios anteriores en **config_sample.py**.
	- Añadido el campo *"descripción"* en las "constantes" *GPIO* en **config_sample.py**.
	- Añadidos mecanismos para depuración remota en **domotica_cliente.py** y **reiniciar_router.py**. 

## Agradecimientos, fuentes consultadas y otros créditos
* A la [documentación oficial de Python](https://docs.python.org/3/), por motivos evidentes.
* A la [documentación del depurador remoto de PyDev](http://www.pydev.org/manual_adv_remote_debugger.html), porque la mayor parte del código se ejecuta en una Raspberry Pi y depurarlo en remoto en el PC es un lujo.
* A *croston*, por [la documentación sobre el módulo Python *raspberry-gpio-python* en formato *wiki*](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/), sin el cual este proyecto no habría sido posible
* A *alex*, por [la documentación en la web *raspi.tv*](http://raspi.tv/2013/rpi-gpio-basics-6-using-inputs-and-outputs-together-with-rpi-gpio-pull-ups-and-pull-downs), la cual me ha orientado en el tratamiento de los puertos GPIO de entrada en **domotica_servidor.py**.
* A *linuxitux*, por [el script *netisup.py*](https://www.linuxito.com/programacion/635-netisup-py-script-python-para-verificar-el-estado-de-la-red), el cual he utilizado (adaptado) en mi **internet.py**.
* A *Oscar Campos*, por [la entrada sobre hilos en la web *www.genbetadev.com*](https://www.genbetadev.com/python/multiprocesamiento-en-python-threads-a-fondo-introduccion), la cual me ha permitido llevar a cabo el multiprocesamiento en **domotica_servidor.py**.
* A *Amelia Zafra*, profesora de Redes en la [Universidad de Córdoba](http://www.uco.es/), por sus *prácticas de dicha asignatura en el curso 2015 - 2016*, las cuales me ayudaron bastante a organizar la lógica de **domotica_cliente.py** y **domotica_servidor.py**. 
* A *Alberto Vela*, por [el minitutorial de sockets en la web *developeando.net*](http://developeando.net/sockets-python/), el cual me ha permitido adaptar mis conocimientos en C / C++ en este campo en **domotica_cliente.py** y **domotica_servidor.py**.
* A *Barlan*, por [la entrada sobre sockets en Python 3.4 en el foro de *underc0de.org*](https://underc0de.org/foro/python/(mini-guia)-sockets-en-python-(3-4)/), la cual me ha permitido adaptar mis conocimientos en C / C++ en este campo en **domotica_cliente.py** y **domotica_servidor.py**.
* A *Pherkad*, por [la sección de "Control del acceso a los recursos. Bloqueos" en la web *python-para-impacientes.blogspot.com.es*](http://python-para-impacientes.blogspot.com.es/2016/12/threading-programacion-con-hilos-y-ii.html), la cual me ha evitado dolores de cabeza variados en **domotica_servidor.py**.

## Por hacer (*TODO*)
- [x] Crear una rama (*branch*) de *testing*.
- [x] Pasar **boton.py** a dicha rama.
- [x] Testear en dicha rama el instalador.
- [x] Acabar de hacer el resto de scripts de init.d.
- [x] Añadir el control de relés.
- [ ] ~~Añadir el configurador general.~~
- [ ] ~~Añadir el control de GPIOs general: leds y relés.~~
- [x] Implementar la domótica remota.
- [x] Cambiar el comando *conectar* para que sea un *conectar* y *listar* en **domotica_cliente.py** ~~y **domotica_servidor.py**~~.
- [x] Implementar comando *estado* para ver en qué estado se encuentra un puerto GPIO en **domotica_cliente.py** y **domotica_servidor.py**.
- [x] Implementar comandos por parámetros en **domotica_cliente.py**.
- [ ] Implementar comandos por archivo en **domotica_cliente.py**.
- [x] Integrar el control de relés en un archivo separado.
- [ ] Añadir control de versiones en la instalación.
- [ ] Hacer que **actualizador.sh** sea "inteligente" y actualice en función de la versión.
- [ ] ¡Mucho más!

## F. A. Q. (*Frequently Asked Questions*) o P. F. (Preguntas Frecuentes)
Desengañémosnos, nadie en su sano juicio preguntaría estas cosas, pero al menos nos sirve a los que las redactamos para aclarar algunas dudas que, creemos, el resto del mundo (mundial) podría tener.

:question: ¿Pero de verdad esto sirve para algo?

:point_right: A ver, a mí me sirve. ~~Y eso es lo que importa.~~ Y pienso que, si bien esto no es nada espectacular, quizá a alguien pueda también servirle o facilitarle el trabajo en algún momento, por lo cual he decidido compartirlo.

:question: No, ahora en serio, ¿de verdad sirve para algo?

:point_right: Bueno, todo esto no es nada *per se*. Pero si le añadimos:
- [Unos leds bonitos](https://www.amazon.es/dp/B00F4MGA0I/ref=cm_sw_r_cp_dp_T2_aTnDzb654D0KY)
- Más [leds bonitos](https://www.amazon.es/dp/B00X9IHNGE/ref=cm_sw_r_cp_dp_T2_QTnDzbEZ4K6H4)
- Varios [leds invisibles](https://www.amazon.es/dp/B00JGFF2SA/ref=cm_sw_r_cp_dp_T2_yTnDzbF49J0A7)
- Algunos [relés](https://www.amazon.es/dp/B009WJBZKO/ref=cm_sw_r_cp_dp_T2_wUnDzb875X91H)
- Mogollón de [placas para tenerlo todo bien conectado](https://www.amazon.es/dp/B00FXHXT80/ref=cm_sw_r_cp_dp_T2_wTnDzb1VJPVT8)
- Una [placa de pruebas](https://www.amazon.es/dp/B00PQC72ZS/ref=cm_sw_r_cp_dp_T2_vTnDzbX3WVERJ)
- Un manojo de [cables especiales para la dichosa placa de pruebas](https://www.amazon.es/dp/B00K67XXSI/ref=cm_sw_r_cp_dp_T2_7VnDzbPYM9NCW)
- Una tira de [cables](https://www.amazon.es/dp/B00DRAI8CC/ref=cm_sw_r_cp_dp_T2_lWnDzbFGEZA8T)
- Dos tiras más de [otros cables similares, pero que no son los mismos](https://www.amazon.es/dp/B00INWWVKY/ref=cm_sw_r_cp_dp_T2_rWnDzb1GD5QTP)
- Algo de [lógica combinacional](https://es.aliexpress.com/store/product/Free-Shipping-10PCS-SN74HC00-HC00-74HC00-74HC00N-DIP14-NAND-gate-IC/614856_670739753.html)
- Y un toque de [lógica secuencial](https://es.aliexpress.com/store/product/20Pcs-CD4060BE-CD4060-4060-Ripple-Carry-Binary-Counter-IC-DIP-16-pin-Low-Power/612195_32629607788.html)


:point_right: Con todo ese cóctel de cosas, podemos tener algo decente. Prometo subir alguna foto del montaje.

:exclamation: Exención de responsabilidad: Esta respuesta no es con fines publicitarios de **Amazon**, ni de ninguna otra web. Simplemente he listado la mayoría de los componentes que he comprado y dónde pueden ser encontrados.

:point_left: Las puertas NAND y los contadores son para propósitos de pruebas y experimentos. Aún no he realizado nada con ellos que esté relacionado con este proyecto, pero preveo hacerlo.


:question: Lo que tú digas, ¿pero cómo lo conecto o cómo se pone en marcha el hardware?

:point_right: La respuesta a esto es complicada, pero intentaré detallar qué hace cada módulo y cómo usarlo sin morir en el intento.
- **cpu.py**: Este sistema está pensado para medir el uso de la CPU de la Raspberry y encender una serie de leds en función de la carga. La cantidad de leds es variable. El último de los leds será el de "alarma", el cual será encendido solamente cuando la carga sea >= 100% cinco o más veces seguidas. 
- **domotica_cliente.py**: Este sistema es un simple script que admite varios comandos y se los manda al servidor correspondiente, una vez conectado a éste. No hace mucho más (aún).
- **domotica_servidor.py**: Este sistema es el más complejo hasta ahora. La idea es que interactúe con relés para llevar a cabo operaciones domóticas, tales como:
    - Control de una fuente de alimentación (para evitar su consumo cuando nada esté conectado a ella, básicamente), a al que, por ahora, irán conectados:
        - Control de los leds infrarrojos ya citados.
        - Control manual del ventilador al que antes hice referencia.
    - Control de un termo eléctrico (necesitaré un relé de más potencia que no he adquirido aún).
    - Control de varios elementos calefactores (necesitaré relés de más potencia que no he adquirido aún).
    - Control de una vávula de riego (necesitaré adquirirla).
- **indice_gpio.py**: Esta herramienta (no lo llamo sistema, ya que no está integrado con nada) sirve para enumerar los puertos GPIO que quedan libres; entiéndanse libres los que no han sido todavía utilizados en la configuración. 
- **internet.py**: Este módulo proporciona utilidades para saber si hay actualmente acceso a Internet.
- **pid.py**: Este módulo proporciona actualmente utilidades para evitar más de una instancia de ejecucución a los sistemas que lo requieran. En un futuro pienso ampliar sus funcionalidades. 
- **reiniciar_router.py**: Este sistema conmuta un relé que controla la alimentación de un módem - router 3G. Personlamente, me ha pasado el perder la conectividad a Internet de un sistema remoto y, por ello, no tener forma de acceder al mismo. La idea es que este sistema comprueba si hay internet (gracias a **internet.py**) y, de no haberlo, reinicie el módem - router... *por las bravas*, aunque en este caso, dicho aparato lo soporta sin problemas.   
- **temperaturas.py**: Este sistema está pensado para algo relacionado con **cpu.py**. Solamente que éste no enciende más de un led simultáneamente. Mi idea es conectar cada uno de los puertos GPIO a un led RGB y el cuarto a un led de alarma. Posteriormente, la alarma será también conectada a un relé que activará un ventilador (ya que si se activa la alarma es que la Raspberry Pi *tiene calor*). Aquí es donde seguramente necesitaré las puertas NAND.


:question: ¿Cuándo será lanzada la versión 1.0?

:point_right: Mis conocimientos del lenguaje Python aún son escasos; los sistemas ahora mismo están bastante aislados entre sí y deberían trabajar más coordinados; el instalador es un script que, si bien cumple su función, no me gusta, me parece cutre. Cuando todos estos problemas se solventen, el código esté más maduro, probado y estable y yo lo crea oportuno, consideraré que este proyecto pasa de ser una *guarrerida* a algo decente. Mientras, bueno, habrá que aprovechar lo que hay.

:question: ¿No has pensado en una interfaz web *to güapa* con *Bootstrap*, *jQuery*, una *API* y su correspondiente *junta de la trócola*? Seguro que así molaba el triple todo.

:point_right: He pensado en añadir *un algo* en Django, por aquello de que el código es Python, pero mis especialidades son C / C++ y PHP, así que no es algo a corto plazo. Si Python lo domino poco, Django aún menos. No quiero entrar en él sin tener más base de Python. Pienso que, mínimo, para enero - marzo de 2018 podré empezar en serio con ello. Quizá antes haga pruebas o implemente versiones preliminares, pero dudo que lo tenga en condiciones antes de la fecha que ya he dicho.

:question: ¿Por qué Python y no C / C++ o PHP, si tan bien (dices) que se te dan? ¿O por qué no <inserte aquí su lenguaje favorito / de moda>? 

:point_right: Porque aparte de un proyecto útil, quiero que sea un reto. Porque quiero aprender Python. Porque no me apetecía estar compilando cada vez que quisiera probar algo.

:point_right: ~~Porque no me ha dado la gana.~~ Analicemos algunos de los [lenguajes más populares](https://www.tiobe.com/tiobe-index/) y veamos:
- Java: Sí, hombre, claro... un lenguaje en que un simple *hola_mundo* requiere 16 GiB de RAM... en una Raspberry Pi Zero (la que yo tengo)... ¡Pfffff...JAJAJAJAJAJA! NOPE
- C / C++ / PHP: Respondido más arriba
- C# / VB .NET: ¿Se puede en Linux? No, es en serio...
- JavaScript (o, quizá, Node.js): Con todo el respeto a los desarrolladores de Node.js, programar en JavaScript no me parece serio.
- Delphi / Object Pascal: Lo veo demasiado complejo para un proyecto tan humilde.
- Go: ¿Esto no era una bebida energética?
- Perl: Sé que existe y que las expresiones regulares son una maravilla, pero no sé nada más de este lenguaje.
- Swift: Soy alérgico a las manzanas.
- Ruby: Es un juguete interesante.
- Ensamblador: Los programadores *senior* lo hacen en ensambaldor. Los programadores *de verdad*, en binario.
