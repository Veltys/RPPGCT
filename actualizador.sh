#!/bin/bash

# Title         : actualizador.sh
# Description   : Actualiza los scripts sin alterar la configuración de inicio automático
# Author        : Veltys
# Date          : 07-07-2017
# Version       : 1.1.1
# Usage         : sudo bash actualizador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
	directorio='/opt/RPPGCT'

	echo 'Recuerde revisar ./Python/config.py.sample por si la configuración ha cambiado'
	rm $directorio/comun.py
	install ./Python/comun.py $directorio/
	rm $directorio/pid.py
	install ./Python/pid.py $directorio/

	echo 'Es necesario que esté instalado el paquete psutil. No olvide instalarlo con "pip3 install psutil" si aún no está instalado'
	/etc/init.d/cpu stop
	rm $directorio/cpu.py
	rm /etc/init.d/cpu
	install ./Python/cpu.py $directorio/
	install ./init/cpu.sh /etc/init.d/cpu

	/etc/init.d/reiniciar_router stop
	rm $directorio/internet.py
	rm $directorio/reiniciar_router.py
	rm /etc/init.d/reiniciar_router
	install ./Python/internet.py $directorio/
	install ./Python/reiniciar_router.py $directorio/
	install ./init/reiniciar_router.sh /etc/init.d/reiniciar_router

	/etc/init.d/temperaturas stop
	rm $directorio/temperaturas.py
	rm /etc/init.d/temperaturas
	install ./Python/temperaturas.py $directorio/
	install ./init/temperaturas.sh /etc/init.d/temperaturas

	rm $directorio/indice_gpio.py
	install ./Python/indice_gpio.py

	echo 'Es necesario que esté instalado el paquete RPIO. No olvide instalarlo con "pip3 install RPIO" si aún no está instalado'
	/etc/init.d/domotica stop
	rm $directorio/domotica.py
	rm /etc/init.d/domotica
	install ./Python/domotica.py $directorio/
	install ./init/domotica.sh /etc/init.d/domotica
fi
