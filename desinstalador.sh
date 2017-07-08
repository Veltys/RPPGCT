#!/bin/bash

# Title         : desinstalador.sh
# Description   : Desinstala los scripts y elimina la configuración para iniciarse automáticamente
# Author        : Veltys
# Date          : 07-07-2017
# Version       : 1.1.1
# Usage         : sudo bash desinstalador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
	directorio='/opt/RPPGCT'

	/etc/init.d/cpu stop
	rm /etc/init.d/cpu
	update-rc.d -f cpu remove
	echo 'Es posible que ya no sea necesario el paquete psutil'
	read -p "¿Desea desinstalarlo de forma automática? (S/n): " eleccion
	case "$eleccion" in
		n|N )
			echo "Omitiendo desinstalación..."
			;;
		* )
			echo "Desnstalando..."
			pip3 uninstall psutil
			;;
	esac

	/etc/init.d/reiniciar_router stop
	rm /etc/init.d/reiniciar_router
	update-rc.d -f reiniciar_router remove

	/etc/init.d/temperaturas stop
	update-rc.d -f temperaturas remove

	/etc/init.d/domotica stop
	rm /etc/init.d/domotica
	update-rc.d -f domotica remove

	rm -r $directorio/
fi
