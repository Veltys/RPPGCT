#!/bin/bash

# Title         : desinstalador.sh
# Description   : Desinstala los scripts y elimina la configuración para iniciarse automáticamente
# Author        : Veltys
# Date          : 30-11-2017
# Version       : 1.2.3
# Usage         : sudo bash desinstalador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
	directorio='/opt/RPPGCT'

	arrancables[0]='cpu'
	arrancables[1]='domotica_servidor'
	arrancables[2]='reiniciar_router'
	arrancables[3]='temperatura'

	for arrancable in "${arrancables[@]}"; do
		/etc/init.d/${arrancable} stop
		update-rc.d -f ${arrancable} remove
		rm /var/lock/${arrancable}.lock > /dev/null
		rm /etc/init.d/${arrancable}
	done

	rm -r ${directorio}/

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
fi
