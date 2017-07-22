#!/bin/bash

# Title         : desinstalador.sh
# Description   : Desinstala los scripts y elimina la configuración para iniciarse automáticamente
# Author        : Veltys
# Date          : 10-07-2017
# Version       : 1.2.0
# Usage         : sudo bash desinstalador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
	directorio='/opt/RPPGCT'
	scripts[0]='cpu'
	scripts[1]='domotica'
	scripts[2]='reiniciar_router'
	scripts[3]='temperatura'

	for script in "${scripts[@]}"; do
		/etc/init.d/${script} stop
		rm /var/lock/${script}.lock
		rm /etc/init.d/${script}
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
