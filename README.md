﻿# RPPGCT
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/78a8d6604cad48329f0b6800b91b36b1)](https://www.codacy.com/app/veltys/RPPGCT?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Veltys/RPPGCT&amp;utm_campaign=Badge_Grade)
[![GitHub release](https://img.shields.io/github/release/Veltys/RPPGCT.svg)](https://GitHub.com/Veltys/RPPGCT/releases/)
[![GitHub commits](https://badgen.net/github/commits/Veltys/RPPGCT)](https://GitHub.com/Veltys/RPPGCT/commit/)
[![GitHub latest commit](https://badgen.net/github/last-commit/Veltys/RPPGCT)](https://GitHub.com/Veltys/RPPGCT/commit/)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/Veltys/RPPGCT/blob/master/LICENSE)
[![Changelog](https://img.shields.io/badge/Changelog%3F-here-green.svg)](https://github.com/Veltys/RPPGCT/blob/master/CHANGELOG.md)

Raspberry Pi Python GPIO Control Tools


## Descripción
Colección de utilidades varias para el control GPIO en Python


## Sistemas
- **aviso_electricidad.py**: Sistema avisador de corte de luz.
- **correo_electronico.py**: Módulo auxiliar de envío de correos electrónicos.
- **cpu.py**: Sistema indicador led de la carga de CPU en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma".
- **domotica_cliente.py**: Cliente del sistema gestor de domótica.
- **domotica_servidor.py**: Servidor del sistema gestor de domótica.
- **indice_gpio.py**: Sistema indicador de los puertos GPIO que quedan libres.
- **internet.py**: Módulo auxiliar de comprobación de conectividad a Internet.
- **pid.py**: Módulo auxiliar para ciertas funciones de bloqueo y de PIDs.
- **reiniciar_router.py**: Sistema que comprueba si hay acceso a Internet. Si no, manda una señal en un puerto GPIO determinado. La idea es conectar un relé a este GPIO y al mismo la alimentación del sistema de acceso a Internet.
- **sonda_dht11.py**: Sistema de lectura de sondas de temperatura DHT11.
- **temperatura.py**: Sistema indicador led de la temperatura del procesador en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma".


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
* A *billiejoex* y *giampaolo.rodola*, por [el paquete psutil](https://pypi.org/project/psutil/), la cuál he utilizado en mi **cpu.py**.
* A *dragoneena12* y *szazo*, por [el paquete dht11](https://pypi.org/project/dht11/), la cuál he utilizado en mi **dht11.py**.
* A *Olivier Lacan*, por [su excelente plantilla para archivos CHANGELOG.md](https://keepachangelog.com/es-ES/0.3.0/), la cuál he utilizado (adaptada) en mi **CHANGELOG.MD**.


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
    - ~~Control de una vávula de riego (necesitaré adquirirla).~~
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


## Otras licencias
### Attribution-ShareAlike 4.0 International (**internet.py**)

Creative Commons Corporation (“Creative Commons”) is not a law firm and does not provide legal services or legal advice. Distribution of Creative Commons public licenses does not create a lawyer-client or other relationship. Creative Commons makes its licenses and related information available on an “as-is” basis. Creative Commons gives no warranties regarding its licenses, any material licensed under their terms and conditions, or any related information. Creative Commons disclaims all liability for damages resulting from their use to the fullest extent possible.

#### Using Creative Commons Public Licenses

Creative Commons public licenses provide a standard set of terms and conditions that creators and other rights holders may use to share original works of authorship and other material subject to copyright and certain other rights specified in the public license below. The following considerations are for informational purposes only, are not exhaustive, and do not form part of our licenses.

* __Considerations for licensors:__ Our public licenses are intended for use by those authorized to give the public permission to use material in ways otherwise restricted by copyright and certain other rights. Our licenses are irrevocable. Licensors should read and understand the terms and conditions of the license they choose before applying it. Licensors should also secure all rights necessary before applying our licenses so that the public can reuse the material as expected. Licensors should clearly mark any material not subject to the license. This includes other CC-licensed material, or material used under an exception or limitation to copyright. [More considerations for licensors](http://wiki.creativecommons.org/Considerations_for_licensors_and_licensees#Considerations_for_licensors).

* __Considerations for the public:__ By using one of our public licenses, a licensor grants the public permission to use the licensed material under specified terms and conditions. If the licensor’s permission is not necessary for any reason–for example, because of any applicable exception or limitation to copyright–then that use is not regulated by the license. Our licenses grant only permissions under copyright and certain other rights that a licensor has authority to grant. Use of the licensed material may still be restricted for other reasons, including because others have copyright or other rights in the material. A licensor may make special requests, such as asking that all changes be marked or described. Although not required by our licenses, you are encouraged to respect those requests where reasonable. [More considerations for the public](http://wiki.creativecommons.org/Considerations_for_licensors_and_licensees#Considerations_for_licensees).

#### Creative Commons Attribution-ShareAlike 4.0 International Public License

By exercising the Licensed Rights (defined below), You accept and agree to be bound by the terms and conditions of this Creative Commons Attribution-ShareAlike 4.0 International Public License ("Public License"). To the extent this Public License may be interpreted as a contract, You are granted the Licensed Rights in consideration of Your acceptance of these terms and conditions, and the Licensor grants You such rights in consideration of benefits the Licensor receives from making the Licensed Material available under these terms and conditions.

##### Section 1 – Definitions.

a. __Adapted Material__ means material subject to Copyright and Similar Rights that is derived from or based upon the Licensed Material and in which the Licensed Material is translated, altered, arranged, transformed, or otherwise modified in a manner requiring permission under the Copyright and Similar Rights held by the Licensor. For purposes of this Public License, where the Licensed Material is a musical work, performance, or sound recording, Adapted Material is always produced where the Licensed Material is synched in timed relation with a moving image.

b. __Adapter's License__ means the license You apply to Your Copyright and Similar Rights in Your contributions to Adapted Material in accordance with the terms and conditions of this Public License.

c. __BY-SA Compatible License__ means a license listed at [creativecommons.org/compatiblelicenses](http://creativecommons.org/compatiblelicenses), approved by Creative Commons as essentially the equivalent of this Public License.

d. __Copyright and Similar Rights__ means copyright and/or similar rights closely related to copyright including, without limitation, performance, broadcast, sound recording, and Sui Generis Database Rights, without regard to how the rights are labeled or categorized. For purposes of this Public License, the rights specified in Section 2(b)(1)-(2) are not Copyright and Similar Rights.

e. __Effective Technological Measures__ means those measures that, in the absence of proper authority, may not be circumvented under laws fulfilling obligations under Article 11 of the WIPO Copyright Treaty adopted on December 20, 1996, and/or similar international agreements.

f. __Exceptions and Limitations__ means fair use, fair dealing, and/or any other exception or limitation to Copyright and Similar Rights that applies to Your use of the Licensed Material.

g. __License Elements__ means the license attributes listed in the name of a Creative Commons Public License. The License Elements of this Public License are Attribution and ShareAlike.

h. __Licensed Material__ means the artistic or literary work, database, or other material to which the Licensor applied this Public License.

i. __Licensed Rights__ means the rights granted to You subject to the terms and conditions of this Public License, which are limited to all Copyright and Similar Rights that apply to Your use of the Licensed Material and that the Licensor has authority to license.

j. __Licensor__ means the individual(s) or entity(ies) granting rights under this Public License.

k. __Share__ means to provide material to the public by any means or process that requires permission under the Licensed Rights, such as reproduction, public display, public performance, distribution, dissemination, communication, or importation, and to make material available to the public including in ways that members of the public may access the material from a place and at a time individually chosen by them.

l. __Sui Generis Database Rights__ means rights other than copyright resulting from Directive 96/9/EC of the European Parliament and of the Council of 11 March 1996 on the legal protection of databases, as amended and/or succeeded, as well as other essentially equivalent rights anywhere in the world.

m. __You__ means the individual or entity exercising the Licensed Rights under this Public License. Your has a corresponding meaning.

##### Section 2 – Scope.

a. ___License grant.___

   1. Subject to the terms and conditions of this Public License, the Licensor hereby grants You a worldwide, royalty-free, non-sublicensable, non-exclusive, irrevocable license to exercise the Licensed Rights in the Licensed Material to:

       A. reproduce and Share the Licensed Material, in whole or in part; and

       B. produce, reproduce, and Share Adapted Material.

   2. __Exceptions and Limitations.__ For the avoidance of doubt, where Exceptions and Limitations apply to Your use, this Public License does not apply, and You do not need to comply with its terms and conditions.

   3. __Term.__ The term of this Public License is specified in Section 6(a).

   4. __Media and formats; technical modifications allowed.__ The Licensor authorizes You to exercise the Licensed Rights in all media and formats whether now known or hereafter created, and to make technical modifications necessary to do so. The Licensor waives and/or agrees not to assert any right or authority to forbid You from making technical modifications necessary to exercise the Licensed Rights, including technical modifications necessary to circumvent Effective Technological Measures. For purposes of this Public License, simply making modifications authorized by this Section 2(a)(4) never produces Adapted Material.

   5. __Downstream recipients.__

       A. __Offer from the Licensor – Licensed Material.__ Every recipient of the Licensed Material automatically receives an offer from the Licensor to exercise the Licensed Rights under the terms and conditions of this Public License.

       B. __Additional offer from the Licensor – Adapted Material. Every recipient of Adapted Material from You automatically receives an offer from the Licensor to exercise the Licensed Rights in the Adapted Material under the conditions of the Adapter’s License You apply.

       C. __No downstream restrictions.__ You may not offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, the Licensed Material if doing so restricts exercise of the Licensed Rights by any recipient of the Licensed Material.

   6. __No endorsement.__ Nothing in this Public License constitutes or may be construed as permission to assert or imply that You are, or that Your use of the Licensed Material is, connected with, or sponsored, endorsed, or granted official status by, the Licensor or others designated to receive attribution as provided in Section 3(a)(1)(A)(i).

b. ___Other rights.___

   1. Moral rights, such as the right of integrity, are not licensed under this Public License, nor are publicity, privacy, and/or other similar personality rights; however, to the extent possible, the Licensor waives and/or agrees not to assert any such rights held by the Licensor to the limited extent necessary to allow You to exercise the Licensed Rights, but not otherwise.

   2. Patent and trademark rights are not licensed under this Public License.

   3. To the extent possible, the Licensor waives any right to collect royalties from You for the exercise of the Licensed Rights, whether directly or through a collecting society under any voluntary or waivable statutory or compulsory licensing scheme. In all other cases the Licensor expressly reserves any right to collect such royalties.

##### Section 3 – License Conditions.

Your exercise of the Licensed Rights is expressly made subject to the following conditions.

a. ___Attribution.___

   1. If You Share the Licensed Material (including in modified form), You must:

       A. retain the following if it is supplied by the Licensor with the Licensed Material:

         i. identification of the creator(s) of the Licensed Material and any others designated to receive attribution, in any reasonable manner requested by the Licensor (including by pseudonym if designated);

         ii. a copyright notice;

         iii. a notice that refers to this Public License;

         iv. a notice that refers to the disclaimer of warranties;

         v. a URI or hyperlink to the Licensed Material to the extent reasonably practicable;

       B. indicate if You modified the Licensed Material and retain an indication of any previous modifications; and

       C. indicate the Licensed Material is licensed under this Public License, and include the text of, or the URI or hyperlink to, this Public License.

   2. You may satisfy the conditions in Section 3(a)(1) in any reasonable manner based on the medium, means, and context in which You Share the Licensed Material. For example, it may be reasonable to satisfy the conditions by providing a URI or hyperlink to a resource that includes the required information.

   3. If requested by the Licensor, You must remove any of the information required by Section 3(a)(1)(A) to the extent reasonably practicable.

b. ___ShareAlike.___

In addition to the conditions in Section 3(a), if You Share Adapted Material You produce, the following conditions also apply.

1. The Adapter’s License You apply must be a Creative Commons license with the same License Elements, this version or later, or a BY-SA Compatible License.

2. You must include the text of, or the URI or hyperlink to, the Adapter's License You apply. You may satisfy this condition in any reasonable manner based on the medium, means, and context in which You Share Adapted Material.

3. You may not offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, Adapted Material that restrict exercise of the rights granted under the Adapter's License You apply.

##### Section 4 – Sui Generis Database Rights.

Where the Licensed Rights include Sui Generis Database Rights that apply to Your use of the Licensed Material:

a. for the avoidance of doubt, Section 2(a)(1) grants You the right to extract, reuse, reproduce, and Share all or a substantial portion of the contents of the database;

b. if You include all or a substantial portion of the database contents in a database in which You have Sui Generis Database Rights, then the database in which You have Sui Generis Database Rights (but not its individual contents) is Adapted Material, including for purposes of Section 3(b); and

c. You must comply with the conditions in Section 3(a) if You Share all or a substantial portion of the contents of the database.

For the avoidance of doubt, this Section 4 supplements and does not replace Your obligations under this Public License where the Licensed Rights include other Copyright and Similar Rights.

##### Section 5 – Disclaimer of Warranties and Limitation of Liability.

a. __Unless otherwise separately undertaken by the Licensor, to the extent possible, the Licensor offers the Licensed Material as-is and as-available, and makes no representations or warranties of any kind concerning the Licensed Material, whether express, implied, statutory, or other. This includes, without limitation, warranties of title, merchantability, fitness for a particular purpose, non-infringement, absence of latent or other defects, accuracy, or the presence or absence of errors, whether or not known or discoverable. Where disclaimers of warranties are not allowed in full or in part, this disclaimer may not apply to You.__

b. __To the extent possible, in no event will the Licensor be liable to You on any legal theory (including, without limitation, negligence) or otherwise for any direct, special, indirect, incidental, consequential, punitive, exemplary, or other losses, costs, expenses, or damages arising out of this Public License or use of the Licensed Material, even if the Licensor has been advised of the possibility of such losses, costs, expenses, or damages. Where a limitation of liability is not allowed in full or in part, this limitation may not apply to You.__

c. The disclaimer of warranties and limitation of liability provided above shall be interpreted in a manner that, to the extent possible, most closely approximates an absolute disclaimer and waiver of all liability.

##### Section 6 – Term and Termination.

a. This Public License applies for the term of the Copyright and Similar Rights licensed here. However, if You fail to comply with this Public License, then Your rights under this Public License terminate automatically.

b. Where Your right to use the Licensed Material has terminated under Section 6(a), it reinstates:

   1. automatically as of the date the violation is cured, provided it is cured within 30 days of Your discovery of the violation; or

   2. upon express reinstatement by the Licensor.

   For the avoidance of doubt, this Section 6(b) does not affect any right the Licensor may have to seek remedies for Your violations of this Public License.

c. For the avoidance of doubt, the Licensor may also offer the Licensed Material under separate terms or conditions or stop distributing the Licensed Material at any time; however, doing so will not terminate this Public License.

d. Sections 1, 5, 6, 7, and 8 survive termination of this Public License.

##### Section 7 – Other Terms and Conditions.

a. The Licensor shall not be bound by any additional or different terms or conditions communicated by You unless expressly agreed.

b. Any arrangements, understandings, or agreements regarding the Licensed Material not stated herein are separate from and independent of the terms and conditions of this Public License.t stated herein are separate from and independent of the terms and conditions of this Public License.

##### Section 8 – Interpretation.

a. For the avoidance of doubt, this Public License does not, and shall not be interpreted to, reduce, limit, restrict, or impose conditions on any use of the Licensed Material that could lawfully be made without permission under this Public License.

b. To the extent possible, if any provision of this Public License is deemed unenforceable, it shall be automatically reformed to the minimum extent necessary to make it enforceable. If the provision cannot be reformed, it shall be severed from this Public License without affecting the enforceability of the remaining terms and conditions.

c. No term or condition of this Public License will be waived and no failure to comply consented to unless expressly agreed to by the Licensor.

d. Nothing in this Public License constitutes or may be interpreted as a limitation upon, or waiver of, any privileges and immunities that apply to the Licensor or You, including from the legal processes of any jurisdiction or authority.

> Creative Commons is not a party to its public licenses. Notwithstanding, Creative Commons may elect to apply one of its public licenses to material it publishes and in those instances will be considered the “Licensor.” Except for the limited purpose of indicating that material is shared under a Creative Commons public license or as otherwise permitted by the Creative Commons policies published at [creativecommons.org/policies](http://creativecommons.org/policies), Creative Commons does not authorize the use of the trademark “Creative Commons” or any other trademark or logo of Creative Commons without its prior written consent including, without limitation, in connection with any unauthorized modifications to any of its public licenses or any other arrangements, understandings, or agreements concerning use of licensed material. For the avoidance of doubt, this paragraph does not form part of the public licenses.
>
> Creative Commons may be contacted at creativecommons.org

### MIT License (**dht11.py**)
MIT License

Copyright (c) 2016 Zoltan Szarvas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.