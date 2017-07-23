#!/bin/bash

# Title         : desinstalador.sh
# Description   : Desinstala los scripts y elimina la configuración para iniciarse automáticamente
# Author        : Veltys
# Date          : 23-07-2017
# Version       : 1.2.1
# Usage         : sudo bash desinstalador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
	echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
	directorio='/opt/RPPGCT'
scripts[0]='cpu'
	scripts[1]='domotica_cliente'
	scripts[2]='domotica_servidor'
	scripts[3]='reiniciar_router'
	scripts[4]='temperatura'

	for script in "${scripts[@]}"; do
		/etc/init.d/${script} stop
		update-rc.d -f ${script} remove
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
