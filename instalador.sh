#!/bin/bash

# Title		: instalador.sh
# Description	: Instala los scripts y los configura para iniciarse automáticamente
# Author	: Veltys
# Date          : 07-07-2017
# Version       : 1.1.1
# Usage		: sudo bash instalador.sh
# Notes		: Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
	directorio='/opt/RPPGCT'

	mkdir $directorio

	install ./Python/config.py.sample $directorio/
	echo "Recuerde editar ${directorio}/config.py.sample y guardarlo como config.py con los valores adecuados"
	install ./Python/comun.py $directorio/
	install ./Python/pid.py $directorio/

	echo 'Es necesario instalar el paquete psutil'
	read -p "¿Desea instalarlo de forma automática? (S/n): " eleccion
	case "$eleccion" in
		n|N )
			echo "Omitiendo instalación..."
			;;
		* )
			echo "Instalando..."
			pip3 install psutil
			;;
	esac
	install ./Python/cpu.py $directorio/
	install ./init/cpu.sh /etc/init.d/cpu
	update-rc.d cpu defaults

	install ./Python/internet.py $directorio/
	install ./Python/reiniciar_router.py $directorio/
	install ./init/reiniciar_router.sh /etc/init.d/reiniciar_router
	update-rc.d reiniciar_router defaults

	install ./Python/temperaturas.py $directorio/
	install ./init/temperaturas.sh /etc/init.d/temperaturas
	update-rc.d temperaturas defaults

	install ./Python/indice_gpio.py $directorio/

	install ./Python/domotica.py $directorio/
	install ./init/domotica.sh /etc/init.d/domotica
	update-rc.d domotica defaults
fi
